# Kali Packer Configuration

<img alt="Kali Linux" src="https://www.kali.org/images/kali-logo.svg" width="150px"/>

This directory contains the resources required to create a lab box image based on [Kali Linux](https://www.kali.org), an open-source, Debian-based Linux distribution geared towards various information security tasks, such as Penetration Testing, Security Research, Computer Forensics and Reverse Engineering.

DigitalOcean does not provide any Kali Linux image to build upon. Rather, this Packer configuration will follow the instructions from the Kali Linux website to [build a custom Kali Linux image on DigitalOcean](https://www.kali.org/docs/cloud/digitalocean/):

> A little while ago, they added support for [custom images](https://blog.digitalocean.com/custom-images/), which allows users to import virtual machine disks and use them as droplets. This is perfect for us as we can use our own version of Kali Linux in their cloud.

The configuration in [kali.pkr.hcl](kali.pkr.hcl) uses the [VirtualBox ISO Packer builder](https://developer.hashicorp.com/packer/integrations/hashicorp/virtualbox/latest/components/builder/iso). According to the documentation:

> The builder builds a virtual machine by creating a new virtual machine from scratch, booting it, installing an OS, provisioning software within the OS, then shutting it down. The result of the VirtualBox builder is a directory containing all the files necessary to run the virtual machine portably.

In this case, the builder starts off from the `kali-linux-2024.3-installer-amd64.iso` installation medium and uses [VirtualBox](https://www.virtualbox.org/) to perform the base installation, install the required packages including a graphical environment, and finally also installs a remote desktop service (provided by [xrdp](https://www.xrdp.org/)), to allow connections from the jumphost.

Finally, the newly created image needs to get imported as a custom image into DigitalOcean. For this task, the Packer configuration uses the [DigitalOcean Import post-processor](https://developer.hashicorp.com/packer/integrations/digitalocean/digitalocean/latest/components/post-processor/digitalocean-import). This steps requires a [DigitalOcean Spaces Object Storage](https://www.digitalocean.com/products/spaces) account as a temporary staging area for the image before it is imported as a custom image. This image can be used to spin up lab boxes.

## Usage
If this is the first time invoking `packer`, you need to initialize it:
```bash
$ packer init
```

This Packer configuration depends on [VirtualBox](https://www.virtualbox.org/). You will need to install the software prior to running the builder. You will also need to provide the `spaces_key`, `spaces_secret`, and `spaces_region` configuration values in [config.yaml](../config.yaml) according to your DigitalOcean Spaces Object Storage account.

```bash
$ packer build kali.pkr.hcl
```

Get yourself a cup of 🍵, the build process takes 30-60 mins depending on your system configuration and network speed.