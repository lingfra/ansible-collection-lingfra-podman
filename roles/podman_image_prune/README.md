<!-- BEGIN_ANSIBLE_DOCS -->
# Ansible Role: lingfra.podman.podman_image_prune

Configures a systemd service to prune unused OCI images.

## Supported Platforms

Not specified.

## Entrypoint `main` - Main entry point for podman_image_prune role

This is the main entrypoint for the podman_image_prune role.

### Options for `main`

#### `podman_image_prune_on_calendar`

Type: `str`, Default: `*-*-* 01:00:00`.

The time on which the service should be started. See **`systemd.time(7)`** for more information.

#### `podman_image_prune_user_list`

Type: list of dicts of `podman_image_prune_user_list` [options](#options-for-main--podman_image_prune_user_list), Default: `[]`.

A list of users for which the podman images should be pruned.

### Options for `main` > `podman_image_prune_user_list`

- **`name`** (Type: `str`, **required**).

  The name of the user.

- `enabled` (Type: `bool`, Default: `True`).

  Specify if the unit should be enabled for the user or not. The default is to enable the user if it is specified in this list. Set this option to `false` if you want to disable the timer for this user.

## Dependencies

None.

## Project Information

This role is part of the Ansible collection [lingfra.podman][collection_url].
For more information, see the collections [README](../../README.md) file.

[collection_url]: https://github.com/lingfra/ansible-collection-lingfra-podman
<!-- END_ANSIBLE_DOCS -->
