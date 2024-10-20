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

import argparse
import json
import jq
import yaml

from prettytable import PrettyTable
from dropletmanager import DropletManager
from guacmanager import GuacamoleManager

def droplet_to_table(droplet_data):
    """
    Converts droplet json data to a condensed list for output formatting
    see api reference: https://docs.digitalocean.com/reference/api/api-reference/#operation/droplets_get
    """
    table = PrettyTable()
    table.field_names = ["id", "name", "status", "size", "template_id", "template_name", "ip-addr"]
    jquery = jq.compile('.[] | [\
            .id, .name, .status, .size_slug, .image.id, .image.name,\
            (.networks.v4[] | select(.type == "public")).ip_address // "-" ]')
    if 'droplets' in droplet_data:
        input = droplet_data['droplets']
    elif 'droplet' in droplet_data:
        input = [droplet_data['droplet']]
    table.add_rows(jquery.input_value(input))
    return table


def add_user_with_connection(name, password):
    """
    Adds or updates a user and adds or updates a connection to the corresponding labbbox.
    Note that the username and the hostname are designed to be the same, i.e. user "labbox-12"
    logs in host "labbox-12"

    :param name: the username/host to associate, e.g. "labbox-12" (= username AND hostname)
    """
    # get dict of form:
    #{
    #    "labbox-0": "134.209.228.65",
    #    "labbox-1": "206.189.59.210"
    #}
    boxes = jq.first('reduce .droplets[] as $i ({}; .[$i.name] = ($i.networks.v4[] | select(.type == "public")).ip_address)', dropletmgr.list())
    if name not in boxes:
        print(f"labbox '{name}' does not exist. Please create it first.")
        return
    users = guacmgr.list_users()
    if name not in users:
        print(f"User does not exist, creating user '{name}'.")
        guacmgr.create_user(name, password)
    res = guacmgr.list_connections_with_parameters()
    conn = jq.all(f'.[] | select(.name == "{name}")', res)
    rdp_username = config['digitalocean']['labbox']['rdp_username']
    rdp_password = config['digitalocean']['labbox']['rdp_password']
    if not conn:
        # connection does not exist yet
        print("creating connection")
        conn = guacmgr.create_connection(name, boxes[name], rdp_username, rdp_password)
        key = conn['identifier']
    elif boxes[name] != conn[0]['hostname']:
        # ip mismatch, replace connection
        print(f"ip mismatch, replacing connection.")
        guacmgr.delete_connection(conn[0]["key"])
        conn = guacmgr.create_connection(name, boxes[name], rdp_username, rdp_password)
        key = conn['identifier']
    else:
        key = conn[0]['key']
    # finally, assign user -> connection
    print(f"assigning {name} to connection {key}")
    guacmgr.assign_user_to_connection(name, key)

def automap():
    for name in jq.all('.droplets[].name', dropletmgr.list()):
        if name.count('-') > 0:
            print(f"[+] automap {name}")
            password = config['digitalocean']['labbox']['password_prefix'] + name.split("-")[1]
            add_user_with_connection(name, password)

def main(args):
    if args.root_cmd == "map":
        if args.map_cmd == "add":
            add_user_with_connection(args.name, args.password)
        if args.map_cmd == "automap":
            automap()


    if args.root_cmd == "droplet":
        if args.droplet_cmd == "list":
            print(droplet_to_table(dropletmgr.list()))
    
        if args.droplet_cmd == "create":
            print(droplet_to_table(dropletmgr.create(args.name)))
    
        if args.droplet_cmd == "destroy":
            droplet_id = dropletmgr.resolve_droplet_id_by_name(args.droplet_name)
            print(json.dumps(dropletmgr.destroy(droplet_id), indent=4))
        
        if args.droplet_cmd == "reboot":
            droplet_id = dropletmgr.resolve_droplet_id_by_name(args.droplet_name)
            print(json.dumps(dropletmgr.reboot(droplet_id), indent=4))

    
    if args.root_cmd == "guacamole":
        if args.guac_cmd == "connection":
            if args.guac_conn_cmd == "list":
                table = PrettyTable()
                table.field_names = ["key", "name", "protocol", "hostname", "port", "username", "password"]
                jquery = jq.compile('.[] | [.key, .name, .protocol, .hostname, .port, .username, .password ]')
                table.add_rows(jquery.input_value(guacmgr.list_connections_with_parameters()))
                print(table)
            if args.guac_conn_cmd == "delete":
                guacmgr.delete_connection(args.key)
            if args.guac_conn_cmd == "create":
                guacmgr.create_connection(args.name, args.host)
        if args.guac_cmd == "user":
            if args.guac_user_cmd == "list":                
                table = PrettyTable()
                table.field_names = ["username", "last_active", "conn_permissions"]
                jquery = jq.compile('.[] | [.username, (.lastActive / 1000 | todate),\
                                    ([.connectionPermissions[] | .name] | join(","))]')
                table.add_rows(jquery.input_value(guacmgr.list_users_with_permissions()))
                print(table)
            if args.guac_user_cmd == "delete":
                guacmgr.delete_user(args.username)
            if args.guac_user_cmd == "create":
                guacmgr.create_user(args.username, args.password)
            if args.guac_user_cmd == "assign":
                conn_id = guacmgr.resolve_connection_by_name(args.conn_name)
                guacmgr.assign_user_to_connection(args.username, conn_id)
            if args.guac_user_cmd == "revoke":
                conn_id = guacmgr.resolve_connection_by_name(args.conn_name)
                guacmgr.revoke_user_from_connection(args.username, conn_id)

