import os
import subprocess
import json
import getpass
import time

import click

from nalej_platformer.exceptions import AzureProviderException
from nalej_platformer.utils import print_debug, spinner_ko_message, spinner_ok_message, get_spinner
from nalej_platformer.config.defaults import SP_PATH


def _get_path():
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.az_path


def login():
    with get_spinner(text="Logging to Azure...") as spinner:
        username = os.environ.get("AZURE_USERNAME", None)
        password = os.environ.get("AZURE_PASSWORD", None)
        if username is None or password is None:
            spinner_ko_message(spinner, "Error logging in to Azure")
            raise AzureProviderException(
                "Azure username or password not defined. Please ensure that both environment variables are set")

        print_debug(f'Logging in to Azure using username: {username} and password: {"*"*len(password)}')
        try:
            cmd = f"{_get_path()} login --username {username} --password {password}"
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as cpe:
            print_debug(f'Error logging in to Azure. Output: {cpe.stdout}. Error: {cpe.stderr}.')
            spinner_ko_message(spinner, "Error logging in to Azure")
            raise AzureProviderException("Error logging to Azure with the provided credentials")
        else:
            print_debug('Logged in to Azure successfully')
            spinner_ok_message(spinner, "Logged in to Azure")
            return True


def check_resource_group(resource_group, spinner):
    if resource_group in ["", None]:
        spinner_ko_message(spinner, "Error checking Azure Resource Group")
        raise AzureProviderException("Resource group name is empty")

    try:
        print_debug(f'Checking Azure Resource group: {resource_group} exists')
        cmd = f"{_get_path()} group show --name {resource_group}"
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error checking Azure Resource group. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, "Error checking Azure Resource Group")
        raise AzureProviderException("Error checking resource group")
    else:
        spinner_ok_message(spinner, "Azure Resource Group exists")
        return resource_group


def check_region(region, spinner):
    if region in ["", None]:
        spinner_ko_message(spinner, "Error checking Azure Region")
        raise AzureProviderException("Region name is empty")

    try:
        print_debug(f'Checking Azure Region {region} exists')
        cmd = (
            f"{_get_path()} account list-locations --query "
            f"\"[?displayName=='{region}' || name=='{region}'].displayName | [0]\""
        )
        get_region = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error checking Azure region. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, "Error checking Azure Region")
        raise AzureProviderException("Error checking Azure region")
    else:
        output = get_region.stdout.strip('"\n')
        if output == "":
            spinner_ko_message(spinner, "No matching region found")
            raise AzureProviderException(f'No matching region found for {region}')
        spinner_ok_message(spinner, f"Found matching Azure region: {output}")
        return output


def check_dns_zone(dns_zone, spinner):
    if dns_zone in ["", None]:
        spinner_ko_message(spinner, "Error checking DNS Zone")
        raise AzureProviderException("DNS Zone is empty")

    try:
        print_debug(f'Checking Azure DNS Zone {dns_zone} exists')
        cmd = f"{_get_path()} network dns zone list --query \"[?name=='{dns_zone}'] | [0].[name, resourceGroup]\""
        get_dns_zone = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error checking DNS Zone. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, "Error checking DNS Zone")
        raise AzureProviderException("Error checking DNS Zone")
    else:
        output = get_dns_zone.stdout.strip('"\n')
        if output == "":
            spinner_ko_message(spinner, "No matching DNS Zone found")
            raise AzureProviderException(f'No matching region found for {dns_zone}')

        output_json = json.loads(output)
        matched_zone = output_json[0]
        matched_resource_group = output_json[1]

        spinner_ok_message(spinner, f"Found DNS Zone: {matched_zone} in {matched_resource_group} resource group")
        return matched_zone


def check_vm_size(vm_size, region, spinner):
    if vm_size in ["", None]:
        spinner_ko_message(spinner, "Error checking VM size")
        raise AzureProviderException("VM size is empty")
    if region in ["", None]:
        spinner_ko_message(spinner, "Error checking VM size")
        raise AzureProviderException("Region name is empty")

    try:
        print_debug(f'Checking VM Size {vm_size} for {region} Azure Region')
        cmd = f"{_get_path()} vm list-sizes --location '{region}' --query \"[?name=='{vm_size}'].name | [0]\""
        get_vm_size = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error checking VM size. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, "Error checking VM size")
        raise AzureProviderException("Error checking VM size")
    else:
        output = get_vm_size.stdout.strip('"\n')
        if output == "":
            spinner_ko_message(spinner, "No matching VM size found")
            raise AzureProviderException(f'No matching VM size found for {vm_size} in {region} region')

        spinner_ok_message(spinner, f"Found VM Size: {output} in {region} region")
        return output


def check_k8s_version(version, region, spinner):
    if version in ["", None]:
        spinner_ko_message(spinner, "Error checking Kubernetes version")
        raise AzureProviderException("Kubernetes version is empty")
    if region in ["", None]:
        spinner_ko_message(spinner, "Error checking Kubernetes version")
        raise AzureProviderException("Region name is empty")

    try:
        print_debug(f'Checking K8s version {version} is available in {region} Azure Region')
        cmd = (
            f"{_get_path()} aks get-versions --location '{region}' --query "
            f"\"orchestrators[?orchestratorType=='Kubernetes' && orchestratorVersion=='{version}'] | [0]\""
        )
        get_k8s_version = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error checking Kubernetes version. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, "Error checking Kubernetes version")
        raise AzureProviderException("Error checking Kubernetes version")
    else:
        output = get_k8s_version.stdout.strip('"\n')
        if output == "":
            spinner_ko_message(spinner, "No matching Kubernetes version found")
            raise AzureProviderException(f'No matching region found for {version} in {region} region')

        output_json = json.loads(output)
        matched_version = output_json["orchestratorVersion"]
        is_preview = output_json["isPreview"]
        if is_preview:
            spinner_ko_message(spinner, "Kubernetes version is not stable")
            raise AzureProviderException(f'Kubernetes version {version} is in preview state and not production ready')

        spinner_ok_message(spinner, f"Found Kubernetes version: {matched_version} in {region} region")
        return matched_version


