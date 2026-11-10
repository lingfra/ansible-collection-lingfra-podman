<!-- BEGIN_ANSIBLE_DOCS -->
# Ansible Role: lingfra.podman.podman_kube

Deploys kubernetes spec files and runs them.

## Supported Platforms

Not specified.

## Entrypoint `main` - Main entry point for lingfra.podman.podman_kube role

The scope of this role is to template kube spec files from the Ansible playbook directory to a host.
It is on the user to write the kube spec.
To run the kube spec a `.kube` quadlet file will be templated to `/etc/containrs/systemd`.
This role also takes care of starting, enabling and restarting the systemd service after changes.

### Options for `main`

#### `podman_kube_list`

Type: list of dicts of `podman_kube_list` [options](#options-for-main--podman_kube_list), Default: `[]`.

A list of kube specs.

### Options for `main` > `podman_kube_list`

- `description` (Type: `str`, optional).

  This description will be added to the system unit. It will appear in the output of `systemctl list-units` or `systemctl status <UNIT-NAME>`.

- **`name`** (Type: `str`, **required**).

  Name of the kube spec.

- `quadlet_options` (Type: `str`, optional).

  Options for the quadlet file, which are copied to the systemd unit.

- `restart` (Type: `str`, optional).

  Policy for restarting the service on exit. Takes the systemd service options, see **[systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html#Restart=)**.

  _Choices:_ `always`, `no`, `on-abnormal`, `on-abort`, `on-failure`, `on-success`, `on-watchdog`

- **`template`** (Type: `str`, **required**).

  Name of a template file residing in the playbooks template directory.

- `template_vars` (Type: `dict`, optional).

  Variables for the template.

### Examples for `main`

```yaml
- name: "Configure podman kube play quadlets"
  hosts: all
  gather_facts: true
  tags:
    - podman_kube
  tasks:
    - name: "Import role lingfra.podman.podman_kube"
      ansible.builtin.import_role:
        name: lingfra.podman.podman_kube
      vars:
        podman_kube_list:
          - name: mailserver
            # file residing in /path/to/playbook/dir/templates/kube/mailserver.yaml.j2
            template: kube/mailserver.yaml.j2
            # the template has a variable called 'template_vars.hostnanme'
            template_vars:
              hostname: mail.example.com
```

## Dependencies

None.

## Project Information

This role is part of the Ansible collection [lingfra.podman][collection_url].
For more information, see the collections [README](../../README.md) file.

[collection_url]: https://github.com/lingfra/ansible-collection-lingfra-podman
<!-- END_ANSIBLE_DOCS -->
