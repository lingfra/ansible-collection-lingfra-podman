<!-- BEGIN_ANSIBLE_DOCS -->
# Ansible Role: lingfra.podman.podman_install

Installs Podman on a host.

## Supported Platforms

Not specified.

## Entrypoint `main` - Main entry point for podman_install role

This role installs podman on a system.
Currently this role only uses generic package names. Contributions are welcome to support individual install procedures for specific distributions.

### Options for `main`

#### `podman_install_enable`

Type: `bool`, Default: `True`.

Whether the Podman packages should be installed or not. Setting this to false won't include any installation tasks. As this role could be included as dependency by other roles, this is useful if it is desired to install Podman with an method not supported by this role.

#### `podman_install_fuse_overlayfs`

Type: `bool`, Default: `False`.

Whether or not fuse-overlayfs should be installed. `fuse-overlayfs` is an alternative storage driver for rootless Podman containers. The native overlayfs provides better performance is most cases, see upstream documentation for more information: <https://github.com/containers/podman/blob/main/docs/tutorials/performance.md#choosing-a-storage-driver>

## Dependencies

None.

## Project Information

This role is part of the Ansible collection [lingfra.podman][collection_url].
For more information, see the collections [README](../../README.md) file.

[collection_url]: https://codeberg.org/lingfra/ansible-collection-lingfra-podman
<!-- END_ANSIBLE_DOCS -->
