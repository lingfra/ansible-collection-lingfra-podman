# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- podman_construct: Added service option `auto_update`, which sets `AutoUpdate=`
  in the container quadlet

## [0.1.0] - 2025-02-02

This version initializes the collection and implements a basic proof of concept
for deploying containerized infrastructure as [Podman
Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)
files.

- Added role podman_install
- Added role podman_config
- Added role podman_construct
- Added playbook podman_construct

[Unreleased]: https://github.com/lingfra/ansible-collection-lingfra-podman/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/lingfra/ansible-collection-lingfra-podman/releases/tag/v0.1.0
