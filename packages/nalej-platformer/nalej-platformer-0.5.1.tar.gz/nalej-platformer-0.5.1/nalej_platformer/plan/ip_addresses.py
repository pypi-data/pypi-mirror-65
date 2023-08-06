from nalej_platformer.exceptions import IPAddressesPlanException
from nalej_platformer.utils import print_debug, get_indentation


class IPAddressesPlan:
    def __init__(self, ingress, dns=None, coredns=None, vpn_server=None):
        self.ingress = ingress
        self.dns = dns
        self.coredns = coredns
        self.vpn_server = vpn_server

    def info(self, indentation=2):
        indent = get_indentation(indentation)
        info_template = f"{indent}Ingress: {self.ingress}\n"

        if self.dns is not None:
            info_template += f"{indent}DNS: {self.dns}\n"
        if self.coredns is not None:
            info_template += f"{indent}CoreDNS: {self.coredns}\n"
        if self.vpn_server is not None:
            info_template += f"{indent}VPN Server: {self.vpn_server}\n"

        return info_template

    @classmethod
    def read_plan(cls, plan_data):
        print_debug(f"Reading IP Address plan block. Raw data: {plan_data}")
        if plan_data is None:
            return None

        ingress = plan_data.get("ingress", None)
        dns = plan_data.get("dns", None)
        coredns = plan_data.get("coredns", None)
        vpn_server = plan_data.get("vpnServer", None)

        if ingress is None:
            raise IPAddressesPlanException("Ingress IP Address not found in plan")

        return cls(ingress, dns, coredns, vpn_server)

    def dict_for_yaml(self):
        yaml_data = {
            "ingress": self.ingress
        }

        if self.dns is not None:
            yaml_data["dns"] = self.dns
        if self.coredns is not None:
            yaml_data["coredns"] = self.coredns
        if self.vpn_server is not None:
            yaml_data["vpnServer"] = self.vpn_server

        return yaml_data
