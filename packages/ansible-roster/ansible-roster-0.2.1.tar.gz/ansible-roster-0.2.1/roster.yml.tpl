# vim: ft=yaml
---
# This is a sample, commented, roster file in order to generate an ansible
# inventory.
#
# Your ansible.cfg must contain the 'roster' plugin and have the plugin enabled.
#   [defaults]
#   inventory = roster.yml
#   inventory_plugins = path/to/roster/plugins/inventory

#   [inventory]
#   enable_plugins = roster
---
# Mandatory line to tell ansible this is a roster file and not any yaml file
# unless file is called 'roster.yml':
plugin: roster

# Host variables are overwritten with priority:
#   1 - values from hosts.*.vars
#   2 - values from labels.*.vars
#   3 - values from groups.*.vars
#   4 - values from vars
# With 1 being the most important variable.
#

vars:
  var__foobar01: true
  components: "main contrib"

groups:
  debian:
    vars:
      distrib: "debian"

  stretch:
    inherit:
      - debian
    vars:
      release: "stretch"

  buster:
    inherit:
      - debian
    vars:
      release: "buster"

  desktops:
    vars:
      components: "main contrib non-free"

  server:
    vars:
      components: "main"

hosts:
  desktop01.internal.example.com:
    groups:
      - desktops
      - buster
    vars:
      var__foobar01: false

  server01.internal.example.com:
    groups:
      - servers
      - debian

  server01.example.com:
    groups:
      - servers
      - debian

  # items that start with a dot will be ignored, as will be items that start
  # with X-/x-
  .server02.example.com:
    groups:
      - servers
      - debian

  server03.example.com:
    x-foobar: jdoe

