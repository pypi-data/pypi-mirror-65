from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display

import kheops.lib.inventory as lib
from kheops.plugins.inventory.roster import RosterInventory

display = Display()


__metaclass__ = type

DOCUMENTATION = """
    name: roster
    plugin_type: inventory
    authors:
      - Julien Lecomte (julien@lecomte.at)
    short_description: Get inventory from a simplified yaml file.
    requirements:
        - python >= 3.6
    description:
        - Lorem Ipsum
    options:
        plugin:
            description: The name of this plugin, it should always be set to 'roster' for this plugin to recognize it as it's own.
            type: str
            required: true
            choices:
              - roster
"""

EXAMPLES = """
---
# roster.yml
plugin: roster
"""


class InventoryModule(BaseInventoryPlugin):
    """
    Host inventory parser for roster.yml source
    """

    NAME = "roster"

    def verify_file(self, path):
        """
        Verify if file is usable by this plugin.
        To be accepted by this plugin, file must be a yaml file and contain:

        ~~~yaml
        ---
        plugin: roster
        ~~~

        :param path: file path
        :returns: True if file is accepted
        """
        # we expect a yaml file, with 'plugin: roster'
        return lib.verify_file(self.NAME, path, display=display)

    def parse(self, inventory, loader, path, cache=True):
        r = RosterInventory(loader.load_from_file(path, cache=False) or {}, display)

        display.debug("Validating roster schema (%s)" % (path))
        r.validate_schema()

        display.debug("Converting roster schema (%s)" % (path))
        inventory = r.parse(inventory, display)
