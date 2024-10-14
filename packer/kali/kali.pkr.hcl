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
        virtualbox = {
          version = "~> 1"
          source  = "github.com/hashicorp/virtualbox"
        }
    }
}


locals {
  config = yamldecode(file("${path.root}/../../config.yaml"))
}

source "virtualbox-iso" "kali-source" {
  boot_wait = "10s"
  boot_command       = [
    "<esc><wait>",
    "auto preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg country=CH ",
    "language=en priority=critical keymap=en local=en_US keymap=us hostname=kali domain=''<enter>"
  ]
  # net install
  #iso_url = "https://cdimage.kali.org/kali-2024.3/kali-linux-2024.3-installer-netinst-amd64.iso",
  #iso_url = "files/kali-linux-2024.3-installer-netinst-amd64.iso"
  #iso_checksum         = "sha256:793061c7367d4c3c89d1e8ebf849ee00386297f5ebaeeaf6d9b37ae9857d2e53"

  # installer disc
  # iso_url = "https://cdimage.kali.org/kali-2024.3/kali-linux-2024.3-installer-amd64.iso"
  iso_url = "files/kali-linux-2024.3-installer-amd64.iso"
  iso_checksum = "sha256:2ba1abf570ea0685ca4a97dd9c83a65670ca93043ef951f0cd7bbff914fa724a"

  vm_name              = "kali"
  headless             = "false"
  http_directory       = "http"
  guest_os_type        = "Debian_64"
  memory = 4096
  cpus = 2
  disk_size            = 20480
  output_directory     = "output"
  guest_additions_mode = "disable"
  shutdown_command     = "echo 'kali' | sudo -S shutdown -P now"
  #format               = "ova"
  ssh_username         = "kali"
  ssh_password         = "kali"
  ssh_port             = 22
  ssh_wait_timeout     = "30m"
  vboxmanage = [
    ["modifyvm", "{{ .Name }}", "--audio", "none"],
    ["modifyvm", "{{ .Name }}", "--usb", "off"],
    ["modifyvm", "{{ .Name }}", "--vram", "12"],
    ["modifyvm", "{{ .Name }}", "--vrde", "off"],
    ["modifyvm", "{{ .Name }}", "--nictype1", "virtio"]
  ]
}


build {
    sources = ["source.virtualbox-iso.kali-source"]
}