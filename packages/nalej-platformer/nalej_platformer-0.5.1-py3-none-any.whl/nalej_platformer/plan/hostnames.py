from nalej_platformer.exceptions import HostnamesPlanException
from nalej_platformer.utils import print_debug, get_indentation


class HostnamesPlan:
    def __init__(self, web, api, login, signup):
        self.web = web
        self.api = api
        self.login = login
        self.signup = signup

    def info(self, indentation=2):
        indent = get_indentation(indentation)
        info_template = (
            f"{indent}Web: {self.web}\n"
            f"{indent}API: {self.api}\n"
            f"{indent}Login: {self.login}\n"
            f"{indent}SignUp: {self.signup}\n"
        )

        return info_template

    @classmethod
    def read_plan(cls, plan_data):
        print_debug(f"Reading hostnames plan block. Raw data: {plan_data}")
        if plan_data is None:
            return None

        web = plan_data.get("web", None)
        api = plan_data.get("api", None)
        login = plan_data.get("login", None)
        signup = plan_data.get("signup", None)

        if web is None:
            raise HostnamesPlanException("Web hostname not found in plan")
        if api is None:
            raise HostnamesPlanException("API hostname not found in plan")
        if login is None:
            raise HostnamesPlanException("Login hostname not found in plan")
        if signup is None:
            raise HostnamesPlanException("SignUp hostname not found in plan")

        return cls(web, api, login, signup)

    def dict_for_yaml(self):
        return {
            "web": self.web,
            "api": self.api,
            "login": self.login,
            "signup": self.signup
        }
