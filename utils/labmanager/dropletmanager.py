# 
# virtualab
#
# MIT License
# 
# Copyright (c) 2024 Antoine Neuenschwander
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PyDo official Python client library for DigitalOcean
# https://pydo.readthedocs.io/en/latest/


from pydo import Client
import json
import jq


class DropletManager:
    """
    Class used to manage kali instances on DigitalOcean
    """

    def __init__(self, token, snapshot, sshkey, vpcname):
        """
        Creates a new manager instance initialized by a config file

        :param config_file: the path of the config file, defaults to './config.ini'
        :return: returns nothing
        """
        self.dop_token = token
        self.dop_snapshot = snapshot
        self.dop_sshkey = sshkey
        self.dop_vpcname = vpcname
        self.client = Client(token=self.dop_token)


    def list(self, tag='labbox'):
        """
        Lists all droplets with the given tag.

        :param tag: tag to retrieve droplets for, defaults to 'kali'.
        :return: returns a dict containing the list of droplets.
        """
        res = self.client.droplets.list(tag_name=tag, per_page=50)
        return res
    
    def create(self, name):
        """
        Creates a droplet from the configured snapshot with the specified name.

        :param name: the name of the droplet to create.
        :return: returns a dict with the created droplet details.
        """
        req = {
            "name": name,
            "region": "fra1",
            "size": "s-2vcpu-4gb",
            "image": self.resolve_snapshot(),
            "ssh_keys": [self.dop_sshkey],
            "backups": False,
            "tags": ["labbox"],
            "vpc_uuid": self.resolve_vpc()
        }
        res = self.client.droplets.create(body=req)
        return res
    
    def destroy(self, droplet_id):
        return self.client.droplets.destroy(droplet_id)

    def resolve_vpc(self):
        for vpc in self.client.vpcs.list()['vpcs']:
            if vpc['name'].strip() == self.dop_vpcname.strip():
                return vpc['id']
    
    def resolve_droplet_id_by_name(self, droplet_name):
        return jq.first(f'.droplets[] | select(.name=="{droplet_name}") | .id', self.list())

    def resolve_snapshot(self, snapshot_name):
        for snapshot in self.client.snapshots.list():
            if snapshot['name'].strip() == self.dop_snapshot.strip():
                return snapshot['id']
    
    def get_ipaddr_by_name(self, droplet_name):
        return jq.first(f'.droplets[] | select(.name=="{droplet_name}") | .networks.v4[] | select(.type == "public") | .ip_address', self.list())
    
    def reboot(self, droplet_id):
        print(f"reboot {droplet_id}")
        #return self.client.droplets.reboot(droplet_id)
        return self.client.droplet_actions.post(droplet_id, body={"type": "power_cycle"})
