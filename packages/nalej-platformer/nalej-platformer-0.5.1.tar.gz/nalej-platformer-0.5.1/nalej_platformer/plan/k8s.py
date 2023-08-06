import os

import vistir

from nalej_platformer.exceptions import KubernetesConfigPlanException, AzureProviderException
from nalej_platformer.utils import print_debug, spinner_ko_message, spinner_ok_message, copy_kubeconfig
from nalej_platformer.utils import get_indentation, get_spinner
from nalej_platformer.provider.azure import check_k8s_version
from nalej_platformer.config.defaults import KC_PATH


class KubernetesConfigPlan:
    def __init__(self, version, num_nodes, kubeconfig):
        self.version = version
        self.num_nodes = num_nodes
        self.kubeconfig = kubeconfig

    def info(self, indentation=2):
        indent = get_indentation(indentation)
        info_template = (
            f"{indent}Version: {self.version}\n"
            f"{indent}Number of nodes: {self.num_nodes}"
        )

        if self.kubeconfig is not None:
            info_template += f"\n{indent}Kubeconfig: {self.kubeconfig}."

        return info_template

    @classmethod
    def read_plan(cls, plan_data, region=None):
        print_debug(f"Reading kubernetes configuration block. Raw data: {plan_data}")
        if plan_data is None:
            raise KubernetesConfigPlanException("Kubernetes configuration block is required")

        try:
            version = cls._validate_version(plan_data.get("version", None), region)
            num_nodes = cls.validate_num_nodes(plan_data.get("nodes", None))
        except AzureProviderException as ape:
            raise KubernetesConfigPlanException(f"Error checking with Azure: {ape}")

        kubeconfig = cls._validate_kubeconfig(plan_data.get("kubeconfig", None))

        return cls(version, num_nodes, kubeconfig)

    @classmethod
    def _validate_version(cls, version, region=None):
        with get_spinner("Checking kubernetes version is valid...") as spinner:
            if version in ["", None]:
                spinner_ko_message(spinner, "Kubernetes version is empty")
                raise KubernetesConfigPlanException("Kubernetes version must not be empty")

            cls._check_minimum_k8s_version(version, spinner)

            if region is None:
                return version
            else:
                return check_k8s_version(version, region, spinner)

    @staticmethod
    def validate_num_nodes(num_nodes):
        with get_spinner("Checking number of nodes are valid...") as spinner:
            if num_nodes in [None, ""]:
                spinner_ko_message(spinner, "Number of nodes is empty")
                raise KubernetesConfigPlanException("Number of nodes must not be empty")

            if num_nodes < 3:
                spinner_ko_message(spinner, "Number of nodes are lower than 3")
                raise KubernetesConfigPlanException("The minimum number of nodes is 3")

            spinner_ok_message(spinner, "Number of nodes is valid")
            return num_nodes

    @staticmethod
    def _validate_kubeconfig(kubeconfig):
        if kubeconfig is not None:
            if os.path.exists(kubeconfig):
                return vistir.path.normalize_path(kubeconfig)
            else:
                raise KubernetesConfigPlanException("Kubeconfig file not found")

        return kubeconfig

    @staticmethod
    def _check_minimum_k8s_version(version, spinner):
        version_numbers = version.split(".")
        if len(version_numbers) < 2:
            spinner_ko_message(spinner, "Kubernetes version format is not valid")
            raise KubernetesConfigPlanException("Kubernetes version is not valid")

        try:
            major_version = int(version_numbers[0])
            minor_version = int(version_numbers[1])
        except ValueError:
            spinner_ko_message(spinner, "Kubernetes version format is not valid")
            raise KubernetesConfigPlanException("Kubernetes version is not valid")

        if major_version < 1 and minor_version < 11:
            spinner_ko_message(spinner, "Kubernetes version is not at least 1.11")
            raise KubernetesConfigPlanException("Kubernetes version is not valid")

    def _set_kubeconfig(self, source_path, cluster_name):
        if source_path is None:
            raise KubernetesConfigPlanException("Kubeconfig not present after provision")

        vistir.path.mkdir_p(KC_PATH)

        kc_dest_path = os.path.join(KC_PATH, f"{cluster_name}.yaml")
        copy_kubeconfig(source_path, kc_dest_path)

        self.kubeconfig = kc_dest_path
        try:
            os.remove(source_path)
        except FileNotFoundError:
            pass

    def dict_for_yaml(self):
        yaml_data = {
            "version": self.version,
            "nodes": self.num_nodes
        }

        if self.kubeconfig is not None:
            yaml_data["kubeconfig"] = self.kubeconfig

        return yaml_data
