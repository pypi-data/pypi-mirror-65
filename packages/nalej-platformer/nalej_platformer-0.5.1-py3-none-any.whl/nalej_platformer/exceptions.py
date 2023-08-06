class ConfigException(Exception):
    """Exception raised when the configuration file is not valid"""

    def __init__(self, message):
        self.message = message


class PlanException(Exception):
    """Exception raised if something in the plan is not valid"""

    def __init__(self, message):
        self.message = message


class ManagementPlanException(PlanException):
    """Exception raised if something in the management plan is not valid"""

    def __init__(self, message):
        self.message = message


class ApplicationPlanException(PlanException):
    """Exception raised if something in the application plan is not valid"""

    def __init__(self, message):
        self.message = message


class AzureConfigPlanException(PlanException):
    """Exception raised if something in the azure config block is not valid"""

    def __init__(self, message):
        self.message = message


class KubernetesConfigPlanException(PlanException):
    """Exception raised if something in the kubernetes config block is not valid"""

    def __init__(self, message):
        self.message = message


class OrganizationPlanException(PlanException):
    """Exception raised if something in the organization config block is not valid"""

    def __init__(self, message):
        self.message = message


class HostnamesPlanException(PlanException):
    """Exception raised if something in the hostnames block is not valid"""

    def __init__(self, message):
        self.message = message


class IPAddressesPlanException(PlanException):
    """Exception raised if something in the IP Addresses block is not valid"""

    def __init__(self, message):
        self.message = message


class ProviderException(Exception):
    """Base exception for provider related exceptions"""

    def __init__(self, message):
        self.message = message


class AzureProviderException(ProviderException):
    """Exception using Azure provider calls"""

    def __init__(self, message):
        self.message = message


class KubernetesProviderException(ProviderException):
    """Exception using Kubernetes provider calls"""

    def __init__(self, message):
        self.message = message


class InstallerProviderException(ProviderException):
    """Exception using Installer provider calls"""

    def __init__(self, message):
        self.message = message


class ProvisionerProviderException(ProviderException):
    """Exception using Provisioner provider calls"""

    def __init__(self, message):
        self.message = message


class SignupProviderException(ProviderException):
    """Exception using Signup provider calls"""

    def __init__(self, message):
        self.message = message


class PublicApiProviderException(ProviderException):
    """Exception using Public API provider calls"""

    def __init__(self, message):
        self.message = message
