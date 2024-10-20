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

# refer to https://github.com/ridvanaltun/guacamole-rest-api-documentation

import requests

class GuacamoleManager:

    def __init__(self, url, username, password):
        self.url = url
        self.token, self.datasource = GuacamoleManager.authenticate(self.url, username, password)

    @staticmethod
    def authenticate(url, username, password):
        url = f"{url}/api/tokens"
        params = {'username': username, 'password': password}
        r = requests.post(url, data=params)
        r.raise_for_status()
        return r.json().get('authToken'),\
            r.json().get('dataSource')

    def base_request(self, api_endpoint, method="GET", json=None):
        url = f"{self.url}/api/session/data/{self.datasource}/{api_endpoint}"
        params = {'token': self.token}
        r = requests.request(method, url, params=params, json=json)
        r.raise_for_status()
        if r.text:
            return r.json()
        return {}

    def list_connections(self):
        return self.base_request("connections")
    
    def list_connections_with_parameters(self):
        res = []
        for key, conn in self.list_connections().items():
            d = {
                'key': conn['identifier'], 
                'name': conn['name'], 
                'protocol': conn['protocol']
            }
            d.update(self.connection_parameters(key))
            res.append(d)
        return res

    def connection_details(self, conn_id):
        return self.base_request(f"connections/{conn_id}")

    def connection_parameters(self, conn_id):
        return self.base_request(f"connections/{conn_id}/parameters")
    
    def delete_connection(self, conn_id):
        self.base_request(f"connections/{conn_id}", method="DELETE")
    
    def create_connection(self, name, ip_address, rdp_username, rdp_password):
        conn_parameters = {
            "parentIdentifier": "ROOT",
            "name": name,
            "protocol": "rdp",
            "parameters": {
                "port": "3389",
                "read-only": "",
                "swap-red-blue": "",
                "cursor": "",
                "color-depth": "",
                "clipboard-encoding": "",
                "disable-copy": "",
                "disable-paste": "",
                "dest-port": "",
                "recording-exclude-output": "",
                "recording-exclude-mouse": "",
                "recording-include-keys": "",
                "create-recording-path": "",
                "enable-sftp": "",
                "sftp-port": "",
                "sftp-server-alive-interval": "",
                "enable-audio": "",
                "security": "",
                "disable-auth": "",
                "ignore-cert": "",
                "gateway-port": "",
                "server-layout": "",
                "timezone": "",
                "console": "",
                "width": "",
                "height": "",
                "dpi": "",
                "resize-method": "",
                "console-audio": "",
                "disable-audio": "",
                "enable-audio-input": "",
                "enable-printing": "",
                "enable-drive": "",
                "create-drive-path": "",
                "enable-wallpaper": "",
                "enable-theming": "",
                "enable-font-smoothing": "",
                "enable-full-window-drag": "",
                "enable-desktop-composition": "",
                "enable-menu-animations": "",
                "disable-bitmap-caching": "",
                "disable-offscreen-caching": "",
                "disable-glyph-caching": "",
                "preconnection-id": "",
                "hostname": ip_address,
                "username": rdp_username,
                "password": rdp_password,
                "domain": "",
                "gateway-hostname": "",
                "gateway-username": "",
                "gateway-password": "",
                "gateway-domain": "",
                "initial-program": "",
                "client-name": "",
                "printer-name": "",
                "drive-name": "",
                "drive-path": "",
                "static-channels": "",
                "remote-app": "",
                "remote-app-dir": "",
                "remote-app-args": "",
                "preconnection-blob": "",
                "load-balance-info": "",
                "recording-path": "",
                "recording-name": "",
                "sftp-hostname": "",
                "sftp-host-key": "",
                "sftp-username": "",
                "sftp-password": "",
                "sftp-private-key": "",
                "sftp-passphrase": "",
                "sftp-root-directory": "",
                "sftp-directory": ""
            },
            "attributes": {
                "max-connections": "1",
                "max-connections-per-user": "1",
                "weight": "",
                "failover-only": "",
                "guacd-port": "",
                "guacd-encryption": "",
                "guacd-hostname": ""
            }
        }
        return self.base_request("connections", method="POST", json=conn_parameters)
    
    def resolve_connection_by_name(self, conn_name):
        for key, data in self.list_connections().items():
            if data['name'] == conn_name:
                return key
        return None

    def list_users(self):
        return self.base_request("users")
    
    def user_permissions(self, username):
        return self.base_request(f"users/{username}/permissions")
    
    def list_users_with_permissions(self):
        res = []
        for username, details in self.list_users().items():
            d = {'username': details['username'], 'lastActive': details.get('lastActive', 0)}
            d['connectionPermissions'] = []
            for conn_id in self.user_permissions(username)['connectionPermissions'].keys():
                conn = self.connection_details(conn_id)
                d['connectionPermissions'].append({
                    "key": conn['identifier'],
                    "name": conn['name']
                })
            res.append(d)
        return res
    
    def delete_user(self, username):
        self.base_request(f"users/{username}", method="DELETE")

    def change_password(self, username, old_password, new_password):
        payload = {
            "oldPassword": old_password,
            "newPassword": new_password
        }
        self.base_request(f"users/{{username}}/password", method="PUT", json=payload)
    
    def create_user(self, username, password):
        data = {
            "username": username,
            "password": password,
            "attributes": {
                "disabled": "",
                "expired": "",
                "access-window-start": "",
                "access-window-end": "",
                "valid-from": "",
                "valid-until": "",
                "timezone": None,
                "guac-full-name": "",
                "guac-organization": "",
                "guac-organizational-role": ""
            }
        }
        return self.base_request("users", method="POST", json=data)
    
    def assign_user_to_connection(self, username, conn_id):
        body = [
            {
                "op": "add",
                "path": f"/connectionPermissions/{conn_id}",
                "value": "READ"
            }
        ]
        self.base_request(f"users/{username}/permissions", method="PATCH", json=body)
    
    def revoke_user_from_connection(self, username, conn_id):
        body = [
            {
                "op": "remove",
                "path": f"/connectionPermissions/{conn_id}",
                "value": "READ"
            }
        ]
        self.base_request(f"users/{username}/permissions", method="PATCH", json=body)
