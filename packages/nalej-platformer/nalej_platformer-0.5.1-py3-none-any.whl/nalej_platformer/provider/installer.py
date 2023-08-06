import subprocess
from datetime import datetime, timedelta

import click

from nalej_platformer.utils import spinner_ok_message, spinner_ko_message, print_debug


def _get_path():
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.installer_path


def _get_assets_path():
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.installer_resources


def _get_binaries_path():
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.installer_binaries

def _get_istio_path():
    return f'{_get_binaries_path()}/istio/bin'


def install_management_cluster(
        kubeconfig, name, environment, dns_zone, ingress_ip, dns_ip, coredns_ip, vpnserver_ip, spinner):

    start_time = datetime.now()
    cmd = (
        f'{_get_path()} install management --debug --binaryPath {_get_binaries_path()} '
        f'--componentsPath {_get_assets_path()} --managementClusterPublicHost={name}.{dns_zone} '
        f'--dnsClusterPublicHost=dns.{name}.{dns_zone} --targetPlatform=AZURE --useStaticIPAddresses '
        f'--ipAddressIngress={ingress_ip} --ipAddressDNS={dns_ip} --ipAddressCoreDNS={coredns_ip} '
        f'--ipAddressVPNServer={vpnserver_ip} --kubeConfigPath={kubeconfig} --targetEnvironment={environment} '
        f'--networkingMode=istio --istioPath={_get_istio_path()}'
    )

    install_mngt = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    result = False
    while True:
        if install_mngt.poll() is not None:
            break

        stderr_line = install_mngt.stderr.readline()
        debug_line = stderr_line.strip('\n')
        if debug_line != "":
            print_debug(f"Installer output: {debug_line}")
        elapsed_time = datetime.now() - start_time
        elapsed_time = elapsed_time - timedelta(microseconds=elapsed_time.microseconds)
        spinner.text = f'Installing management cluster...[{elapsed_time}]'

    install_mngt.stdout.close()
    install_mngt.stderr.close()
    exit_code = install_mngt.poll()
    if exit_code == 0:
        spinner_ok_message(spinner, "Management cluster installed successfully")
        result = True
    else:
        spinner_ko_message(spinner, "Error installing management cluster")

    return result
