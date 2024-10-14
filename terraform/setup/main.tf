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

terraform {
  required_providers {

    # DigitalOcean Provider
    # https://registry.terraform.io/providers/digitalocean/digitalocean/latest/docs
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.42.0"
    }
  }
}

# Decode the YAML configuration file
locals {
  config = yamldecode(file("${path.module}/../../config.yaml"))
}

provider "digitalocean" {
  token = local.config["digitalocean"]["token"]
}

resource "digitalocean_project" "virtualab" {
  name = local.config["digitalocean"]["project_name"]
}

# DNS zone for the lab domain
resource "digitalocean_domain" "lab_domain" {
  name = local.config["digitalocean"]["domain"]
}

# the loadbalancer is used to serve guacamole with a secure
# connection using a let's encrypt certificate
resource "digitalocean_certificate" "cert" {
  name = "virtualab-cert"
  type = "lets_encrypt"

  #domains = [digitalocean_record.loadbalancer.fqdn] # results in a cycle
  domains = [ "${local.config["digitalocean"]["jumphost"]["hostname"]}.${local.config["digitalocean"]["domain"]}" ]
}

resource "digitalocean_project_resources" "lab_domain" {
  project = digitalocean_project.virtualab.id
  resources = [digitalocean_domain.lab_domain.urn]
}