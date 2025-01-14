from __future__ import absolute_import, division, print_function

from ansible.plugins.lookup import LookupBase

__metaclass__ = type

DOCUMENTATION = """
    name: all_nodes
    author: Julien Tachoires
    short_description: Lookup function returning the list of all the nodes
    description:
      - "Lookup function returning the list of all the nodes and their public
      and private IPs"
    options:
"""

EXAMPLES = """
- name: Show all the nodes and their IPs
  debug: msg="{{ lookup('all_nodes') }}"
"""

RETURN = """
_value:
  description:
    - List: list of dict containing the inventory hostname, the private ip and
      the public ip.
  type: list
  elements: dict
"""


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        all_nodes = []
        added_nodes = {}
        myvars = getattr(self._templar, "_available_variables", {})

        allowed_groups = [
            "primary",
            "standby",
            "pemserver",
            "pgbouncer",
            "pgpool2",
            "barmanserver",
            "dbt2_driver",
            "dbt2_client",
            "hammerdbserver",
            "witness",
            "proxy",
            "pgbackrestserver",
        ]
        for group, nodes in variables["groups"].items():
            # Ignore hosts that are not part of any group used in this
            # collection.
            if group not in allowed_groups:
                continue

            for inventory_hostname in nodes:
                if inventory_hostname in added_nodes:
                    continue
                added_nodes[inventory_hostname] = True
                hostvars = myvars["hostvars"][inventory_hostname]
                all_nodes.append(
                    dict(
                        inventory_hostname=inventory_hostname,
                        private_ip=hostvars.get("private_ip", None),
                        ansible_host=hostvars.get("ansible_host", None),
                    )
                )
        return all_nodes
