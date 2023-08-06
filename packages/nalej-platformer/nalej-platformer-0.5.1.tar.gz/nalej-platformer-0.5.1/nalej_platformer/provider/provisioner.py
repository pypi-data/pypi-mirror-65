from datetime import datetime, timedelta
from tempfile import gettempdir
import subprocess
import json

import click

from nalej_platformer.utils import spinner_ok_message, spinner_ko_message, print_debug
from nalej_platformer.exceptions import ProvisionerProviderException


def _get_path():
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.provisioner_path


def _get_resources_path():
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.provisioner_resources


def provision_management_cluster(
        sp_path, vm_size, region, name, resource_group, dns_zone, kubernetes_version,
        num_nodes, environment, spinner):

    start_time = datetime.now()
    cmd = (
        f'{_get_path()} provision --debug --azureCredentialsPath={sp_path} --platform AZURE --nodeType {vm_size} '
        f'--zone "{region}" --name {name} --resourceGroup {resource_group} --tempPath={gettempdir()} '
        f'--resourcesPath={_get_resources_path()} --dnsZoneName={dns_zone} --kubernetesVersion={kubernetes_version} '
        f'--numNodes={num_nodes}'
    )
    if environment == "PRODUCTION":
        cmd += ' --isProduction'

    provision_mngt = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    result_data = dict()
    while True:
        if provision_mngt.poll() is not None:
            break

        stderr_line = provision_mngt.stderr.readline()
        debug_line = stderr_line.strip('\n')
        if debug_line != "":
            print_debug(f"Provision output: {debug_line}")
        elapsed_time = datetime.now() - start_time
        elapsed_time = elapsed_time - timedelta(microseconds=elapsed_time.microseconds)
        spinner.text = f'Provisioning management cluster...[{elapsed_time}]'

        try:
            line_json = json.loads(stderr_line)
        except json.JSONDecodeError:
            pass
        else:
            line_type = line_json.get("type", None)
            line_progress = line_json.get("progress", None)
            if line_type == "Provision" and line_progress == "Finished":
                result_data = line_json

    provision_mngt.stdout.close()
    provision_mngt.stderr.close()
    exit_code = provision_mngt.poll()
    if exit_code == 0:
        spinner_ok_message(spinner, "Management cluster provisioned successfully")
    else:
        spinner_ko_message(spinner, "Error provisioning management cluster")
        raise ProvisionerProviderException("Error provisioning management cluster")

    return result_data
