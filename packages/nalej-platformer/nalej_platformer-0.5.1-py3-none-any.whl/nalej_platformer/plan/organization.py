import yaml
import click

from nalej_platformer.plan.user import OrganizationUserPlan
from nalej_platformer.exceptions import OrganizationPlanException, SignupProviderException
from nalej_platformer.utils import print_debug, spinner_ko_message, spinner_ok_message, get_indentation, get_spinner
from nalej_platformer.provider.signup import wait_for_signup, create_organization, organization_exists


class OrganizationPlan:
    def __init__(self, name, owner, nalej_admin, organization_id=None):
        self.name = name
        self.owner = owner
        self.nalej_admin = nalej_admin
        self.organization_id = organization_id

    def info(self, only_name=False, indentation=2):
        if only_name:
            return self.name
        else:
            indent = get_indentation(indentation)
            owner = self.owner.info(indentation=indentation + 1)
            nalej_admin = self.nalej_admin.info(indentation=indentation + 1)
            info_template = (
                f"{indent}Name: {self.name}\n"
                f"{indent}Users:\n"
                f"{indent}- Owner:\n{owner}\n"
                f"{indent}- Nalej Admin\n{nalej_admin}"
            )
            if self.organization_id is not None:
                id_info = f"{indent}ID: {self.organization_id}\n"
                info_template = id_info + info_template

            return info_template

    def apply(self, management):
        signup_address = management.hostnames.signup
        environment = management.environment

        with get_spinner(f'Creating organization {self.name}...') as spinner:
            if organization_exists(signup_address, self, environment):
                spinner_ok_message(spinner, f"Organization {self.name} already exists, skipping")
            else:
                try:
                    self.organization_id = create_organization(signup_address, self, environment, spinner)
                except SignupProviderException as sexc:
                    raise OrganizationPlanException(sexc)

        return self

    @classmethod
    def read_list(cls, plan_list=[]):
        org_list = []
        if plan_list is None:
            return org_list

        click.echo("ORGANIZATIONS: ")
        for plan in plan_list:
            name = plan.get("name", "<NO NAME>")
            click.echo(f"Organization {name}")
            org_list.append(cls.read_plan(plan))
            click.echo('\n')
        return org_list

    @classmethod
    def read_plan(cls, plan_data):
        print_debug(f"Reading organization configuration block. Raw data: {plan_data}")
        if plan_data is None:
            raise OrganizationPlanException("Organization configuration block is required")

        name = cls._validate_name(plan_data.get("name", None))
        users = plan_data.get("users", None)
        organization_id = plan_data.get("organizationID", None)

        if users is None:
            raise OrganizationPlanException("Users block is required")

        owner = OrganizationUserPlan.read_plan(users.get("owner", None), "owner")
        nalej_admin = OrganizationUserPlan.read_plan(users.get("nalejAdmin", None), "nalej admin")

        return cls(name, owner, nalej_admin, organization_id)

    @classmethod
    def apply_list(cls, organization_list, management):
        print_debug("Applying organization block")
        with get_spinner("Waiting for signup to be ready...") as spinner:
            signup_address = management.hostnames.signup
            environment = management.environment
            try:
                wait_for_signup(signup_address, environment, spinner)
            except SignupProviderException as sexc:
                raise OrganizationPlanException(sexc)

        applied_list = [org.apply(management) for org in organization_list]
        cls._update_plan_file(applied_list)
        return applied_list

    @classmethod
    def _validate_name(cls, name):
        with get_spinner("Checking organization name...") as spinner:
            if name in ["", None]:
                spinner_ko_message(spinner, "Organization name is empty")
                raise OrganizationPlanException("Organization name must not be empty")

            spinner_ok_message(spinner, "Organization name is valid")
            return name

    @staticmethod
    def _update_plan_file(organization_list):
        with get_spinner("Updating plan file...") as spinner:
            ctx = click.get_current_context()
            yaml_contents = {}
            with open(ctx.obj['PLAN_PATH'], "r") as plan_file:
                yaml_contents = yaml.load(plan_file, Loader=yaml.FullLoader)

            yaml_contents["organization"] = [org.dict_for_yaml() for org in organization_list]

            with open(ctx.obj['PLAN_PATH'], "w") as plan_file:
                plan_file.write(yaml.dump(yaml_contents, default_flow_style=False))

            spinner_ok_message(spinner, "Updated plan file")

    @staticmethod
    def find_by_name(org_list, name):
        for org in org_list:
            if org.name == name:
                return org

        return None

    def dict_for_yaml(self):
        data_dict = {
            "name": self.name,
            "users": {
                "nalejAdmin": self.nalej_admin.dict_for_yaml(),
                "owner": self.owner.dict_for_yaml()
            }
        }
        if self.organization_id is not None:
            data_dict["organizationID"] = self.organization_id
        return data_dict
