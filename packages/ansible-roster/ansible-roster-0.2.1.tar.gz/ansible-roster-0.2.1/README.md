[![documentation](https://img.shields.io/badge/documentation-html-informational)](https://ansible-kheops.gitlab.io/plugins/roster/index.html)
[![python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-informational)](https://pypi.org/project/kheops-roster/)

# Kheops Ansible Roster Plugin

This repository contains an Ansible inventory plugin to generate inventory from a subjectively simpler inventory description file while having more possibilities.

Supports ranges (eg: "[0:9]") and regex hostnames (eg: "(dev|prd)-srv")

## Installation

Install latest version:

~~~bash
python3 -mpip install --pre -U kheops-roster
~~~

## Features

* Subjectively simpler syntax

* 'Labels' that behave like groups but that do not create groups.

* Ranges and Regex support: `sql-[0:9].example.com`, `(front|back)end-[0:9].example.com`

## Usage

### 'Roster' inventory file

The roster inventory file is a typical yaml file.

A sample, commented, file named 'roster.yml.tpl' is located at the root of the git repository.

In order for ansible to use the plugin and parse your roster file, several conditions must be met.

* Your yaml file must contain a line indicating that the file is in the roster format.

* You must activate plugins and enable the roster inventory plugin in your ansible.cfg

### Sample roster.yml

~~~yaml
---
plugin: roster

hosts:
  localhost:
~~~

### Sample edited ansible.cfg

~~~toml
[defaults]
# The following line prevents having to pass -i to ansible-inventory.
# Filename can be anything as long as it has a 'yml' or 'yaml' extension although
# the plugin will directly accept any file named 'roster.yml'.
inventory = roster.yml

[inventory]
# You must enable the roster plugin if 'auto' does not work for you
enable_plugins = roster
~~~

Verify that the plugin is correctly found:

~~~bash
ansible-inventory --graph
~~~

## Development

To run unit tests, you can simply run the make target:

~~~bash
# run all tests:
make check
~~~

It's also possible to quickly check the output inventory:
~~~bash
export PYTHONPATH="$PYTHONPATH:$(pwd)"
ANSIBLE_INVENTORY_ENABLED=roster ANSIBLE_INVENTORY_PLUGINS="$(pwd)/ansible_roster/plugins/inventory" ansible-inventory --list -i roster.yml
~~~

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Locations

  * Documentation: [https://ansible-kheops.gitlab.io/plugins/roster/index.html](https://ansible-kheops.gitlab.io/plugins/roster/index.html)
  * GitLab: [https://gitlab.com/ansible-kheops/plugins/roster](https://gitlab.com/ansible-kheops/plugins/roster)