def check_aks_cluster_name(cluster_name, resource_group, spinner, required=True):
    if cluster_name in ["", None]:
        spinner_ko_message(spinner, "Error checking AKS cluster name")
        raise AzureProviderException("Cluster name is empty")
    if resource_group in ["", None]:
        spinner_ko_message(spinner, "Error checking AKS cluster name")
        raise AzureProviderException("Resource group is empty")

    try:
        print_debug(f'Checking if AKS service {cluster_name} exists in {resource_group} Azure Resource Group')
        cmd = f"{_get_path()} aks show --resource-group {resource_group} --name {cluster_name}"
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        if required:
            print_debug(f'Error getting AKS cluster name. Output: {cpe.stdout}. Error: {cpe.stderr}.')
            spinner_ko_message(spinner, "Error getting AKS cluster name")
            raise AzureProviderException("Error getting AKS cluster name")
        else:
            spinner_ok_message(spinner, "AKS cluster name does not exist")
    else:
        spinner_ok_message(spinner, f"AKS cluster name {cluster_name} exists")

    return cluster_name


def create_service_principal(spinner):
    if os.path.exists(SP_PATH):
        print_debug("Service Principal for provisioning already exists")
        spinner_ok_message(spinner, "Service Principal already exists")
    else:
        print_debug("No Service Principal for provisioning found, creating")
        sp_name = f"{getpass.getuser()}_provisioner"

        try:
            print_debug(f'Creating new Service Principal with name {sp_name}')
            cmd = f"{_get_path()} ad sp create-for-rbac --name http://{sp_name} --sdk-auth"
            create_sp = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as cpe:
            print_debug(f'Error creating provisioner service principal. Output: {cpe.stdout}. Error: {cpe.stderr}.')
            spinner_ko_message(spinner, "Error creating Azure Service Principal")
            raise AzureProviderException("Error creating Azure Service Principal")
        else:
            with open(SP_PATH, "w") as sp_file:
                sp_file.write(create_sp.stdout)
                print_debug(f'Provisioner Service Principal file created at {SP_PATH}')

            time.sleep(30)  # Sleep to give enough time for Azure to really create the SP
        spinner_ok_message(spinner, "Service Principal created successfully")
    return SP_PATH


def get_cluster_by_cluster_id(cluster_id, spinner):
    try:
        print_debug(f'Getting AKS cluster information for Cluster ID: {cluster_id}')

        cmd = f'{_get_path()} aks list --query "[?tags.clusterID==\'{cluster_id}\']"'
        cluster_info = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error getting cluster info from Azure. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, "Error getting cluster info from Azure")
        raise AzureProviderException("Error getting cluster info from Azure")
    else:
        try:
            json_info = json.loads(cluster_info.stdout)
        except json.JSONDecodeError:
            raise AzureProviderException("Malformed response getting cluster info from Azure")
        else:
            spinner_ok_message(spinner, "Retrieved cluster information from Azure successfully")
            return json_info[0]


def get_aks_credentials(resource_group, cluster_name, kubeconfig_path, spinner):
    try:
        print_debug(f'Getting AKS cluster kubeconfig file cluster: {cluster_name} on {resource_group} resource group')

        cmd = (
            f'{_get_path()} aks get-credentials --resource-group {resource_group} '
            f'--name {cluster_name} --file {kubeconfig_path} --overwrite-existing'
        )
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error getting AKS cluster kubeconfig file. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, "Error getting AKS cluster kubeconfig file")
        raise AzureProviderException("Error getting AKS cluster kubeconfig file")
    else:
        spinner_ok_message(spinner, "Retrieved AKS cluster kubeconfig file successfully")


def get_ingress_ip_from_resource_group(resource_group, spinner):
    try:
        print_debug(f'Getting Ingress IP Address from {resource_group} resource group')

        cmd = f'{_get_path()} network public-ip show --resource-group {resource_group} --name ingressPublicIPAddress'
        ip_info = json.loads(subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True).stdout)
    except subprocess.CalledProcessError as cpe:
        print_debug((
            f'Error getting Ingress IP Address from {resource_group} resource group. '
            f'Output: {cpe.stdout}. Error: {cpe.stderr}.'
        ))
        spinner_ko_message(spinner, f'Error getting Ingress IP Address from {resource_group} resource group')
        raise AzureProviderException(f'Error getting Ingress IP Address from {resource_group} resource group')
    except json.JSONDecodeError:
        print_debug(f'Malformed response getting ingress IP Address info.')
        spinner_ko_message(spinner, "Malformed response getting ingress IP Address info")
        raise AzureProviderException("Malformed response getting ingress IP Address info")
    else:
        spinner_ok_message(spinner, "Found Ingress IP Address")
        return ip_info['ipAddress']
