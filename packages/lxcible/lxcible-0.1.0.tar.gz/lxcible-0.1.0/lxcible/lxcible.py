#!/usr/bin/env python3
"""
A dynamic ansible inventory based on running linuxcontainers.

When invoked with --list, lxd-inventory.py will a json inventory based on
currently running containers.
"""

import argparse
import subprocess
import sys
import json


class LxcInventory():
    """
    Use LxcInventory to create an ansible inventory that reflects
    currently running linux containers
    """
    def __init__(self):
        self.lxc_bin = '/snap/bin/lxc'
        self.inventory = {}

        self.containers = self.get_containers()
        self.inventory = self.get_inventory()

    def dump(self):
        """
        prints the json inentory to stdout
        """
        print(json.dumps(self.inventory, sort_keys=True, indent=4))

    def get_containers(self):
        """
        runs lxc ls to get the containers in json format
        """
        result = subprocess.run(
            [self.lxc_bin, 'ls', '--format=json'],
            stdout=subprocess.PIPE,
            check=True
        )
        return json.loads(result.stdout.decode('UTF-8'))

    def get_inventory(self):
        """
        transforms the list of containers into an ansible inventory
        """
        inv = {}
        hostvars = {}
        for container in self.containers:
            if container['state']['status'] == 'Running':
                address = container['state']['network']['eth0']['addresses'][0]['address']
                hostvar = {
                    'ansible_host': address
                }
                hostvars[container['name']] = hostvar

                # determine ansible groups
                groups = []
                if 'user.ansible.groups' in container['config']:
                    groups = container['config']['user.ansible.groups'].split(",")

                # add host to 'all' group
                groups.append('all')

                # pivot
                for group in groups:
                    if group not in inv:
                        inv[group] = []
                    inv[group].append(container['name'])

        inv['_meta'] = {'hostvars': hostvars}
        return inv


if __name__ == "__main__":
    # execute only if run as a script
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--list', action='store_true')
    ARGS = PARSER.parse_args()
    if ARGS.list:
        INVENTORY = LxcInventory()
        INVENTORY.dump()
        sys.exit(0)
    else:
        print("Use --list for actual inventory output")
        sys.exit(1)