if __name__ == '__main__':
    with open('../../config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    token = config['digitalocean']['token']
    snapshot = config['digitalocean']['labbox']['snapshot_name']
    sshkey = config['digitalocean']['ssh_key_name']
    vpcname = config['digitalocean']['network']['vpc_name']
    dropletmgr = DropletManager(token, snapshot, sshkey, vpcname)

    guac_url = f"https://{config['digitalocean']['jumphost']['hostname']}.{config['digitalocean']['domain']}/guacamole"
    guac_username = config['guacamole']['admin_username']
    guac_password = config['guacamole']['admin_password']
    guacmgr = GuacamoleManager(guac_url, guac_username, guac_password)

    parser = argparse.ArgumentParser()

    root_parser = parser.add_subparsers(help='sub-command help', dest='root_cmd')

    map_parser = root_parser.add_parser('map', help='map users to connections')
    map_subparser = map_parser.add_subparsers(help='map help', dest="map_cmd")
    map_add_parser = map_subparser.add_parser('add', help='add mapping from user to connection')
    map_add_parser.add_argument("name")
    map_add_parser.add_argument("password")
    map_automap_parser = map_subparser.add_parser('automap', help='automap users/droplets/connections')

    droplet_parser = root_parser.add_parser('droplet', help='droplet operations')
    droplet_subparser = droplet_parser.add_subparsers(help='droplet help', dest='droplet_cmd')
    droplet_list_parser = droplet_subparser.add_parser('list', help='list droplets')

    droplet_create_parser = droplet_subparser.add_parser('create', help='create a droplet')
    droplet_create_parser.add_argument("name")

    droplet_destroy_parser = droplet_subparser.add_parser('destroy', help='destroy a droplet')
    droplet_destroy_parser.add_argument("droplet_name")

    droplet_reboot_parser = droplet_subparser.add_parser('reboot', help='reboot a droplet')
    droplet_reboot_parser.add_argument("droplet_name")

    guac_parser = root_parser.add_parser('guacamole', help="guacamole operations")
    guac_subparser = guac_parser.add_subparsers(help='guacamole help', dest='guac_cmd')
    guac_conn_parser = guac_subparser.add_parser('connection', help="connections help")
    guac_conn_subparser = guac_conn_parser.add_subparsers(help='guacamole connection help', dest='guac_conn_cmd')
    guac_conn_list_parser = guac_conn_subparser.add_parser('list', help='list connections')
    guac_conn_delete_parser = guac_conn_subparser.add_parser('delete', help='delete a connection')
    guac_conn_delete_parser.add_argument("key")
    guac_conn_create_parser = guac_conn_subparser.add_parser('create', help='create a connection')
    guac_conn_create_parser.add_argument("name")
    guac_conn_create_parser.add_argument("host")
    guac_user_parser = guac_subparser.add_parser('user', help='users help')
    guac_user_subparser = guac_user_parser.add_subparsers(help='guacamole user help', dest='guac_user_cmd')
    guac_user_list_parser = guac_user_subparser.add_parser('list', help='list users')
    guac_user_delete_parser = guac_user_subparser.add_parser('delete', help='delete a user')
    guac_user_delete_parser.add_argument("username")
    guac_user_create_parser = guac_user_subparser.add_parser('create', help="create a user")
    guac_user_create_parser.add_argument("username")
    guac_user_create_parser.add_argument("password")
    guac_user_assign_parser = guac_user_subparser.add_parser('assign', help="assign a connection to a user")
    guac_user_assign_parser.add_argument("username")
    guac_user_assign_parser.add_argument("conn_name")
    guac_user_revoke_parser = guac_user_subparser.add_parser('revoke', help="revoke a connection from a user")
    guac_user_revoke_parser.add_argument("username")
    guac_user_revoke_parser.add_argument("conn_name")

    args = parser.parse_args()
    main(args)