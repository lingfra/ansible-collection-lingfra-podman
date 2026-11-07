# Ansible Collection - lingfra.podman

> [!WARNING]
> **This repository has moved to GitHub:
> [github.com/lingfra/ansible-collection-lingfra-podman](https://github.com/lingfra/ansible-collection-lingfra-podman).**
> The Codeberg repository is no longer maintained. All issues and pull requests
> have been migrated, keeping their numbers.
>
> In July 2026 the Codeberg e.V. assembly
> [voted](https://blog.codeberg.org/protecting-our-floss-commons-from-llms.html)
> to extend Codeberg's Terms of Use with
> [§ 2 (1) 7](https://codeberg.org/Codeberg/org/commit/71149c7fc95ccfeae36109b5cddca339e4aa1473),
> which prohibits sharing projects that mostly consist of code written by
> generative AI tools such as Claude or OpenAI Codex. AI assistance is used for
> this repository, so it moved to GitHub.

Collection of Ansible content for managing Podman containers.

The main scope of this collection is to deploy Podman containers as systemd
units using [Podman Quadlet][quadlet] on remote servers. If you don't know what
[Podman Quadlet][quadlet] is, please read [this blog post][quadlet-intro]. It is
important that you have a basic understanding of [Podman Quadlet][quadlet] to
get the most out of this collection.

While [Quadlet][quadlet] is a really nice feature of Podman, it is not as
convenient as [Docker Compose][docker-compose] is. Especially, if you need to
manage many servers with individual container configurations, there is a need to
have a central place for these configurations. This collection tries to fulfill
this need by allowing configuration of multi-container applications through the
Ansible inventory.

Please note that while the `podman_construct_list` elements at first may look
like [Docker Compose][docker-compose] specs at first, they aren't! In
particular, it's not possible to just copy & paste sample Docker Compose files
from the web and just run them. This is expected because **Podman is not
Docker**. The interface of `podman_construct` is primarily designed to match the
vocabulary of Ansible and Podman. In addition, there are Podman specific
features supported by this collection (e.g. user namespaces). However,
rewriting the sample Docker Compose code shouldn't be too hard.

**Experimental alpha quality code. Expect bugs and interface changes, use with
caution!**

## Included Content

### Roles

- [podman_config](./roles/podman_config/README.md): Makes the necessary
configuration to use Podman on a host.
- [podman_construct](./roles/podman_construct/README.md): Deploys the Podman
components.
- [podman_image_prune](./roles/podman_image_prune/README.md): Configures a
systemd service to prune unused OCI images.
- [podman_install](./roles/podman_install/README.md): Installs Podman on a host.
- [podman_kube](./roles/podman_kube/README.md): Deploys kubernetes spec files and runs them.

### Playbooks

- [podman_construct](./roles): Creates a target group for all hosts, which have
`podman_construct_list` in their `hostvars` and runs the
[podman_construct](./roles/podman_construct/README.md) role on that group. The
roles `podman_config` and `podman_install` are pulled in as dependencies.
- [podman_image_prune](./playbooks/podman_image_prune.yaml): Runs role
[podman_image_prune](./roles/podman_image_prune/README.md).
- [podman_kube](./playbooks/podman_kube.yaml): Runs role [podman_kube](./roles/podman_kube/README.md).

## Installation

This collection is published to [Ansible Galaxy](https://galaxy.ansible.com). It
can be installed using the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install lingfra.podman
```

It is also possible to specify this collection in the `requirements.yaml` (or
`requirements.yml`) file:

```yaml
---
collections:
  - name: lingfra.podman
    version: "v0.1.0"   # optionally specify version
```

And use the Ansible Galaxy CLI to install the definitions from the requirements
file:

```bash
ansible-galaxy install -r requirements.yaml
```

Alternatively, the collection can be obtained from the Git repository. The
following `requirements.yaml` entry, can be used to download directly from Git:

```yaml
---
collections:
  - name: https://github.com/lingfra/ansible-collection-lingfra-podman
    version: main
    type: git
```

For more information, see the [Installing
collections](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html)
section of the Ansible documentation.

## Requirements

There are no platform specific requirements. However, [Quadlet][quadlet] is a
relatively new feature of Podman and therefore requires a recent version of
Podman. This collection is tested on Arch Linux with Podman 5.3.

Reports about tests on other distributions and Podman versions are very welcome!

## Usage

First define a _construct_ in [`podman_construct_list`][construct-doc] for a
host in the their host variables For example in
`host_vars/memos.example.com/main.yaml`:

```yaml
podman_construct_list:
  - name: memos

    secrets:
      memos-dsn: postgresql://memos:SuperS3cret@db:5432/memos
      postgres-password: SuperS3cret

    services:
      - name: app
        image: ghcr.io/usememos/memos:0.23.1
        depends_on:
          - postgres
        env:
          MEMOS_DRIVER=postgres
        publish:
          - 5230:5230
        pull: newer
        secrets:
          - name: memos-dsn
            env: MEMOS_DSN
        user: 1000
        userns: auto
        volumes:
          - src: app-storage
            dest: /var/opt/memos

      - name: db
        image: docker.io/library/postgres:17.2-alpine
        env:
          POSTGRES_DB: memos
          POSTGRES_USER: memos
        pull: newer
        secrets:
          - name: postgres-password
            env: POSTGRES_PASSWORD
        userns: auto
        volumes:
          - src: postgres-pgdata
            dest: /var/lib/postgresql/data
```

See the [podman_construct][construct-doc] role documentation for all options and
the [Molecule configuration](./molecule/podman_construct/converge.yml) for
examples.

Note that the name of the construct will be appended to all components: In this
example, the containers (services) will be named `memos-app` and `memos-db`.

After defining `podman_construct_list` for your hosts, you can run the playbook
provided by this collection. The playbook creates a target group containing only
hosts that have `podman_construct_list` in their host variables. Therefore, it
is safe to run the playbook against your entire inventory. However, it is still
strongly recommended to run a check first. It is also possible to limit the
affected hosts by modifying the variable `target`. Some examples:

```bash
# check run and show changes
ansible-playbook --check --diff lingfra.podman.podman_construct
# real run
ansible-playbook lingfra.podman.podman_construct
# custom inventory
ansible-playbook -i custom_inventory lingfra.podman.podman_construct
# limit to group 'my_podman_hosts' (need to exists in your inventory)
ansible-playbook lingfra.podman.podman_construct --limit my_podman_hosts
```

The roles `podman_config` and `podman_install` are pulled in as dependencies. If
this is not desired you can use the `--skip-tags` option:

```bash
ansible-playbook lingfra.podman.podman_construct --skip-tags podman_install,podman_config
```

You can also import the playbook into your local playbooks. Limiting the
affected hosts is possible by using the `target` variable. Disabling
`podman_config` and `podman_install` is also possible by using variables. This
approach also allows to use the dynamically created target group for further
configuration on these hosts (e.g. setting up a reverse proxy):

```yaml
---
- name: Import lingfra.podman.podman_construct
  ansible.builtin.import_playbook: lingfra.podman.podman_construct
  vars:
    target:
      - my_podman_hosts
    podman_install_enable: false
    podman_config_enable: false

# further configuration

- name: Further configure target_group_podman_construct hosts
  hosts: target_group_podman_construct
  tasks:
    - name: "Import my own or a custom role"
      ansible.builtin.import_role:
        # replace with an existing role
        name: my_reverse_proxy
```

The resulting [Quadlet][quadlet] files are placed in `/etc/containers/systemd`
and can be examined there. These are converted to systemd units after a `systemd
daemon-reload`, which the role runs automatically. However, if the role fails,
you may need to do this manually. After that, you can also examine the generated
systemd units:

```bash
systemctl cat memos-db
systemctl cat memos-app
```

A current limitation of podman_construct is that the generated services are not
managed (e.g. not started after deployment and are not restarted after changes).
This will be fixed soon! However, the systemd services generated by [Podman
Quadlet][Quadlet] are enabled by default, so they will start after a reboot. You
can also manage them manually with the usual systemd commands:

```bash
systemctl start memos-db
systemctl status memos-db
systemctl restart memos-db
systemctl start memos-app
systemctl status memos-app
systemctl restart memos-app

# Retrieve logs for the units only
journalctl -e -u memos-db.service
journalctl -e -u memos-app.service
```

### Updates with Renovate

Manually searching the web for updates to your images is a tedious task. For all
images listed in your Ansible inventory, it is a good idea to use
[Renovate](https://www.mend.io/renovate/). It will detect outdated image tags
and offer you the new versions.

Renovate has a [manager](https://docs.renovatebot.com/modules/manager/) to
detect image tags in e.g. Dockerfiles or Docker Compose files and provide a
[datasource](https://docs.renovatebot.com/modules/datasource/docker/) to update
them. However, the manager does not work on the
[podman_construct][construct-doc] syntax and does not match the Ansible
inventory files. Therefore, it is necessary to specify a custom manager. Add a
`renovate.json` file to your playbook root directory with the following content:

```json
{
  "enabledManagers": ["custom.regex"],
  "customManagers": [
    {
      "customType": "regex",
      "fileMatch": ["^inventory/.*/.*/.*\\.yaml$"],
      "matchStrings": [
        "image:\\s*(?<depName>[\\w./-]+):(?<currentValue>[\\w.-]+)"
      ],
      "datasourceTemplate": "docker"
    }
  ],
}
```

You may need to adjust the `fileMatch` regex depending on your inventory
structure. See [#3][issue-3] for more information.

There are many ways to [run
Renovate](https://docs.renovatebot.com/getting-started/running/). One way to run
Renovate is on your own server with Podman by using this collection:

```yaml
podman_construct_list:
  # ...
  - name: renovate

    secrets:
      gitea-token: foo # add your token here
      github-com-token: bar # add your token here

    services:
      - name: bot
        image: renovate-custom.build
        env:
          RENOVATE_AUTODISCOVER: '"true"'
          RENOVATE_ENDPOINT: https://codeberg.org/
          RENOVATE_GIT_AUTHOR: '"Renovate Bot <my-account@example.com>"'
          RENOVATE_PLATFORM: gitea
          RENOVATE_USERNAME: my-account
        restart: "no"
        secrets:
          - name: gitea-token
            env: RENOVATE_TOKEN
          - name: github-com-token
            env: GITHUB_COM_TOKEN
        userns: auto
```

Note that this is just a rough example and you will need to adapt this to your
needs! Create a systemd
[timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html)
to run the bot periodically:

```dosini
# /etc/systemd/system/renovate-bot.timer
[Unit]
Description=Run renovate bot

[Timer]
OnCalendar=*-*-* 05:00:00

[Install]
WantedBy=timers.target
```

Finish the configuration by enabling the timer:

```bash
systemctl daemon-reload
systemctl enable --now renovate-bot.timer
```

## Limitations

- [#1: Pods not supported](https://github.com/lingfra/ansible-collection-lingfra-podman/issues/1)
- [#4: `.build` Quadlets not supported](https://github.com/lingfra/ansible-collection-lingfra-podman/issues/4)

## Documentation

Role documentation (`roles/foo/README.md`) is generated by
[aar-doc](https://pypi.org/project/aar-doc/) based on the role's
`meta/argument_specs.yaml` file. See [.aar_doc.yml](./.aar_doc.yml) for the
configuration. The templates are maintained in a separate repository:
[lingfra/aar-doc-config](https://codeberg.org/lingfra/aar-doc-config).

Example for generating the `README.md` file for a role named _foo_:

```bash
aar-doc roles/foo markdown
```

## License

[The Unlicense](./LICENSE)

## Author Information

lingling ([Codeberg][Codeberg], [GitHub][GitHub])

[Codeberg]: https://codeberg.org/lingling
[GitHub]: https://github.com/lingling9000

[issue-3]: https://github.com/lingfra/ansible-collection-lingfra-podman/issues/3
[construct-doc]: https://github.com/lingfra/ansible-collection-lingfra-podman/tree/main/roles/podman_construct#podman_construct_list
[docker-compose]: https://docs.docker.com/compose/
[quadlet-intro]: https://www.redhat.com/en/blog/quadlet-podman
[quadlet]: https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
