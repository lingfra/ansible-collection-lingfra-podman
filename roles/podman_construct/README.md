<!-- BEGIN_ANSIBLE_DOCS -->
# Ansible Role: lingfra.podman.podman_construct

Deployes the Podman components.

## Supported Platforms

Not specified.

## Entrypoint `main` - Main entry point for podman_construct role

This is the main entrypoint for the podman_construct role.
Creates the quadlet files for the containerized components.

### Options for `main`

#### `podman_construct_list`

Type: `list of dicts of 'podman_construct_list' options`, **required**.

Specifies the configuration for the containers to be created.

**Options:**

- **`name`** (Type: `str`, **required**).

  Name of the construct. Will be appended to all the created content from this role.

- `networks` (Type: `list of dicts of 'networks' options`, optional).

  Definition of networks, which should be available in this construct.

  **Options:**

  - **`name`** (Type: `str`, **required**).

    Name of the network.

  - `driver` (Type: `str`, optional).

    Optionally set the driver for the network. Refer to [**podman-network-create(1)**](https://docs.podman.io/en/latest/markdown/podman-network-create.1.html) for more information. The special value `external` indicates that the network should be assumed existing and not managed by Ansible. If unspecified falls back to `bridge`.

    **Choices:**

    - `bridge`
    - `macvlan`
    - `ipvlan`
    - `external`

- `pod` (Type: `bool`, optional).

  Whether the services (containers) should be placed in a pod or not. If not placed in a pod, a network will be created.

- `secrets` (Type: `dict`, optional).

  A dictionary of secrets in the form `name: content`. It is necessary to define a secret here to use it in the service configuration.

- **`services`** (Type: `list of dicts of 'services' options`, **required**).

  Dictionary containing the definition of services.

  **Options:**

  - `depends_on` (Type: `str`, optional).

    List of other containers or services this container should depend on.

  - `env` (Type: `dict`, optional).

    Environment variables for the container.

  - `hostname` (Type: `str`, optional).

    Hostname of the container. Defaults to use the service name from the construct config.

  - `image` (Type: `str`, optional).

    Fully qualified image name (FQIN) and version (tag or digest) of the container image.

  - `map_user` (Type: `dict of 'map_user' options`, optional).

    A user to be mapped into the container user namespace. Using this option implies user namespace mode `auto`. This option is ignored when specifying `userns`.

    **Options:**

    - `container_gid` (Type: `int`, optional).

      The GID to be mapped into the container. Defaults to `container_uid` if unspecified.

    - **`container_uid`** (Type: `int`, **required**).

      The UID to be mapped into the container.

    - **`host_user`** (Type: `str`, **required**).

      A user on the host system.

    - `host_group` (Type: `str`, optional).

      A group on the host system. If empty the primary group of `host_user` will be used.

  - **`name`** (Type: `str`, **required**).

    Name of the service.

  - `network` (Type: `list of 'str'`, optional).

    Networks the container should be attached to.

  - `pod` (Type: `str`, optional).

    Pod the container should be attached to.

  - `pull` (Type: `str`, optional).

    Pull policy for the container.

  - `publish` (Type: `list of 'str'`, optional).

    List of port mappings for the container.

  - `restart` (Type: `str`, optional).

    Policy for restarting the service on exit. Takes the systemd service options, see **[systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html#Restart=)**.

    **Choices:**

    - `always`
    - `no`
    - `on-abnormal`
    - `on-abort`
    - `on-failure`
    - `on-success`
    - `on-watchdog`

  - `secrets` (Type: `list of dicts of 'secrets' options`, optional).

    Secrets the container should get access to.

    **Options:**

    - **`name`** (Type: `str`, **required**).

      The name of the secret as defined in the `secrets` top level option.

    - **`env`** (Type: `str`, **required**).

      Name of the environment variable inside the container, which should contain the secret.

  - `user` (Type: `str`, optional).

    User running the application inside the container. Either name or UID.

  - `userns` (Type: `str`, optional).

    User namespace mode for the container. Overwrites `map_user` when configured.

  - `volumes` (Type: `list of dicts of 'volumes' options`, optional).

    Volumes for the container.

    **Options:**

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

## Dependencies

- {'role': 'lingfra.podman.podman_install', 'tags': ['podman_install']}
- {'role': 'lingfra.podman.podman_config', 'tags': ['podman_config']}

## Project Information

This role is part of the Ansible collection [lingfra.podman][collection_url].
For more information, see the collections [README](../../README.md) file.

[collection_url]: https://github.com/lingfra/ansible-collection-lingfra-podman
<!-- END_ANSIBLE_DOCS -->
