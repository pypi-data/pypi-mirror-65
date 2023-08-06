import subprocess
import time
import json
from datetime import datetime, timedelta

import click

from nalej_platformer.utils import spinner_ok_message, spinner_ko_message, print_debug, parse_json_output
from nalej_platformer.exceptions import SignupProviderException


def _get_path():
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.signup_path


def _get_ca_path(environment):
    ctx = click.get_current_context()
    config = ctx.obj['CONFIGURATION']
    return config.get_ca_path(environment)


def wait_for_signup(signup_address, environment, spinner):
    start_time = datetime.now()
    print_debug("Waiting for signup to be ready")
    for i in range(0, 36):
        elapsed_time = datetime.now() - start_time
        elapsed_time = elapsed_time - timedelta(microseconds=elapsed_time.microseconds)
        spinner.text = f'Waiting for signup to be ready...[{elapsed_time}]'
        try:
            cmd = f'{_get_path()} list --signupAddress={signup_address}:443 --caPath={_get_ca_path(environment)}'
            subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            print_debug("Signup is not ready yet, waiting 5 seconds")
            time.sleep(5)
            continue
        else:
            print_debug("Signup is ready")
            spinner_ok_message(spinner, "Signup component is ready")
            return True
    print_debug("Timeout waiting for signup to be ready")
    spinner_ko_message(spinner, "Timeout waiting for signup to be ready")
    raise SignupProviderException("Timeout waiting for signup to be ready")


def create_organization(signup_address, organization, environment, spinner):
    print_debug(f'Creating organization {organization.name}')
    owner = organization.owner
    nalej_admin = organization.nalej_admin
    try:
        cmd = (
            f'{_get_path()} signup --signupAddress={signup_address}:443 --orgName={organization.name} '
            f'--ownerEmail={owner.email} --ownerName={owner.email} --ownerPassword={owner.password} '
            f'--nalejAdminEmail={nalej_admin.email} --nalejAdminName={nalej_admin.email} '
            f'--nalejAdminPassword={nalej_admin.password} --caPath={_get_ca_path(environment)}'
        )
        create_org = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as cpe:
        print_debug(f'Error creating organization {organization.name}. Output: {cpe.stdout}. Error: {cpe.stderr}.')
        spinner_ko_message(spinner, f"Error creating organization {organization.name}")
        raise SignupProviderException(f"Error creating organization {organization.name}")
    else:
        try:
            parsed_json = parse_json_output(create_org.stderr)
        except json.JSONDecodeError:
            print_debug(f'Malformed response from signup.')
            spinner_ko_message(spinner, f"Malformed response from organization")
            raise SignupProviderException(f"Malformed response from signup")
        else:
            if len(parsed_json) < 1:
                print_debug(f'Malformed response from signup. Output: {parsed_json}.')
                spinner_ko_message(spinner, f"Malformed response from organization")
                raise SignupProviderException(f"Malformed response from signup")
            signup_data = parsed_json[-1]
            organization_id = signup_data.get("organizationID", None)
            if organization_id is None:
                print_debug(f'Organization ID not found in response. Output: {parsed_json}.')
                spinner_ko_message(spinner, f"Organization ID not found in response")
                raise SignupProviderException(f"Organization ID not found in response")
            else:
                print_debug(f'Organization {organization.name} created with {organization_id}')
                spinner_ok_message(spinner, f"Organization {organization.name} created successfully")
                return organization_id


def organization_exists(signup_address, organization, environment):
    if organization.organization_id is None:
        return False

    print_debug(f'Checking if organization {organization.name} exists')
    try:
        cmd = (
            f'{_get_path()} info  --signupAddress={signup_address}:443 '
            f'--organizationID={organization.organization_id} --caPath={_get_ca_path(environment)}'
        )
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return False
    else:
        return True
