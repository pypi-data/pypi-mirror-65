import subprocess
import json
from datetime import datetime, timedelta
import time

import click

from nalej_platformer.utils import spinner_ok_message, spinner_ko_message, print_debug
from nalej_platformer.exceptions import KubernetesProviderException


def _get_path():
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.kubectl_path


def validate_cluster_installation(kubeconfig, spinner, oneshot=False):
    start_time = datetime.now()
    results = []
    node_count = get_node_count(kubeconfig)
    for i in range(0, 36):
        elapsed_time = datetime.now() - start_time
        elapsed_time = elapsed_time - timedelta(microseconds=elapsed_time.microseconds)
        spinner.text = f'Validating cluster installation...[{elapsed_time}]'

        results = [
            _validate_replicable_resource(kubeconfig, "deployments", spinner),
            _validate_replicable_resource(kubeconfig, "statefulsets", spinner),
            _validate_daemonsets(kubeconfig, node_count, spinner),
            _validate_jobs(kubeconfig, spinner)
        ]

        if all(results):
            spinner_ok_message(spinner, "Cluster installation is valid")
            break

        if oneshot:
            break

        print_debug("Platform is not ready yet, waiting 30 seconds...")
        time.sleep(30)

    return all(results)


def get_node_count(kubeconfig):
    try:
        print_debug(f'Getting node count: {kubeconfig}')
        cmd = f"{_get_path()} --kubeconfig {kubeconfig} -nnalej get nodes -o json"
        get_nodes = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error getting node count from cluster. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        raise KubernetesProviderException(f"Error getting node count from cluster")
    else:
        try:
            output = json.loads(get_nodes.stdout)
        except json.JSONDecodeError as jexc:
            print_debug(f'Malformed response from Kubernetes. Output: {jexc}.')
            raise KubernetesProviderException("Malformed response from Kubernetes")
        else:
            return len(output.get('items', []))


def _validate_replicable_resource(kubeconfig, resource_kind, spinner):
    try:
        print_debug(f'Validating all {resource_kind} are ready: {kubeconfig}')
        cmd = f"{_get_path()} --kubeconfig {kubeconfig} -nnalej get {resource_kind} -o json"
        get_resource = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error getting {resource_kind} from cluster. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, f"Error getting {resource_kind} from cluster")
        raise KubernetesProviderException(f"Error getting {resource_kind} from cluster")
    else:
        try:
            output = json.loads(get_resource.stdout)
        except json.JSONDecodeError as jexc:
            print_debug(f'Malformed response from Kubernetes. Output: {jexc}.')
            spinner_ko_message(spinner, "Malformed response from Kubernetes")
            raise KubernetesProviderException("Malformed response from Kubernetes")
        else:
            for resource in output['items']:
                replicas = int(resource['spec']['replicas'])
                ready_output = resource['status'].get('readyReplicas', None)
                if ready_output in ["", None]:
                    ready_output = 0
                ready_replicas = int(ready_output)
                print_debug((
                    f"{resource_kind.capitalize()} {resource['metadata']['name']}, "
                    f"found {replicas} replicas which {ready_replicas} are ready")
                )
                if replicas != ready_replicas:
                    return False
            print_debug(f"All {resource_kind} are ready")
            return True


def _validate_daemonsets(kubeconfig, node_count, spinner):
    try:
        print_debug(f'Validating all daemonsets are ready: {kubeconfig}')
        cmd = f"{_get_path()} --kubeconfig {kubeconfig} -nnalej get daemonsets -o json"
        get_daemonsets = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error getting daemonsets from cluster. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, f"Error getting daemonsets from cluster")
        raise KubernetesProviderException(f"Error getting daemonsets from cluster")
    else:
        try:
            output = json.loads(get_daemonsets.stdout)
        except json.JSONDecodeError as jexc:
            print_debug(f'Malformed response from Kubernetes. Output: {jexc}.')
            spinner_ko_message(spinner, "Malformed response from Kubernetes")
            raise KubernetesProviderException("Malformed response from Kubernetes")
        else:
            for daemonset in output['items']:
                ready_output = daemonset['status'].get('numberReady', None)
                if ready_output in ["", None]:
                    ready_output = 0
                ready_output = int(ready_output)
                print_debug((
                    f"Daemonset {daemonset['metadata']['name']}, "
                    f"expected {node_count} replicas which {ready_output} are ready")
                )
                if node_count != ready_output:
                    return False
            print_debug(f"All daemonsets are ready")
            return True


def _validate_jobs(kubeconfig, spinner):
    try:
        print_debug(f'Validating all jobs are complete: {kubeconfig}')
        cmd = f"{_get_path()} --kubeconfig {kubeconfig} -nnalej get jobs -o json"
        get_jobs = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error getting jobs from cluster. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, f"Error getting jobs from cluster")
        raise KubernetesProviderException(f"Error getting jobs from cluster")
    else:
        try:
            output = json.loads(get_jobs.stdout)
        except json.JSONDecodeError as jexc:
            print_debug(f'Malformed response from Kubernetes. Output: {jexc}.')
            spinner_ko_message(spinner, "Malformed response from Kubernetes")
            raise KubernetesProviderException("Malformed response from Kubernetes")
        else:
            for job in output['items']:
                succeeded = job['status'].get('succeeded', 0)
                if succeeded in ["", None, 0] or int(succeeded) <= 0:
                    print_debug(f"Job {job['metadata']['name']} has no succeeded jobs")
                    return False
            print_debug("Every job has succeeded")
            return True
