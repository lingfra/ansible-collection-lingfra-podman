from ansible.errors import AnsibleFilterError


class PodmanConstructProcessor:
    # arguments for services, which should be copied unmodified
    SERVICE_COPY_ARGS = [
        "env",
        "hostname",
        "image",
        "map_user",
        "publish",
        "pull",
        "restart",
        "user",
        "userns",
        "volumes",
    ]

    def __init__(self, construct, construct_name) -> None:
        self.construct = construct
        self.name = construct_name

        # init top level objects
        self.networks: list = []
        self.pod: str | None = None
        self.secrets: list = []
        self.services: list = []
        self.volumes: list = []

        # helper variables
        self.service_names: list = []
        if self.construct["services"]:
            self.service_names = [s["name"] for s in self.construct["services"]]
        else:
            self.service_names = []

    def process(self):
        self.top_level_args()
        self.parse_services()

        output = {
            "name": self.name,
            "networks": self.networks,
            "pod": self.pod,
            "secrets": self.secrets,
            "services": self.services,
            "volumes": self.volumes,
        }

        return output

    # ---------- Top Level Args (without 'services') ----------

    def top_level_args(self):
        self.parse_pod()
        self.parse_networks()
        self.parse_secrets()
        self.parse_volumes()

    def parse_pod(self):
        if "pod" in self.construct.keys():
            self.pod = f"{self.name}.pod"

    def parse_networks(self):
        if "networks" in self.construct.keys():
            for network in self.construct["networks"]:
                self.networks.append(self.parse_network(network))

    def parse_network(self, network):
        if network["driver"]:
            network_driver = network["driver"]
        else:
            network_driver = "bridge"

        if network_driver == "external":
            network_name = network["name"]
        else:
            network_name = f"{self.name}-{network['name']}.network"

        return {
            "name": network_name,
            "driver": network_driver,
        }

    def parse_secrets(self):
        if "secrets" in self.construct.keys():
            if not isinstance(self.construct["secrets"], dict):
                raise AnsibleFilterError(
                    f"construct.secrets need to be a dict, got {type(self.construct['secrets'])}"
                )

            for k, v in self.construct["secrets"].items():
                if not isinstance(self.construct["secrets"][k], str):
                    raise AnsibleFilterError(
                        f"secrets need to be a str, got {type(self.construct['secrets'])}"
                    )
                self.secrets.append(
                    {
                        "-".join([self.name, k]): v,
                    }
                )

    def parse_volumes(self):
        pass

    # ---------- Services ----------

    def parse_services(self):
        if "services" in self.construct.keys():
            for service in self.construct["services"]:
                if not "name" in service.keys():
                    raise AnsibleFilterError(f"service.name need to be defined")
                self.services.append(self.parse_service(service))
        else:
            raise AnsibleFilterError(f"service need to be defined")

    def parse_service(self, service):

        service_name = "-".join([self.name, service["name"]])

        service_dict = {
            "name": service_name,
            "depends_on": str | None,
            "networks": list | None,
        }

        # process easy args
        for arg in self.SERVICE_COPY_ARGS:
            if arg in service.keys():
                service_dict[arg] = service[arg]
            else:
                service_dict[arg] = None

        service_dict["depends_on"] = self.parse_service_depends_on(service)
        service_dict["networks"] = self.parse_service_networks(service)
        service_dict["pod"] = self.parse_service_pod()

        return service_dict

    def parse_service_depends_on(self, service):
        depends_on: list | None = None
        if "depends_on" in service.keys():
            for dep in service["depends_on"]:
                if not dep in self.service_names:
                    raise AnsibleFilterError(f"{dep} is not a defined service.")
            depends_on = service["depends_on"]
        return depends_on

    def parse_service_networks(self, service):
        service_networks: list = []
        if "network" in service.keys():
            for network in service["network"]:
                # TODO this may be problematic. Need better check if the
                # network is defined in the top level networks key.
                if ".network" in network and network not in self.networks:
                    self.networks.append(network)
                service_networks.append(network)
        else:
            if not self.pod:
                network = f"{self.name}.network"
                if not network in self.networks:
                    self.networks.append(network)
        return service_networks

    def parse_service_pod(self):
        if self.pod:
            return self.pod
        else:
            return None


def process_construct_name(construct):
    if not "name" in construct.keys():
        raise AnsibleFilterError(f"construct.name need to be defined")
    if not isinstance(construct["name"], str):
        raise AnsibleFilterError(
            f"construct.name need to be string, got {type(construct['name'])}"
        )

    return construct["name"]


def process_construct(construct):
    if not isinstance(construct, dict):
        error_msg = "Each list item in the input data need to be of"
        error_msg += f" type dict, got {type(construct)}"
        raise AnsibleFilterError(error_msg)

    construct_name = process_construct_name(construct)
    construct_processor = PodmanConstructProcessor(construct, construct_name)
    return construct_processor.process()


def process_construct_list(construct_list):
    """
    Process list of nested podman_construct definitions, which are nested
    dictionaries.

    :param data: List of dictionaries
    :return: List of processed dictionaries
    """
    if not isinstance(construct_list, list):
        raise AnsibleFilterError("Input data must be a list")

    result = []
    for construct in construct_list:
        result.append(process_construct(construct))

    return result


# Register the filter
class FilterModule(object):
    def filters(self):
        return {
            "process_construct": process_construct,
            "process_construct_list": process_construct_list,
        }
