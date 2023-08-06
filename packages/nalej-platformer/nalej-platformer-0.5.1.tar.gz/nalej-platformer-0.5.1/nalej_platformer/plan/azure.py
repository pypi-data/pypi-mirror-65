from nalej_platformer.exceptions import AzureConfigPlanException, AzureProviderException
from nalej_platformer.utils import print_debug, spinner_ko_message, get_indentation, get_spinner
from nalej_platformer.provider import azure as azure_provider


class AzureConfigPlan:
    def __init__(self, resource_group, region, dns_zone, vm_size, aks_cluster_name=None):
        self.resource_group = resource_group
        self.region = region
        self.dns_zone = dns_zone
        self.vm_size = vm_size
        self.aks_cluster_name = aks_cluster_name

    def info(self, indentation=2):
        indent = get_indentation(indentation)

        info_template = (
            f"{indent}Resource Group: {self.resource_group}\n"
            f"{indent}Region: {self.region}\n"
            f"{indent}DNS Zone: {self.dns_zone}\n"
            f"{indent}Node VM Size: {self.vm_size}"

        )

        if self.aks_cluster_name is not None:
            info_template += f"\n{indent}AKS Cluster Name: {self.aks_cluster_name}."

        return info_template

    @classmethod
    def read_plan(cls, plan_data):
        print_debug(f"Reading azure configuration block. Raw data: {plan_data}")
        if plan_data is None:
            return None

        try:
            resource_group = cls._validate_resource_group(plan_data.get("resourceGroup", None))
            region = cls._validate_region(plan_data.get("region", None))
            dns_zone = cls._validate_dns_zone(plan_data.get("dnsZone", None))
            vm_size = cls._validate_vm_size(plan_data.get("vmSize", None), region)
            aks_cluster_name = cls._validate_aks_cluster_name(plan_data.get("aksName", None), resource_group)

        except AzureProviderException as ape:
            raise AzureConfigPlanException(f"Error checking with Azure: {ape}")

        return cls(resource_group, region, dns_zone, vm_size, aks_cluster_name)

    @classmethod
    def _validate_resource_group(cls, resource_group):
        with get_spinner("Checking resource group is valid...") as spinner:
            if resource_group in ["", None]:
                spinner_ko_message(spinner, "Resource group name is empty")
                raise AzureConfigPlanException("Resource group must not be empty")

            return azure_provider.check_resource_group(resource_group, spinner)

    @classmethod
    def _validate_region(cls, region):
        with get_spinner("Checking Azure region is valid...") as spinner:
            if region in ["", None]:
                spinner_ko_message(spinner, "Azure region name is empty")
                raise AzureConfigPlanException("Azure region must not be empty")

            return azure_provider.check_region(region, spinner)

    @classmethod
    def _validate_dns_zone(cls, dns_zone):
        with get_spinner("Checking DNS Zone is valid...") as spinner:
            if dns_zone in ["", None]:
                spinner_ko_message(spinner, "Azure DNS zone name is empty")
                raise AzureConfigPlanException("Azure DNS zone must not be empty")

            return azure_provider.check_dns_zone(dns_zone, spinner)

    @classmethod
    def _validate_vm_size(cls, vm_size, region):
        with get_spinner("Checking VM size is valid...") as spinner:
            if vm_size in ["", None]:
                spinner_ko_message(spinner, "Azure VM size name is empty")
                raise AzureConfigPlanException("Azure VM size name must not be empty")

            return azure_provider.check_vm_size(vm_size, region, spinner)

    @classmethod
    def _validate_aks_cluster_name(cls, cluster_name=None, resource_group=None):
        if cluster_name is None:
            return cluster_name

        with get_spinner("Checking AKS cluster name exists...") as spinner:
            if cluster_name in ["", None]:
                spinner_ko_message(spinner, "AKS cluster name is empty")
                raise AzureConfigPlanException("AKS cluster name must not be empty")

            return azure_provider.check_aks_cluster_name(cluster_name, resource_group, spinner)

    def dict_for_yaml(self):
        yaml_data = {
            "resourceGroup": self.resource_group,
            "region": self.region,
            "dnsZone": self.dns_zone,
            "vmSize": self.vm_size
        }

        if self.aks_cluster_name is not None:
            yaml_data["aksName"] = self.aks_cluster_name

        return yaml_data
