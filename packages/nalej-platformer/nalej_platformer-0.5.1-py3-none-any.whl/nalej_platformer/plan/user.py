import re

from nalej_platformer.exceptions import OrganizationPlanException
from nalej_platformer.utils import print_debug, spinner_ko_message, spinner_ok_message, get_indentation, get_spinner


class OrganizationUserPlan:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def info(self, indentation=3):
        indent = get_indentation(indentation)
        info_template = (
            f"{indent}Name: {self.name}\n"
            f"{indent}Email: {self.email}"
        )
        return info_template

    @classmethod
    def read_plan(cls, plan_data, user_type):
        print_debug(
            f"Reading {user_type} user block. Raw data: {plan_data}")
        if plan_data is None:
            cap_user_type = user_type.capitalize()
            raise OrganizationPlanException(f"{cap_user_type} user block is required")

        with get_spinner(f"Checking {user_type} user block...") as spinner:
            name = cls._validate_name(plan_data.get("name", None), user_type, spinner)
            email = cls._validate_email(plan_data.get("email", None), user_type, spinner)
            password = cls._validate_password(plan_data.get("password", None), user_type, spinner)

        return cls(name, email, password)

    @classmethod
    def _validate_name(cls, name, user_type, spinner):
        cap_user_type = user_type.capitalize()
        if name in ["", None]:
            spinner_ko_message(spinner, f"{cap_user_type} user name is empty")
            raise OrganizationPlanException(f"{cap_user_type} user name is empty")

        spinner_ok_message(spinner, f"{cap_user_type} user name is valid")
        return name

    @classmethod
    def _validate_email(cls, email, user_type, spinner):
        cap_user_type = user_type.capitalize()
        if email in ["", None]:
            spinner_ko_message(spinner, f"{cap_user_type} user email is empty")
            raise OrganizationPlanException(f"{cap_user_type} user email is empty")

        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(email_regex, email) is None:
            spinner_ko_message(spinner, f"{cap_user_type} user email is not valid")
            raise OrganizationPlanException(f"{cap_user_type} user email is not valid")

        spinner_ok_message(spinner, f"{cap_user_type} user email is valid")
        return email

    @classmethod
    def _validate_password(cls, password, user_type, spinner):
        cap_user_type = user_type.capitalize()
        if password in ["", None]:
            spinner_ko_message(spinner, f"{cap_user_type} user password is empty")
            raise OrganizationPlanException(f"{cap_user_type} user password is empty")
        if len(password) < 6:
            spinner_ko_message(spinner, f"{cap_user_type} user password doesn't match the password policy")
            raise OrganizationPlanException(f"{cap_user_type} user password needs at least 6 characters")

        spinner_ok_message(spinner, f"{cap_user_type} user password is valid")
        return password

    def dict_for_yaml(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
