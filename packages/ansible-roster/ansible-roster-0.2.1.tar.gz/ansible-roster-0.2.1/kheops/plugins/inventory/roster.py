# TODO:
# - Add explicit localhost?
#   ansible foobar.example.com -m debug -a 'var=group_names' => correct
#   ansible localhost          -m debug -a 'var=group_names' => incorrect
#
# - Handle ambiguity:
#   - if host is part of two groups with different variables?
#
# - Handle variables that aren't key-values, but lists or dicts.
#
# - Add yaml <<* support with collapsing
#
import re

from copy import deepcopy
from functools import wraps

import exrex
import cerberus
import yaml

from ansible.errors import AnsibleParserError
from torxtools import dicttools

from boltons.iterutils import remap, default_enter, default_visit

SCHEMA = r"""
---
include:
  type: list
  default: []  
  schema:
    type: string

vars: &vars
  type: dict
  default: {}
  keysrules:
    type: string
    # source: VALID_VAR_REGEX from ansible/playbook/conditional.py
    regex: '^[_A-Za-z]\w*$'

groups:
  type: dict
  default: {}
  keysrules: &group_name
    type: string
    # source: _SAFE_GROUP from somewhere
    regex: '^[_A-Za-z]\w*$'
  valuesrules:
    type: dict
    default: {}
    nullable: true
    schema:
      vars: *vars
      inherit:
        type: list
        default: []
        schema: *group_name

labels:
  type: dict
  default: {}
  keysrules: &label_name
    type: string
    regex: '^[\w]+$'
  valuesrules:
    type: dict
    default: {}
    nullable: true
    schema:
      vars: *vars
      inherit:
        type: list
        default: []
        schema: *label_name
 
hosts:
  type: dict
  default: {}
  keysrules:
    type: string
    # Accept almost anything and validate later
    regex: '^\S+$'
  valuesrules:
    type: dict
    default: {}
    nullable: true
    schema:
      vars: *vars
      groups:
        type: list
        default: []
        schema: *group_name
      labels:
        type: list
        default: []
        schema: *label_name
"""
schema = yaml.safe_load(SCHEMA)

from functools import wraps

kwd_mark = object()


def catch_recursion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (func.__qualname__,) + args + (kwd_mark,) + tuple(sorted(kwargs.items()))

        if key in catch_recursion.func_list:
            raise Exception("Labels create a creates a recursive dependency loop.")
        catch_recursion.func_list.append(key)
        rv = func(*args, **kwargs)
        catch_recursion.func_list.remove(key)
        return rv

    return wrapper


catch_recursion.func_list = []


# match a 'flat' part of hostname, that is without [], ()
flat_name_re = re.compile(r"^([^\[\(]+)")

# match a simple char class
range_seq_re = re.compile(r"^(\[(?:\d+:\d+)\])")
range_seq_parts = re.compile(r"^\[(\d+):(\d+)\]$")

# match a group
group_class_re = re.compile(r"^(\((?:[^\)\s]+)\))")


def _recompose_host(hostname, display):
    # convert foo[0-9]bar into parts, eg: foo, [0-9], and bar
    # we'll only exrex the regex'y parts
    #
    # The point being desktop[0-9].example.com should be treated as desktop[0-9]\.example\.com
    # There's probably a much easier way
    #
    # Convert range to regex
    def convert_range_to_regex(value, display):
        match = range_seq_parts.fullmatch(value)
        first = int(match[1])
        second = int(match[2]) + 1

        if first >= second:
            raise Exception(f"Range sequence [{first}:{second-1}] is invalid")

        fmt = "{:d}"
        if len(match[1]) > 1 and match[1][0] == "0":
            cnt = len(match[1])
            fmt = "{:0" + str(cnt) + "d}"

        rv = "(" + "|".join([str(fmt).format(x) for x in range(first, second)]) + ")"
        rv = exrex.simplify(rv)
        display.vvv(f"    Expand range sequence [{first}:{second-1}] with '{fmt}' format generates '{rv}'")
        return rv

    rv = []

    original = hostname
    display.vv(f"Splitting hostname = '{hostname}' via exrex...")
    while hostname:
        display.vvvv(f"  Current hostname = '{hostname}'")

        for what in [
            [flat_name_re, "plain", re.escape],
            [range_seq_re, "range", lambda x: convert_range_to_regex(x, display)],
            [group_class_re, "group", lambda x: x],
        ]:
            match = what[0].match(hostname)
            if bool(match):
                part = match[0]
                display.vvv("    Found %s section '%s'" % (what[1], part))
                rv.append(what[2](part))
                hostname = hostname[len(part) :]
                break
        else:
            raise Exception(f"Failed to recompose range sequence or regex from '{original}'")

    return "".join(rv)


