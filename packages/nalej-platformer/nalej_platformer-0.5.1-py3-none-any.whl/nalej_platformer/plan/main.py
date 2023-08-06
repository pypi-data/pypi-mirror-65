import yaml
import click

from nalej_platformer.utils import print_debug, get_indentation
from nalej_platformer.plan.management import ManagementPlan
from nalej_platformer.plan.application import ApplicationPlan
from nalej_platformer.plan.organization import OrganizationPlan
from nalej_platformer.exceptions import PlanException


class Plan:
    def __init__(self, plan_data):
        self.management = ManagementPlan.read_plan(plan_data.get('management', None))
        self.organization_list = OrganizationPlan.read_list(plan_data.get('organization', None))
        self.application_list = ApplicationPlan.read_list(plan_data.get('application', None), self.organization_list)

    def info(self, indentation=0):
        indent = get_indentation(indentation)
        management = self.management.info(indentation=indentation + 1)
        info_template = f"{indent}Management:\n{management}"

        info_template += f"{indent}Application clusters:\n"
        for application in self.application_list:
            info_template += application.info(indentation=indentation + 1)

        info_template += f"{indent}Organizations:\n"
        for organization in self.organization_list:
            info_template += organization.info(indentation=indentation + 1)

        return info_template

    def apply(self):
        print_debug("Applying plan")

        self.management.apply()
        self.organization_list = OrganizationPlan.apply_list(self.organization_list, self.management)
        self.application_list = ApplicationPlan.apply_list(
            self.application_list, self.organization_list, self.management)

    @classmethod
    def read_plan(cls, plan_path):
        """Reads the plan file"""

        print_debug(f"Reading plan file: {plan_path}")

        plan = None
        with open(plan_path) as plan_file:
            try:
                plan_dict = yaml.load(plan_file, Loader=yaml.FullLoader)
            except yaml.YAMLError as yexc:
                raise PlanException(f"Error reading YAML plan file. Details: {yexc}")
            else:
                click.echo("Reading and validating plan")
                plan = cls(plan_dict)

        return plan
