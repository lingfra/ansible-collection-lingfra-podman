<!-- BEGIN_ANSIBLE_DOCS -->
# Ansible Role: lingfra.podman.podman_auto_update

Manages the podman-auto-update timer for the system and for users.

## Supported Platforms

Not specified.

## Entrypoint `main` - Main entry point for podman_auto_update role

This is the main entrypoint for the podman_auto_update role.
Manages the `podman-auto-update.timer` shipped with Podman for the system (rootful containers) and for users (rootless containers).
The timer runs [**podman-auto-update(1)**](https://docs.podman.io/en/latest/markdown/podman-auto-update.1.html), which updates all containers that have `AutoUpdate=` set in their quadlet (see the `auto_update` option of the `podman_construct` role).
An `OnCalendar=` override is written as a systemd drop-in and removed again when the option is unset.
The timer is restarted when its drop-in changes.

### Options for `main`

#### `podman_auto_update_enabled`

Type: `bool`, Default: `True`.

Whether the system `podman-auto-update.timer` is enabled and started. Set this option to `false` to disable and stop the timer.

#### `podman_auto_update_on_calendar`

Type: `str`, optional.

Overrides `OnCalendar=` of the system `podman-auto-update.timer`. When unset, the drop-in is removed and the Podman default (`daily`) applies. See [**systemd.time(7)**](https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html) for the syntax.

#### `podman_auto_update_user_list`

Type: list of dicts of `podman_auto_update_user_list` [options](#options-for-main--podman_auto_update_user_list), Default: `[]`.

A list of users for which the user `podman-auto-update.timer` is managed. Lingering must be enabled for every user in this list, because the timer only runs while the user's systemd instance is running. The role fails if lingering is not enabled, but does not manage it. Removing a user from this list does not change anything for that user. Set `enabled: false` instead.

### Options for `main` > `podman_auto_update_user_list`

- **`name`** (Type: `str`, **required**).

  The name of the user.

- `enabled` (Type: `bool`, Default: `True`).

  Whether the timer is enabled and started for the user. Set this option to `false` to disable and stop the timer for this user.

- `on_calendar` (Type: `str`, optional).

  Overrides `OnCalendar=` of the user's `podman-auto-update.timer`. When unset, the drop-in is removed and the Podman default (`daily`) applies.

### Examples for `main`

```yaml
- name: "Configure podman auto-update"
  hosts: all
  tasks:
    - name: "Import role lingfra.podman.podman_auto_update"
      ansible.builtin.import_role:
        name: lingfra.podman.podman_auto_update
      vars:
        # update rootful containers every night at 04:00
        podman_auto_update_on_calendar: "*-*-* 04:00:00"
        podman_auto_update_user_list:
          # rootless containers of alice, Podman default schedule
          - name: alice
          # rootless containers of bob, every Sunday
          - name: bob
            on_calendar: "Sun *-*-* 03:00:00"
```

## Dependencies

None.

## Project Information

This role is part of the Ansible collection [lingfra.podman][collection_url].
For more information, see the collections [README](../../README.md) file.

[collection_url]: https://github.com/lingfra/ansible-collection-lingfra-podman
<!-- END_ANSIBLE_DOCS -->
