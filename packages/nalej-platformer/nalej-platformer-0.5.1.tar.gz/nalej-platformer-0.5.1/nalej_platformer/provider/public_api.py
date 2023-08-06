import subprocess

import click

from nalej_platformer.utils import spinner_ok_message, spinner_ko_message, print_debug, parse_json_output
from nalej_platformer.exceptions import PublicApiProviderException


def _get_path():
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.public_api_path


def _get_ca_path(environment):
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.get_ca_path(environment)


def login(login_address, environment, user, spinner):
    print_debug(f"Logging into the platform with user {user.email}")
    try:
        cmd = (
            f'{_get_path()} login --loginAddress={login_address} --loginPort=443 --email={user.email} '
            f'--password={user.password} --cacert={_get_ca_path(environment)}'
        )
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(
            f'Error logging to the platform with user {user.email}. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, f"Error logging to the platform with user {user.email}")
        raise PublicApiProviderException(f"Error logging to the platform with user {user.email}")
    else:
        print_debug("Logged in to the platform successfully")
        spinner_ok_message(spinner, "Logged in to the platform successfully")
        return True


def provision_and_install(
        sp_path, vm_size, region, name, resource_group, dns_zone, kubernetes_version,
        num_nodes, environment, api_address, organization_id, spinner):
    print_debug(f"Launching provision and install application cluster {name}")
    try:
        cmd = (
            f'{_get_path()} cluster provision-and-install --nalejAddress={api_address} --clusterName={name} '
            f'--azureDnsZoneName={dns_zone} --azureResourceGroup={resource_group} --numNodes={num_nodes} '
            f'--nodeType={vm_size} --zone="{region}" --kubernetesVersion={kubernetes_version} '
            f'--azureCredentialsPath={sp_path} --organizationId={organization_id} --targetPlatform=AZURE '
            f'--cacert={_get_ca_path(environment)} --clusterType=KUBERNETES'
        )
        if environment == "PRODUCTION":
            cmd += ' --isProductionCluster'

        pai_output = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug((
            f'Error launching provision and install application cluster {name}. '
            f'Output: {cpe.stdout}. Error: {cpe.stderr}.'
        ))
        spinner_ko_message(spinner, f"Error launching provision and install application cluster {name}")
        raise PublicApiProviderException(f"Error launching provision and install application cluster {name}")
    else:
        print_debug("Launched provision and install process succesfully")
        json_output = parse_json_output(pai_output.stdout)[0]
        cluster_id = json_output.get("cluster_id", None)
        print_debug(f'Application cluster ID: {cluster_id}')
        spinner_ok_message(spinner, "Launched provision and install process succesfully")
        return json_output


def get_cluster_state(api_address, environment, cluster_id, spinner):
    print_debug(f'Validating that cluster {cluster_id} is installed')
    try:
        cmd = (
            f'{_get_path()} cluster info --nalejAddress={api_address} --cacert={_get_ca_path(environment)} '
            f'{cluster_id}'
        )

        cluster_info = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error validating cluster {cluster_id} is installed. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, f"Error validating cluster {cluster_id} is installed")
        raise PublicApiProviderException(f"Error validating cluster {cluster_id} is installed")
    else:
        cluster_json = parse_json_output(cluster_info.stdout)[0]
        state_name = cluster_json.get("state_name", None)
        if state_name is None:
            print_debug('Malformed response getting cluster info')
            spinner_ko_message(spinner, 'Malformed response getting cluster info')
            raise PublicApiProviderException('Malformed response getting cluster info')
        else:
            return state_name