def _split_hosts(hosts, display):
    # split hosts if we find a regex
    is_regex = lambda k: "(" in k or "[" in k
    split_required = [True for k, _ in hosts.items() if is_regex(k)]
    if not split_required:
        return hosts

    rv = {}
    for hostname, item in hosts.items():
        if not is_regex(hostname):
            rv[hostname] = item
            continue

        exrex_hostname = _recompose_host(hostname, display)
        # split with exreg
        count = exrex.count(exrex_hostname)
        display.vv("Generating %s hostnames from '%s'" % (count, hostname))
        if count > 100:
            msg = ""
            if count > 9000:
                msg = "It's over 9000! There's no way that could be right! "
            raise Exception(
                "error: {}extraction of the regex hostname '%s' would generate {} hostnames".format(msg, count)
            )

        for hostname in exrex.generate(exrex_hostname):
            rv[hostname] = item

    return rv


def _validate_data(data=None):
    """
    Validate the yaml data against a known and valid schema.

    :param data: yaml data
    :returns: True if valid, False if empty, Exception otherwise.
    """

    def visit(_path, key, _value):
        # drop all items that start with a dot ('.')
        if isinstance(key, str) and (key[0] == "."):
            return False
        return True

    if data is None:
        return False, None

    # drop the 'plugin' if present, it's not needed anymore
    data.pop("plugin", None)

    data = remap(data, visit=visit)
    validator = cerberus.Validator(schema)

    if not validator.validate(data):
        raise Exception(validator.errors)

    return True, data


def _include_file(path, data, display):
    with open(path, "r") as fd:
        new_data = yaml.safe_load(fd)
        rv, new_data = _validate_data(new_data)

    if rv == False:
        return data

    data = dicttools.deepmerge(new_data, data, visit=dicttools.strip_none)
    return _recursive_include(data, display)


def _recursive_include(data, display):
    if not data.get("include"):
        return data

    files = data.pop("include")
    for f in files:
        data = _include_file(f, data, display)

    return data


class RosterInventory:
    def __init__(self, data, display):
        self.display = display
        self._inventory = None

        # Save the contents in data and
        self._data = deepcopy(data)
        self._settings = self._data.pop("settings", None)

        self._data = _recursive_include(self._data, display)

    def validate_schema(self):
        """
        Validate the yaml data against a known and valid schema.

        :returns: True if valid, False if empty, Exception otherwise.
        """
        rv, data = _validate_data(self._data)
        if rv == False:
            return False

        self._data = data
        return True

    def parse(self, inventory, display):
        """
        :params inventory: An InventoryData object
        :returns: Inventory passed as params
        """
        # discard any invalid files with no hosts
        if not self._data.get("hosts"):
            raise AnsibleParserError("Inventory file has no hosts declared")

        self._roster = self._data
        self._inventory = inventory

        # for every group, add it as a group, then add it's variables if it has any
        self._root_groups = self._roster.get("groups") or {}
        self._root_hosts = self._roster.get("hosts") or {}

        # get all global vars and add them as is to the 'all' group
        self._add_item_vars(name="all", content=self._roster)

        self._root_hosts = _split_hosts(self._root_hosts, self.display)

        # fmt: off
        groups_method = {
            "funcs": [self._add_item, self._add_item_vars, self._add_item_subgroups],
            "add_fn": self._inventory.add_group,
            "subgroups_key": "inherit",
            "subgroups_msg": "Inherited group '%s' in '%s' not declared in root groups",
        }
        hosts_method = {
            "funcs": [self._add_item, self._add_item_labels, self._add_item_subgroups, self._add_item_vars],
            "add_fn": self._inventory.add_host,
            "subgroups_key": "groups",
            "subgroups_msg": "Group '%s' for host '%s' not declared in root groups",
        }
        # fmt: on

        self._add_items(self._root_groups, groups_method)
        self._add_items(self._root_hosts, hosts_method)

        # call reconcile to ensure "ungrouped" contains all hosts
        self._inventory.reconcile_inventory()
        return self._inventory

    def _add_items(self, source, method):
        for name, content in source.items():
            for fn in method.get("funcs", []):
                fn(name=name, content=content, method=method)

    def _add_item(self, name, method, **_kwargs):
        method["add_fn"](name)

    def _add_item_vars(self, name, content, **_kwargs):
        if not (content or {}).get("vars"):
            return
        for k, v in content["vars"].items():
            self._inventory.set_variable(name, k, v)

    @catch_recursion
    def _add_item_label(self, name, label_name):
        if not self._roster.get("labels") or not self._roster["labels"].get(label_name):
            self.display.warning("Label named '%s' for host '%s' is not declared in root 'labels'" % (label_name, name))
            return
        label = self._roster["labels"][label_name]
        for label_name in label.get("inherit") or []:
            self._add_item_label(name, label_name)
        # add the labels's variables to this host
        self._add_item_vars(name, content=label)

    def _add_item_labels(self, name, content, sublabels_name="labels", **_kwargs):
        if not content:
            return
        for label_name in content.get(sublabels_name) or []:
            self._add_item_label(name, label_name)

    def _add_item_subgroups(self, name, content, method):
        if not content:
            return
        for group in content.get(method["subgroups_key"], []):
            if group not in self._root_groups:
                self.display.warning(method["subgroups_msg"] % (group, name))
            self._inventory.add_group(group)
            self._inventory.add_child(group, name)
