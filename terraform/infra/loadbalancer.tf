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

# the loadbalancer is used to serve guacamole with a secure
# connection using a let's encrypt certificate
data "digitalocean_certificate" "cert" {
  name = "virtualab-cert"
}

resource "digitalocean_loadbalancer" "virtualab-https-endpoint" {
  name                             = "virtualab-https-endpoint"
  region                           = local.config["digitalocean"]["region"]
  size_unit                        = 1
  redirect_http_to_https           = true
  project_id                       = data.digitalocean_project.virtualab.id
  vpc_uuid                         = digitalocean_vpc.virtualab-network.id
  disable_lets_encrypt_dns_records = true

  forwarding_rule {
    entry_port     = 443
    entry_protocol = "https"

    target_port     = 8080
    target_protocol = "http"

    certificate_name = data.digitalocean_certificate.cert.name
  }

  healthcheck {
    port     = 8080
    protocol = "http"
    path     = "/guacamole/"
  }

  droplet_ids = [digitalocean_droplet.jumphost.id]
}