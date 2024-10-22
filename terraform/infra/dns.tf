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

# DNS zone for the lab domain
data "digitalocean_domain" "lab_domain" {
  name = local.config["digitalocean"]["domain"]
}

# hardcoded DNS record for the guacamole host (e.g. for direct connection via ssh)
resource "digitalocean_record" "guacamole" {
  name   = "guacamole"
  domain = data.digitalocean_domain.lab_domain.id
  type   = "A"
  value  = digitalocean_droplet.jumphost.ipv4_address
  ttl    = 300
}

# DNS record for the the loadbalancer (used for HTTPS with the let's encrypt cert)
resource "digitalocean_record" "loadbalancer" {
  name   = local.config["digitalocean"]["jumphost"]["hostname"]
  domain = data.digitalocean_domain.lab_domain.id
  type   = "A"
  value  = digitalocean_loadbalancer.virtualab-https-endpoint.ip
  ttl    = 300
}

# DNS records for the individual labboxes
resource "digitalocean_record" "labbox" {
  count  = length(digitalocean_droplet.labbox)
  domain = data.digitalocean_domain.lab_domain.id
  type   = "A"
  name   = "${local.config["digitalocean"]["labbox"]["hostname_prefix"]}-${count.index + 1}"
  value  = digitalocean_droplet.labbox[count.index].ipv4_address
  ttl    = 300
}