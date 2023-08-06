import time
from datetime import datetime, timedelta
import os
from tempfile import gettempdir

import click
import yaml

from nalej_platformer.plan.azure import AzureConfigPlan
from nalej_platformer.plan.organization import OrganizationPlan
from nalej_platformer.plan.k8s import KubernetesConfigPlan
from nalej_platformer.plan.ip_addresses import IPAddressesPlan
from nalej_platformer.exceptions import ApplicationPlanException, ProviderException
from nalej_platformer.utils import print_debug, spinner_ok_message, spinner_ko_message, get_indentation, get_spinner
from nalej_platformer.provider.public_api import login, provision_and_install, get_cluster_state
from nalej_platformer.provider.azure import create_service_principal, get_aks_credentials, get_cluster_by_cluster_id
from nalej_platformer.provider.azure import get_ingress_ip_from_resource_group
from nalej_platformer.provider.kubernetes import validate_cluster_installation, get_node_count


ENVIRONMENTS = [
    "PRODUCTION",
    "STAGING",
    "DEVELOPMENT"
]


class ApplicationPlan:
    def __init__(
            self, name, k8s_config, organization, cluster_id, azure_config=None, entrypoint=None, ip_addresses=None):
        self.name = name
        self.organization = organization
        self.cluster_id = cluster_id
        self.entrypoint = entrypoint
        self.azure_config = azure_config
        self.k8s_config = k8s_config
        self.ip_addresses = ip_addresses

        self._already_provisioned = False
        self._already_installed = False
        self._apply_data = {}

    def info(self, indentation=1):
        indent = get_indentation(indentation)
        org_name = self.organization.info(only_name=True)
        k8s_config = self.k8s_config.info(indentation=indentation + 1)
        info_template = (
            f"{indent}Name: {self.name}\n"
            f"{indent}Organization: {org_name}\n"
        )

        if self.cluster_id is not None:
            info_template += f'{indent}Cluster ID: {self.cluster_id}\n'

        if self.entrypoint is not None:
            info_template += f'{indent}Entrypoint: {self.entrypoint}\n'

        info_template += f"{indent}K8s configuration: \n{k8s_config}\n"

        if self.azure_config is not None:
            azure_config = self.azure_config.info(indentation=indentation + 1)
            info_template += f"{indent}Azure configuration: \n{azure_config}"

        if self.ip_addresses is not None:
            ip_addresses = self.ip_addresses.info(indentation=indentation + 1)
            info_template += f"{indent}IP Addresses: \n{ip_addresses}\n"

        info_template += '\n'
        return info_template

    def apply(self, organization_list, management):
        self._management = management
        login_address = self._management.hostnames.login
        environment = self._management.environment

        self._validate_organization(organization_list, self.organization.name)

        with get_spinner(f'Creating application cluster {self.name}...') as spinner:
            try:
                login(login_address, environment, self.organization.nalej_admin, spinner)
            except ProviderException as pexc:
                raise ApplicationPlanException(pexc)
            else:
                print_debug(f'Applying application block {self.name}')

                workflow = [
                    "_apply_create_service_principal",
                    "_apply_provision_and_install",
                    "_validate_provision_and_install",
                    "_set_application_info",
                    "_update_plan_file",
                    "_apply_validate_application_install",
                ]

                for step in workflow:
                    try:
                        getattr(self, step)()
                    except ProviderException as pexc:
                        raise ApplicationPlanException(f"Error applying plan. Details: {pexc}")

        return self

    def get_dns_zone(self):
        if self.azure_config is not None:
            return self.azure_config.dns_zone
        else:
            return self.dns_zone

    @classmethod
    def read_list(cls, plan_list=[], org_list=[]):
        app_list = []
        if plan_list is None:
            return app_list

        click.echo("APPLICATION CLUSTERS: ")
        for i, plan in enumerate(plan_list, start=1):
            click.echo(f"Application cluster {i}")
            app_list.append(cls.read_plan(plan, org_list))
            click.echo('\n')
        return app_list

    @classmethod
    def read_plan(cls, plan_data, org_list):
        print_debug(f"Reading application plan block. Raw data: {plan_data}")
        if plan_data is None:
            raise ApplicationPlanException("No block found in plan")
        name = cls._validate_name(plan_data.get("name", None))
        cluster_id = plan_data.get("clusterID", None)
        entrypoint = plan_data.get("entrypoint", None)
        azure_config = AzureConfigPlan.read_plan(plan_data.get("azure", None))
        region = azure_config.region if azure_config is not None else None
        k8s_config = KubernetesConfigPlan.read_plan(plan_data.get("kubernetes", None), region)
        ip_addresses = IPAddressesPlan.read_plan(plan_data.get("ipAddresses", None))
        organization_name = plan_data.get("organization", None)
        organization = cls._validate_organization(org_list, organization_name)

        return cls(name, k8s_config, organization, cluster_id, azure_config, entrypoint, ip_addresses)

    @classmethod
    def apply_list(cls, application_list, organization_list, management):
        print_debug("Applying application block")

        applied_list = [app.apply(organization_list, management) for app in application_list]
        # cls._update_plan_file(applied_list)
        return applied_list

    @classmethod
    def _validate_name(cls, name):
        with get_spinner("Checking application cluster name is valid...") as spinner:
            if name in ["", None]:
                spinner_ko_message(spinner, "Application cluster name is empty")
                raise ApplicationPlanException("Name must not be empty")

            spinner_ok_message(spinner, "Application cluster name is valid")
        return name

    @classmethod
    def _validate_organization(cls, org_list, name):
        if name is None:
            raise ApplicationPlanException("No organization is set for this application")
        return OrganizationPlan.find_by_name(org_list, name)

    def _apply_create_service_principal(self):
        with get_spinner("Getting a service principal for provisioning...") as spinner:
            self._apply_data["sp_path"] = create_service_principal(spinner)

    def _apply_provision_and_install(self):
        node_count = None
        with get_spinner(f'Provisioning and/or installing application cluster {self.name}...') as spinner:
            if self.k8s_config.kubeconfig is not None:
                spinner.text = "Checking if application cluster is already provisioned..."
                try:
                    node_count = get_node_count(self.k8s_config.kubeconfig)
                    cluster_state = get_cluster_state(
                        self._management.hostnames.api, self._management.environment, self.cluster_id, spinner)
                except ProviderException as pexc:
                    raise ApplicationPlanException(pexc)
                else:
                    if cluster_state == 'PROVISIONED':
                        self._already_provisioned = True
                        # TODO: Install a previously provisioned cluster
                        spinner_ok_message(spinner, "Application cluster is already provisioned")
                        raise ApplicationPlanException("Install only application cluster workflow not supported yet")
                    elif cluster_state == 'INSTALLED':
                        self._already_provisioned = True
                        if validate_cluster_installation(self.k8s_config.kubeconfig, spinner, True):
                            self._already_installed = True
            else:
                sp_path = self._apply_data.get("sp_path", "")
                self._apply_data["provision_result"] = provision_and_install(
                    sp_path, self.azure_config.vm_size, self.azure_config.region, self.name,
                    self.azure_config.resource_group, self.azure_config.dns_zone, self.k8s_config.version,
                    self.k8s_config.num_nodes, self._management.environment, self._management.hostnames.api,
                    self.organization.organization_id, spinner
                )

        try:
            if node_count is not None:
                self.k8s_config.validate_num_nodes(node_count)
                self._already_provisioned = True
                spinner_ok_message(spinner, "Already provisioned application cluster seems valid")
        except ProviderException as pexc:
            raise ApplicationPlanException(pexc)

    def _validate_provision_and_install(self):
        if not self._already_installed:
            start_time = datetime.now()
            with get_spinner('Validating application cluster provision and install...') as spinner:
                cluster_id = self._apply_data["provision_result"]["cluster_id"]
                for i in range(0, 36):
                    elapsed_time = datetime.now() - start_time
                    elapsed_time = elapsed_time - timedelta(microseconds=elapsed_time.microseconds)
                    spinner.text = f'Validating application cluster provision and install... [{elapsed_time}]'
                    try:
                        cluster_state = get_cluster_state(
                            self._management.hostnames.api, self._management.environment, cluster_id, spinner)
                    except ProviderException as pexc:
                        raise ApplicationPlanException(pexc)
                    else:
                        if cluster_state == "FAILURE":
                            spinner_ko_message(spinner, "Application cluster failed to provision and/or install")
                            raise ApplicationPlanException("Application cluster failed to provision and/or install")
                        elif cluster_state == "INSTALLED":
                            spinner_ok_message(spinner, "Application cluster finished provision and/or install")
                            return
                        else:
                            time.sleep(60)
                raise ApplicationPlanException("Timeout waiting for application cluster to provision and/or install")

    def _set_application_info(self):
        if not self._already_provisioned:
            provision_result = self._apply_data.get("provision_result", {})
            self.cluster_id = provision_result['cluster_id']

            with get_spinner('Getting cluster information from Azure...') as spinner:
                cluster_info = get_cluster_by_cluster_id(self.cluster_id, spinner)

            cluster_name = f"appcluster-{self.cluster_id}"
            self.azure_config.aks_cluster_name = cluster_name

            dns_zone = self.get_dns_zone()
            self.entrypoint = f'*.{self.name}.{dns_zone}'

            kubeconfig_path = os.path.join(gettempdir(), f'{cluster_name}.yaml')
            with get_spinner('Getting AKS cluster kubeconfig file...') as spinner:
                get_aks_credentials(self.azure_config.resource_group, cluster_name, kubeconfig_path, spinner)
                self.k8s_config._set_kubeconfig(kubeconfig_path, cluster_name)

            with get_spinner('Getting Ingress IP Address...') as spinner:
                ingress_address = get_ingress_ip_from_resource_group(cluster_info['nodeResourceGroup'], spinner)
                self.ip_addresses = IPAddressesPlan(ingress=ingress_address)

    def _update_plan_file(self):
        if not self._already_provisioned:
            with get_spinner("Updating plan file...") as spinner:
                ctx = click.get_current_context()
                yaml_contents = {}
                with open(ctx.obj['PLAN_PATH'], "r") as plan_file:
                    yaml_contents = yaml.load(plan_file, Loader=yaml.FullLoader)

                application_list = yaml_contents.get("application", None)
                if application_list is None:
                    spinner_ko_message(spinner, "The original plan file is malformed")
                    raise ApplicationPlanException("No application block found in plan file")

                for i, application_block in enumerate(application_list):
                    if application_block['name'] == self.name:
                        application_block['clusterID'] = self.cluster_id
                        application_block['entrypoint'] = self.entrypoint
                        application_block['ipAddresses'] = self.ip_addresses.dict_for_yaml()
                        application_block['kubernetes'] = self.k8s_config.dict_for_yaml()
                        application_block['azure'] = self.azure_config.dict_for_yaml()

                        application_list[i] = application_block

                yaml_contents["application"] = application_list

                with open(ctx.obj['PLAN_PATH'], "w") as plan_file:
                    plan_file.write(yaml.dump(yaml_contents, default_flow_style=False))

                spinner_ok_message(spinner, "Updated plan file")

    def _apply_validate_application_install(self):
        if not self._already_installed:
            with get_spinner("Validating cluster installation...") as spinner:
                validate_cluster_installation(self.k8s_config.kubeconfig, spinner)
