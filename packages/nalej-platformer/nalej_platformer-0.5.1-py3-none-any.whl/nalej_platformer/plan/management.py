import click
import yaml

from nalej_platformer.plan.azure import AzureConfigPlan
from nalej_platformer.plan.k8s import KubernetesConfigPlan
from nalej_platformer.plan.hostnames import HostnamesPlan
from nalej_platformer.plan.ip_addresses import IPAddressesPlan
from nalej_platformer.exceptions import ManagementPlanException, ProviderException
from nalej_platformer.utils import rreplace, print_debug, spinner_ok_message, spinner_ko_message, get_indentation
from nalej_platformer.utils import get_spinner
from nalej_platformer.provider.azure import create_service_principal
from nalej_platformer.provider.provisioner import provision_management_cluster
from nalej_platformer.provider.installer import install_management_cluster
from nalej_platformer.provider.kubernetes import validate_cluster_installation, get_node_count


ENVIRONMENTS = [
    "PRODUCTION",
    "STAGING",
    "DEVELOPMENT"
]


class ManagementPlan:
    def __init__(
            self, name, k8s_config, environment, azure_config=None, hostnames=None, ip_addresses=None):
        self.name = name
        self.azure_config = azure_config
        self.k8s_config = k8s_config
        self.environment = environment
        self.hostnames = hostnames
        self.ip_addresses = ip_addresses

        self._already_provisioned = False
        self._already_installed = False
        self._apply_data = {}

    def info(self, indentation=1):
        indent = get_indentation(indentation)
        k8s_config = self.k8s_config.info(indentation=indentation + 1)

        info_template = (
            f"{indent}Name: {self.name}\n"
            f"{indent}Environment: {self.environment}\n"
            f"{indent}K8s configuration: \n{k8s_config}\n"
        )

        if self.azure_config is not None:
            azure_config = self.azure_config.info(indentation=indentation + 1)
            info_template += f"{indent}Azure configuration: \n{azure_config}\n"

        if self.hostnames is not None:
            hostnames = self.hostnames.info(indentation=indentation + 1)
            info_template += f"{indent}Hostnames: \n{hostnames}"

        if self.ip_addresses is not None:
            ip_addresses = self.ip_addresses.info(indentation=indentation + 1)
            info_template += f"{indent}IP Addresses: \n{ip_addresses}\n"

        return info_template

    def apply(self):
        workflow = [
            "_apply_create_service_principal",
            "_apply_provision_management_cluster",
            "_set_management_info",
            "_update_plan_file",
            "_apply_install_management_cluster",
            "_apply_validate_management_install",
        ]
        print_debug("Applying management block")

        for step in workflow:
            try:
                getattr(self, step)()
            except ProviderException as pexc:
                raise ManagementPlanException(f"Error applying plan. Details: {pexc}")

    @classmethod
    def read_plan(cls, plan_data):
        print_debug(f"Reading management plan block. Raw data: {plan_data}")
        click.echo("MANAGEMENT CLUSTER: ")
        if plan_data is None:
            raise ManagementPlanException("No block found in plan")

        name = cls._validate_name(plan_data.get("name", None))
        environment = cls._validate_environment(plan_data.get("environment", None))
        azure_config = AzureConfigPlan.read_plan(plan_data.get("azure", None))
        region = None if azure_config is None else azure_config.region
        k8s_config = KubernetesConfigPlan.read_plan(plan_data.get("kubernetes", None), region)
        hostnames = HostnamesPlan.read_plan(plan_data.get("hostnames", None))
        ip_addresses = IPAddressesPlan.read_plan(plan_data.get("ipAddresses", None))
        dns_zone = cls._validate_dns_zone(plan_data.get("dns_zone", None))

        if azure_config is None and dns_zone is None:
            raise ManagementPlanException("No DNS Zone defined or Azure block containing it found")
        if azure_config is not None and dns_zone is not None:
            raise ManagementPlanException("Duplicated DNS Zone defined in both Azure block and DNS Zone field")

        click.echo('\n')

        return cls(name, k8s_config, environment, azure_config, hostnames, ip_addresses)

    def get_dns_zone(self):
        if self.azure_config is not None:
            return self.azure_config.dns_zone
        else:
            return self.dns_zone

    @staticmethod
    def _validate_name(name):
        with get_spinner("Checking management cluster name is valid...") as spinner:
            if name in ["", None]:
                spinner_ko_message(spinner, "Management cluster name is empty")
                raise ManagementPlanException("Name must not be empty")

            spinner_ok_message(spinner, "Management cluster name is valid")
        return name

    @staticmethod
    def _validate_dns_zone(dns_zone):
        if dns_zone is not None:
            with get_spinner("Checking management cluster DNS Zone is valid...") as spinner:
                if dns_zone in ["", None]:
                    spinner_ko_message(spinner, "Management cluster DNS Zone is empty")
                    raise ManagementPlanException("Management cluster DNS Zone must not be empty")

                spinner_ok_message(spinner, "Management cluster DNS Zone is valid")
        return dns_zone

    @staticmethod
    def _validate_environment(environment):
        with get_spinner("Checking platform environment is valid...") as spinner:
            if environment in ["", None]:
                spinner_ko_message(spinner, "Environment is empty")
                raise ManagementPlanException("Environment must not be empty")

            environment = environment.upper()
            if environment not in ENVIRONMENTS:
                env_list = rreplace(', '.join(ENVIRONMENTS), ', ', ' or ', 1)
                spinner_ko_message(spinner, "Environment is not valid")
                raise ManagementPlanException(f"Invalid environment. Must be {env_list}")

            spinner_ok_message(spinner, f"Environment: {environment}")
        return environment

    def _apply_create_service_principal(self):
        with get_spinner("Getting a service principal for provisioning...") as spinner:
            self._apply_data["sp_path"] = create_service_principal(spinner)

    def _apply_provision_management_cluster(self):
        node_count = None
        with get_spinner("Provisioning management cluster...") as spinner:
            if self.k8s_config.kubeconfig is not None:
                spinner.text = "Checking if management cluster is already provisioned..."
                try:
                    node_count = get_node_count(self.k8s_config.kubeconfig)
                except ProviderException as pexc:
                    raise ManagementPlanException(pexc)
                else:
                    spinner_ok_message(spinner, "Management cluster is already provisioned")
            else:
                sp_path = self._apply_data.get("sp_path", "")
                try:
                    self._apply_data["provision_result"] = provision_management_cluster(
                        sp_path, self.azure_config.vm_size, self.azure_config.region, self.name,
                        self.azure_config.resource_group, self.azure_config.dns_zone, self.k8s_config.version,
                        self.k8s_config.num_nodes, self.environment, spinner
                    )
                except ProviderException as pexc:
                    raise ManagementPlanException(pexc)

        try:
            if node_count is not None:
                self.k8s_config.validate_num_nodes(node_count)
                self._already_provisioned = True
                spinner_ok_message(spinner, "Already provisioned management cluster seems valid")
        except ProviderException as pexc:
            raise ManagementPlanException(pexc)

    def _set_management_info(self):
        if not self._already_provisioned:
            provision_result = self._apply_data.get("provision_result", {})
            dns_zone = self.get_dns_zone()
            cluster_name = f"mngt-{self.name}"

            self.k8s_config._set_kubeconfig(provision_result.get("kubeconfig", None), cluster_name)
            self.azure_config.aks_cluster_name = cluster_name

            self.hostnames = HostnamesPlan(**{
                "web": f"web.{self.name}.{dns_zone}",
                "api": f"api.{self.name}.{dns_zone}",
                "login": f"login.{self.name}.{dns_zone}",
                "signup": f"signup.{self.name}.{dns_zone}"
            })

            self.ip_addresses = IPAddressesPlan(**{
                "ingress": provision_result.get("ingress_ip", None),
                "dns": provision_result.get("dns_ip", None),
                "coredns": provision_result.get("coredns_ip", None),
                "vpn_server": provision_result.get("vpnserver_ip", None)
            })

    def _update_plan_file(self):
        if not self._already_provisioned:
            with get_spinner("Updating plan file...") as spinner:
                ctx = click.get_current_context()
                yaml_contents = {}
                with open(ctx.obj['PLAN_PATH'], "r") as plan_file:
                    yaml_contents = yaml.load(plan_file, Loader=yaml.FullLoader)

                management_block = yaml_contents.get("management", None)
                if management_block is None:
                    spinner_ko_message(spinner, "The original plan file is malformed")
                    raise ManagementPlanException("No management block found in plan file")
                management_block["hostnames"] = self.hostnames.dict_for_yaml()
                management_block["ipAddresses"] = self.ip_addresses.dict_for_yaml()
                management_block["kubernetes"] = self.k8s_config.dict_for_yaml()
                management_block["azure"] = self.azure_config.dict_for_yaml()

                yaml_contents["management"] = management_block

                with open(ctx.obj['PLAN_PATH'], "w") as plan_file:
                    plan_file.write(yaml.dump(yaml_contents, default_flow_style=False))

                spinner_ok_message(spinner, "Updated plan file")

    def _apply_install_management_cluster(self):
        with get_spinner("Installing management cluster...") as spinner:
            if self._already_provisioned:
                spinner.text = "Checking if Nalej is installed and running"
                if validate_cluster_installation(self.k8s_config.kubeconfig, spinner):
                    self._already_installed = True
                    return

            install_management_cluster(
                self.k8s_config.kubeconfig, self.name, self.environment, self.get_dns_zone(),
                self.ip_addresses.ingress, self.ip_addresses.dns, self.ip_addresses.coredns,
                self.ip_addresses.vpn_server, spinner)

    def _apply_validate_management_install(self):
        if not self._already_installed:
            with get_spinner("Validating cluster installation...") as spinner:
                validate_cluster_installation(self.k8s_config.kubeconfig, spinner)
