<!-- BEGIN_ANSIBLE_DOCS -->
# Ansible Role: lingfra.podman.podman_config

Makes the necessary configuration to use Podman on a host.

## Supported Platforms

Not specified.

## Entrypoint `main` - Main entry point for podman_config role

This role does some necessary system configuration for using Podman.
Currently this role only adds ID ranges in `/etc/subuid` and `/etc/subgid` for the user `containers` to use the user namespace mode `auto` in rootful Podman.

### Options for `main`

#### `podman_config_enable`

Type: `bool`, Default: `True`.

Whether the podman configuration tasks should be run or not. Setting this to `false` results in skipping the include for the configuration tasks. As this role is also used as a dependency, this is a way to disable this role. This could be desired if a custom configuration is made, which conflicts with the configuration provided by this role.

## Dependencies

None.

## Project Information

This role is part of the Ansible collection [lingfra.podman][collection_url].
For more information, see the collections [README](../../README.md) file.

[collection_url]: https://codeberg.org/lingfra/ansible-collection-lingfra-podman
<!-- END_ANSIBLE_DOCS -->
