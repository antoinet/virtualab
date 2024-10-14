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

packer {
  required_plugins {
    digitalocean = {
      version = ">= 1.0.4"
      source  = "github.com/digitalocean/digitalocean"
    }
  }
}

locals {
  config = yamldecode(file("${path.root}/../../config.yaml"))
}

source "digitalocean" "jumphost-source" {
  api_token        = local.config["digitalocean"]["token"]
  image            = "ubuntu-24-04-x64"
  region           = local.config["digitalocean"]["region"]
  size             = local.config["digitalocean"]["jumphost"]["droplet_size"]
  ssh_username     = "root"
  droplet_name     = "jumphost-packer-build"
  snapshot_name    = local.config["digitalocean"]["jumphost"]["snapshot_name"]
  snapshot_regions = [local.config["digitalocean"]["region"]]
  tags             = ["packer", "jumphost"]
}

build {
  sources = ["source.digitalocean.jumphost-source"]

  # finish booting to avoid issues with apt-get locks
  # https://developer.hashicorp.com/packer/docs/debugging#issues-installing-ubuntu-packages
  provisioner "shell" {
    inline = [
      "echo waiting for cloud-init to finish...",
      "cloud-init status --wait",
    ]
    valid_exit_codes = [0, 2]
  }

  provisioner "shell" {
    inline = [
      "groupadd -g 1001 ubuntu",
      "useradd ubuntu -m -g 1001 -u 1001 -s /bin/bash",
      "usermod -aG sudo ubuntu",
      "echo \"ubuntu ALL=(ALL) NOPASSWD: ALL\" > /etc/sudoers.d/ubuntu"
    ]
  }

  # retrieve the forked Guacamole-Installer (modified from itiligent/Guacamole-Installer)
  provisioner "shell" {
    inline = [
      "cd /home/ubuntu",
      "wget https://raw.githubusercontent.com/antoinet/Guacamole-Installer/main/1-setup.sh"
    ]
  }

  # replace shell variables
  provisioner "shell" {
    inline = [
      "cd /home/ubuntu",
      "sed -i 's/^SERVER_NAME=\"\"/SERVER_NAME=\"${local.config["digitalocean"]["jumphost"]["hostname"]}\"/' 1-setup.sh",
      "sed -i 's/^LOCAL_DOMAIN=\"\"/LOCAL_DOMAIN=\"${local.config["digitalocean"]["domain"]}\"/' 1-setup.sh",
      "sed -i 's/^INSTALL_MYSQL=\"\"/INSTALL_MYSQL=\"true\"/' 1-setup.sh",
      "sed -i 's/^SECURE_MYSQL=\"\"/SECURE_MYSQL=\"false\"/' 1-setup.sh",
      "sed -i 's/^MYSQL_ROOT_PWD=\"\"/MYSQL_ROOT_PWD=\"password\"/' 1-setup.sh",
      "sed -i 's/^GUAC_PWD=\"\"/GUAC_PWD=\"password\"/' 1-setup.sh",
      "sed -i 's/^INSTALL_TOTP=\"\"/INSTALL_TOTP=\"false\"/' 1-setup.sh",
      "sed -i 's/^INSTALL_DUO=\"\"/INSTALL_DUO=\"false\"/' 1-setup.sh",
      "sed -i 's/^INSTALL_LDAP=\"\"/INSTALL_LDAP=\"false\"/' 1-setup.sh",
      "sed -i 's/^INSTALL_QCONNECT=\"\"/INSTALL_QCONNECT=\"false\"/' 1-setup.sh",
      "sed -i 's/^INSTALL_HISTREC=\"\"/INSTALL_HISTREC=\"false\"/' 1-setup.sh",
      "sed -i 's/^GUAC_URL_REDIR=\"\"/GUAC_URL_REDIR=\"true\"/' 1-setup.sh",
      "sed -i 's/^INSTALL_NGINX=\"\"/INSTALL_NGINX=\"false\"/' 1-setup.sh",
      "sed -i 's/^PROXY_SITE=\"\"/PROXY_SITE=\"${local.config["digitalocean"]["jumphost"]["hostname"]}.${local.config["digitalocean"]["domain"]}\"/' 1-setup.sh",
      "sed -i 's/^SELF_SIGN=\"\"/SELF_SIGN=\"false\"/' 1-setup.sh",
      "sed -i 's/^LETS_ENCRYPT=\"\"/LETS_ENCRYPT=\"false\"/' 1-setup.sh",
      "sed -i 's/^LE_DNS_NAME=\"\"/LE_DNS_NAME=\"${local.config["digitalocean"]["jumphost"]["hostname"]}.${local.config["digitalocean"]["domain"]}\"/' 1-setup.sh",
      "sed -i 's/^LE_EMAIL=\"\"/LE_EMAIL=\"nobody@example.com\"/' 1-setup.sh",
      "sed -i 's/^BACKUP_EMAIL=\"\"/BACKUP_EMAIL=\"nobody@example.com\"/' 1-setup.sh",
    ]
  }

  # run the Guacamole-Installer as ubuntu
  provisioner "shell" {
    inline = [
      "cd /home/ubuntu",
      "chown ubuntu:ubuntu 1-setup.sh",
      "chmod +x 1-setup.sh",
      "su - ubuntu -c ./1-setup.sh"
    ]
  }

  # apply the virtualab branding
  provisioner "file" {
    source      = "files/branding.jar"
    destination = "/etc/guacamole/extensions/branding.jar"
  }
}
