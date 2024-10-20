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

data "digitalocean_droplet_snapshot" "labbox_snapshot" {
  name   = local.config["digitalocean"]["labbox"]["snapshot_name"]
  region = local.config["digitalocean"]["region"]
}


resource "digitalocean_droplet" "labbox" {
  image    = data.digitalocean_droplet_snapshot.labbox_snapshot.id
  count    = local.config["digitalocean"]["labbox"]["count"]
  name     = "${local.config["digitalocean"]["labbox"]["droplet_name_prefix"]}-${count.index + 1}"
  region   = local.config["digitalocean"]["region"]
  size     = local.config["digitalocean"]["labbox"]["droplet_size"]
  vpc_uuid = digitalocean_vpc.virtualab-network.id
  ssh_keys = [data.digitalocean_ssh_key.terraform.id]

  tags       = ["labbox"]
  depends_on = [digitalocean_vpc.virtualab-network]
}

resource "digitalocean_project_resources" "labbox" {
  project   = data.digitalocean_project.virtualab.id
  resources = digitalocean_droplet.labbox[*].urn
}
