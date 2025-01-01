from ansible.errors import AnsibleFilterError


class PodmanConstruct:
    def __init__(self, construct_name) -> None:
        self.construct_name = construct_name


class PodmanConstructVolume(PodmanConstruct):
    def __init__(
        self,
        construct_name,
        src,
        dest: str | None = None,
        service_name=None,
        options=None,
        owner=None,
        group=None,
        mode=None,
    ) -> None:
        super().__init__(construct_name)
        self.src: str = src
        self.used_by: dict = {}

        self.owner: str | None = owner if owner else None
        self.group: str | None = group if group else None
        self.mode: str | None = mode if mode else None

        self.volume_type: str = self.determine_type()

        self.src_name_full: str
        self.src_quadlet_name: str | None = None

        if self.volume_type == "named":
            self.src_name_full = "-".join([self.construct_name, self.src])
            self.src_quadlet_name = ".".join([self.src_name_full, "volume"])
        elif self.volume_type == "bind":
            self.src_name_full = self.src

        if service_name and dest:
            self.add_used_by(service_name, dest, options)

        self.syntax_checks()

    def determine_type(self) -> str:
        if self.src[0] in [".", "/"]:
            return "bind"
        else:
            return "named"

    def is_volume_used_by_service(self, service_name) -> bool:
        if service_name in self.used_by.keys():
            return True
        else:
            return False

    def add_used_by(self, service_name, dest, options=None) -> None:
        if self.is_volume_used_by_service(service_name):
            msg = f"Service '{service_name}' already present in self.used_by."
            msg += " This could mean that there is a duplicate in the volumes list."
            msg += f" Current data: {self.to_dict()}"
            raise AnsibleFilterError(msg)
        else:
            self.used_by[service_name] = {"dest": dest, "options": options}

    def syntax_checks(self) -> None:
        self.check_permissions()

    def check_permissions(self) -> None:
        if self.volume_type == "named":
            if self.owner or self.group or self.mode:
                msg = "The fields 'owner', 'group' and 'mode' are only allowed"
                msg += " on bind volumes, but not for named volumes."
                msg += f" Current data: {self.to_dict()}"
                raise AnsibleFilterError(msg)

    def to_dict_global_bind(self) -> dict:
        return {
            "src": self.src,
            "owner": self.owner,
            "group": self.group,
            "mode": self.mode,
            "used_by": self.used_by,
        }

    def to_dict_global_named(self) -> dict:
        return {
            "src_original": self.src,
            "src_name_full": self.src_name_full,
            "src_quadlet_name": self.src_quadlet_name,
            "used_by": self.used_by,
        }

    def to_string_service(self, service_name) -> str:
        if self.is_volume_used_by_service(service_name):
            volume_join = [self.src_name_full]
            volume_join.append(self.used_by[service_name]["dest"])

            if self.used_by[service_name]["options"]:
                volume_join.append(self.used_by[service_name]["options"])
            print(volume_join)
            return ":".join(volume_join)
        else:
            msg = f"Volume {self.src} is not in use by {service_name}!"
            msg += f" Current data: {self.to_dict()}"
            raise AnsibleFilterError(msg)

    def to_dict(self) -> dict:
        return {
            "construct_name": self.construct_name,
            "src": self.src,
            "used_by": self.used_by,
            "owner": self.owner,
            "group": self.group,
            "mode": self.mode,
            "volume_type": self.volume_type,
            "src_name_full": self.src_name_full,
            "src_quadlet_name": self.src_quadlet_name,
        }


class PodmanConstructVolumes(PodmanConstruct):
    def __init__(self, construct_name) -> None:
        super().__init__(construct_name)
        self.volumes: list[PodmanConstructVolume] = []

    def add_volume(
        self,
        src,
        dest=None,
        service_name=None,
        options=None,
        owner=None,
        group=None,
        mode=None,
    ) -> None:
        volume: PodmanConstructVolume | None = self.search_volume(src)
        if not volume:
            volume = PodmanConstructVolume(
                self.construct_name,
                src,
                dest=dest,
                service_name=service_name,
                options=options,
                owner=owner,
                group=group,
                mode=mode,
            )
            self.volumes.append(volume)
        elif volume and dest:
            volume.add_used_by(service_name, dest, options=options)

    def search_volume(self, src) -> PodmanConstructVolume | None:
        for v in self.volumes:
            if src == v.src:
                return v
        return None

    def get_named_volumes_for_global(self) -> list[dict]:
        named_volumes: list[dict] = []
        for v in self.volumes:
            if v.volume_type == "named":
                named_volumes.append(v.to_dict_global_named())
        return named_volumes

    def get_bind_volumes_for_global(self) -> list[dict]:
        bind_volumes: list[dict] = []
        for v in self.volumes:
            if v.volume_type == "bind":
                bind_volumes.append(v.to_dict_global_bind())
        return bind_volumes

    def get_volumes_for_service(self, service_name) -> list[str]:
        service_volumes: list[str] = []
        for v in self.volumes:
            if (
                v.is_volume_used_by_service(service_name)
                and v.used_by[service_name]["dest"]
            ):
                service_volumes.append(v.to_string_service(service_name))
        return service_volumes


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
        self.volumes: PodmanConstructVolumes = PodmanConstructVolumes(construct_name)

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
            "named_volumes": self.volumes.get_named_volumes_for_global(),
            "bind_volumes": self.volumes.get_bind_volumes_for_global(),
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
        if "volumes" in self.construct.keys():
            for v in self.construct["volumes"]:
                self.volumes.add_volume(
                    v["src"],
                    owner=v["owner"] if "owner" in v.keys() else None,
                    group=v["group"] if "group" in v.keys() else None,
                    mode=v["mode"] if "mode" in v.keys() else None,
                )

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
        service_dict["volumes"] = self.parse_service_volumes(service)

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

    def parse_service_volumes(self, service):
        if "volumes" in service.keys():
            for v in service["volumes"]:
                self.volumes.add_volume(
                    v["src"],
                    dest=v["dest"],
                    service_name=service["name"],
                    options=v["options"] if "options" in v.keys() else None,
                    owner=v["owner"] if "owner" in v.keys() else None,
                    group=v["group"] if "group" in v.keys() else None,
                    mode=v["mode"] if "mode" in v.keys() else None,
                )
            return self.volumes.get_volumes_for_service(service["name"])


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
