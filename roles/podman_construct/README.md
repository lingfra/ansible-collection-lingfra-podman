<!-- BEGIN_ANSIBLE_DOCS -->
# Ansible Role: lingfra.podman.podman_construct

Deploys the Podman components.

## Supported Platforms

Not specified.

## Entrypoint `main` - Main entry point for podman_construct role

This is the main entrypoint for the podman_construct role.
Creates the quadlet files for the containerized components.
Restarts a service after its container quadlet file changed, which also starts it on the first deployment.
Services are also restarted when one of their secrets changed, because Podman passes secrets to the container when it is created.

### Options for `main`

#### `podman_construct_list`

Type: list of dicts of `podman_construct_list` [options](#options-for-main--podman_construct_list), **required**.

Specifies the configuration for the containers to be created.

#### `podman_construct_network_list`

Type: list of dicts of `podman_construct_network_list` [options](#options-for-main--podman_construct_network_list), optional.

A list of servive unrelated networks to create. Most options are passthroughed to the ansible module [containers.podman.podman_network](https://docs.ansible.com/projects/ansible/latest/collections/containers/podman/podman_network_module.html). See its documentation for a reference to the options.

### Options for `main` > `podman_construct_list`

- **`name`** (Type: `str`, **required**).

  Name of the construct. Will be appended to all the created content from this role.

- `networks` (Type: list of dicts of `networks` [options](#options-for-main--podman_construct_list--networks), optional).

  Definition of networks, which should be available in this construct.

- `pod` (Type: `bool`, optional).

  Whether the services (containers) should be placed in a pod or not. If not placed in a pod, a network will be created.

- `secrets` (Type: `dict`, optional).

  A dictionary of secrets in the form `name: content`. It is necessary to define a secret here to use it in the service configuration.

- **`services`** (Type: list of dicts of `services` [options](#options-for-main--podman_construct_list--services), **required**).

  Dictionary containing the definition of services.

### Options for `main` > `podman_construct_list` > `networks`

- **`name`** (Type: `str`, **required**).

  Name of the network.

- `driver` (Type: `str`, optional).

  Optionally set the driver for the network. Refer to [**podman-network-create(1)**](https://docs.podman.io/en/latest/markdown/podman-network-create.1.html) for more information. The special value `external` indicates that the network should be assumed existing and not managed by Ansible. If unspecified falls back to `bridge`.

  _Choices:_ `bridge`, `macvlan`, `ipvlan`, `external`

### Options for `main` > `podman_construct_list` > `services`

- `auto_update` (Type: `str`, optional).

  Enables automatic updates of the container image with `podman auto-update`. `registry` pulls the image when the registry digest of the configured tag differs from the local one. It requires a fully qualified image name. `local` only restarts the container when the image in local storage was updated, e. g. by a manual pull or build. The updates run through the `podman-auto-update.timer`, which is managed by the `podman_auto_update` role. Combine it with `notify: healthy`, so `podman auto-update` rolls back to the previous image if the new container never becomes healthy. Refer to [**podman-auto-update(1)**](https://docs.podman.io/en/latest/markdown/podman-auto-update.1.html) for more information.

  _Choices:_ `registry`, `local`

- `cap_add` (Type: list of `str`, optional).

- `cap_drop` (Type: list of `str`, optional).

- `command` (Type: list of `str`, optional).

- `depends_on` (Type: `str`, optional).

  List of other containers or services this container should depend on.

- `entrypoint` (Type: `str`, optional).

- `env` (Type: `dict`, optional).

  Environment variables for the container.

- `healthcheck` (Type: dict of `healthcheck` [options](#options-for-main--podman_construct_list--services--healthcheck), optional).

  Health check configuration for the container. Refer to [**podman-run(1)**](https://docs.podman.io/en/latest/markdown/podman-run.1.html) for more information. The options correspond to the `--health-*` options of podman.

- `hostname` (Type: `str`, optional).

  Hostname of the container. Defaults to use the service name from the construct config.

- `image` (Type: `str`, optional).

  Fully qualified image name (FQIN) and version (tag or digest) of the container image.

- `labels` (Type: `dict`, optional).

  Labels to be added to the container

- `map_user` (Type: dict of `map_user` [options](#options-for-main--podman_construct_list--services--map_user), optional).

  A user to be mapped into the container user namespace. Using this option implies user namespace mode `auto`. This option is ignored when specifying `userns`.

- **`name`** (Type: `str`, **required**).

  Name of the service.

- `network` (Type: list of `str`, optional).

  Networks the container should be attached to.

- `notify` (Type: `str`, optional).

  How systemd startup notifications are handled for the container. `true` lets the application inside the container send the notification itself (requires sd_notify support). `healthy` delays the notification until the container is marked healthy (requires `healthcheck.cmd`). Defaults to `false`, where the service is started once the container runtime starts the container. Refer to [**podman-systemd.unit(5)**](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html) for more information.

  _Choices:_ `true`, `false`, `healthy`

- `pod` (Type: `str`, optional).

  Pod the container should be attached to.

- `pull` (Type: `str`, optional).

  Pull policy for the container.

- `publish` (Type: list of `str`, optional).

  List of port mappings for the container.

- `restart` (Type: `str`, optional).

  Policy for restarting the service on exit. Takes the systemd service options, see **[systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html#Restart=)**.

  _Choices:_ `always`, `no`, `on-abnormal`, `on-abort`, `on-failure`, `on-success`, `on-watchdog`

- `secrets` (Type: list of dicts of `secrets` [options](#options-for-main--podman_construct_list--services--secrets), optional).

  Secrets the container should get access to.

- `user` (Type: `str`, optional).

  User running the application inside the container. Either name or UID.

- `userns` (Type: `str`, optional).

  User namespace mode for the container. Overwrites `map_user` when configured.

- `volumes` (Type: list of dicts of `volumes` [options](#options-for-main--podman_construct_list--services--volumes), optional).

  Volumes for the container.

### Options for `main` > `podman_construct_list` > `services` > `healthcheck`

- `cmd` (Type: `str`, optional).

  Command to run inside the container to check its health. Use `none` to disable a health check defined in the container image.

- `interval` (Type: `str`, optional).

  Interval between health checks (e. g. `30s`). The value `disable` results in no automatic timer setup.

- `log_destination` (Type: `str`, optional).

  Destination of the health check logs. Either `local`, `events_logger` or a directory path.

- `max_log_count` (Type: `int`, optional).

  Maximum number of health check log entries to keep. `0` means infinite.

- `max_log_size` (Type: `int`, optional).

  Maximum character length of each health check log entry. `0` means infinite.

- `on_failure` (Type: `str`, optional).

  Action to take when the container is considered unhealthy.

  _Choices:_ `none`, `kill`, `restart`, `stop`

- `retries` (Type: `int`, optional).

  Number of consecutive failures before the container is considered unhealthy.

- `start_period` (Type: `str`, optional).

  Initialization time of the container, during which failed health checks are not counted (e. g. `1m`).

- `timeout` (Type: `str`, optional).

  Maximum time a health check command may run before it is considered failed (e. g. `30s`).

- `startup` (Type: dict of `startup` [options](#options-for-main--podman_construct_list--services--healthcheck--startup), optional).

  Startup health check, which runs until it succeeds before the regular health check begins.

### Options for `main` > `podman_construct_list` > `services` > `healthcheck` > `startup`

- **`cmd`** (Type: `str`, **required**).

  Command to run inside the container for the startup health check.

- `interval` (Type: `str`, optional).

  Interval between startup health checks.

- `retries` (Type: `int`, optional).

  Number of attempts before the container is restarted. `0` means the container is never restarted.

- `success` (Type: `int`, optional).

  Number of successful runs required before the regular health check begins.

- `timeout` (Type: `str`, optional).

  Maximum time a startup health check command may run before it is considered failed.

### Options for `main` > `podman_construct_list` > `services` > `map_user`

- `container_gid` (Type: `int`, optional).

  The GID to be mapped into the container. Defaults to `container_uid` if unspecified.

- **`container_uid`** (Type: `int`, **required**).

  The UID to be mapped into the container.

- `host_uid` (Type: `int`, optional).

- `host_user` (Type: `str`, optional).

  A user on the host system.

- `host_gid` (Type: `int`, optional).

- `host_group` (Type: `str`, optional).

  A group on the host system. If empty the primary group of `host_user` will be used.

### Options for `main` > `podman_construct_list` > `services` > `secrets`

- **`name`** (Type: `str`, **required**).

  The name of the secret as defined in the `secrets` top level option.

- **`env`** (Type: `str`, **required**).

  Name of the environment variable inside the container, which should contain the secret.

### Options for `main` > `podman_construct_list` > `services` > `volumes`

- **`src`** (Type: `str`, **required**).

  Named volume or source directory on the host.

- **`dest`** (Type: `str`, **required**).

  Destination directory inside the container.

- `options` (Type: `str`, optional).

  Mount options for the volume (e. g. `ro`).

- `owner` (Type: `str`, optional).

  If this is a bind volume and the folder is non-existing, the newly created folder will be owned by this user. Does not modify existing folders.

- `group` (Type: `str`, optional).

  Same as owner, but for group.

- `mode` (Type: `str`, optional).

  If this is a bind volume and the folder is non-existing, the newly created folder will have this mode. Does not modify existing folders.

### Options for `main` > `podman_construct_network_list`

- `disable_dns` (Type: `bool`, optional).

- `dns` (Type: `str`, optional).

- `driver` (Type: `str`, optional).

  Optionally set the driver for the network. Refer to [**podman-network-create(1)**](https://docs.podman.io/en/latest/markdown/podman-network-create.1.html) for more information. The special value `external` indicates that the network should be assumed existing and not managed by Ansible. If unspecified falls back to `bridge`.

  _Choices:_ `bridge`, `macvlan`, `ipvlan`, `external`

- `gateway` (Type: `str`, optional).

- `interface_name` (Type: `str`, optional).

- `internal` (Type: `bool`, optional).

- `ipam_driver` (Type: `str`, optional).

- `ipv6` (Type: `str`, optional).

- **`name`** (Type: `str`, **required**).

  Name of the quadlet file.

- `network_name` (Type: `str`, optional).

  Name of the podman network (e. g. `podman network ls`).

- `state` (Type: `str`, optional).

  This is the only option, which has little different effects than the original option from the ansible module. As this role always creates a quadlet `present` means that the quadlet is present and `absent` means that the quadlet is removed.

  _Choices:_ `present`, `absent`

- `subnet` (Type: `str`, optional).

## Dependencies

- {'role': 'lingfra.podman.podman_install', 'tags': ['podman_install'], 'when': ['podman_install_enable | default(true)']}
- {'role': 'lingfra.podman.podman_config', 'tags': ['podman_config'], 'when': ['podman_config_enable | default(true)']}

## Project Information

This role is part of the Ansible collection [lingfra.podman][collection_url].
For more information, see the collections [README](../../README.md) file.

[collection_url]: https://github.com/lingfra/ansible-collection-lingfra-podman
<!-- END_ANSIBLE_DOCS -->
