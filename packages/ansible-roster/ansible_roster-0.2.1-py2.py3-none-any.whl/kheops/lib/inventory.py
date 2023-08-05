import os
from operator import attrgetter
import yaml

from ansible.cli.inventory import INTERNAL_VARS

from boltons.iterutils import remap, default_exit


def verify_file(name, path, display, ext=None):
    """
    Verify if file is usable by this plugin.
    To be accepted by this plugin, file must be a yaml file and contain:

    ~~~yaml
    ---
    plugin: *name*
    ~~~

    :param path: file path
    :param display: Ansible display object
    :returns: True if file is accepted
    """
    if not ext:
        ext = ["yml", "yaml"]

    try:
        lpath = path.lower()
        if not lpath.endswith(tuple([".{}".format(e.lower()) for e in ext])):
            display.debug("roster inventory plugin ignoring '%s': wrong file extension" % path)
            return False

        # if file is called 'name.ext', then accept it without opening it
        # TODO: we could be nice on lcase/ucase extensions like above ...
        if os.path.basename(path) in ["{}.{}".format(name, e) for e in ext]:
            display.debug("roster inventory plugin accepting '%s': exact file name match" % path)
            return True

        with open(path, "r") as fd:
            data = yaml.safe_load(fd)

        if data.get("plugin") == name:
            return True
        display.warning("roster inventory plugin ignoring '%s': no 'plugin: %s' key-value" % (path, name))
    except yaml.scanner.ScannerError as err:
        display.warning("syntax error %s: %s" % (str(err.problem_mark).strip(), err.problem))
    except Exception as err:
        display.warning("unknown exception: %s" % str(err))
    return False


def to_dict(inventory):
    """
    Return inventory as a dict. It can then be transformed directly to
    valid ansible JSON inventory.

    :params inventory: An InventoryData object
    :returns: Dictionnary
    """

    def visit(_path, key, value):
        # if it's a list, but it's empty, then drop it
        if isinstance(value, list) and not value:
            return False
        if isinstance(value, dict) and not value and key != "hostvars":
            return False
        return True

    def exit(path, key, old_parent, new_parent, new_items):
        rv = default_exit(path, key, old_parent, new_parent, new_items)
        # if it's a list, then sort it.
        if isinstance(rv, list):
            rv.sort()
        return rv

    # loosely adapted from ansible/cli/inventory.py
    # too bad there's no public API for this conversion
    rv = {"_meta": {"hostvars": {}}}
    seen = set()

    def format_group(group):
        rv = {
            group.name: {
                # since a host belongs to either a group, or the group 'ungrouped', there are no hosts in group 'all'
                "hosts": [h.name for h in sorted(group.hosts, key=attrgetter("name")) if group.name != "all"],
                "children": [],
            },
        }
        for subgroup in sorted(group.child_groups, key=attrgetter("name")):
            rv[group.name]["children"].append(subgroup.name)
            if subgroup.name not in seen:
                rv.update(format_group(subgroup))
                seen.add(subgroup.name)
        return rv

    top = inventory.groups.get("all")
    rv.update(format_group(top))

    # populate meta
    for host_name, host in inventory.hosts.items():
        host_vars = {}
        for group in sorted(host.groups, key=attrgetter("name")):
            # print(group.name, " =>", group.vars)
            host_vars.update(group.vars)
        host_vars.update(host.vars)
        host_vars = {k: v for k, v in host_vars.items() if k not in INTERNAL_VARS}
        if host_vars:
            rv["_meta"]["hostvars"][host_name] = host_vars

    rv = remap(rv, visit=visit, exit=exit)
    return rv
