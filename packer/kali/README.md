# Kali Packer Configuration

<img alt="Kali Linux" src="https://www.kali.org/images/kali-logo.svg" width="150px"/>

This directory contains the resources required to create a lab box image based on [Kali Linux](https://www.kali.org), an open-source, Debian-based Linux distribution geared towards various information security tasks, such as Penetration Testing, Security Research, Computer Forensics and Reverse Engineering.

---

⚠️ This packer configuration is not in working order right now. You are welcome to submit improvements. Until then, you might prefer to manually create a Kali Linux image following the [official Kali documentation](https://www.kali.org/docs/cloud/digitalocean/).

---

DigitalOcean does not provide any Kali Linux image to build upon. Rather, this Packer configuration will follow the instructions from the Kali Linux website to [build a custom Kali Linux image on DigitalOcean](https://www.kali.org/docs/cloud/digitalocean/):

> A little while ago, they added support for [custom images](https://blog.digitalocean.com/custom-images/), which allows users to import virtual machine disks and use them as droplets. This is perfect for us as we can use our own version of Kali Linux in their cloud.

The configuration in [kali.pkr.hcl](kali.pkr.hcl) uses the [VirtualBox ISO Packer builder](https://developer.hashicorp.com/packer/integrations/hashicorp/virtualbox/latest/components/builder/iso). According to the documentation:

> The builder builds a virtual machine by creating a new virtual machine from scratch, booting it, installing an OS, provisioning software within the OS, then shutting it down. The result of the VirtualBox builder is a directory containing all the files necessary to run the virtual machine portably.

In this case, the builder starts off from the `kali-linux-2024.3-installer-amd64.iso` installation medium and uses [VirtualBox](https://www.virtualbox.org/) to perform the base installation, install the required packages including a graphical environment, and also installs a remote desktop service (provided by [xrdp](https://www.xrdp.org/)) to allow connections from the jumphost.

Finally, the newly created image is imported as a custom image into DigitalOcean. For this, the Packer configuration uses the [DigitalOcean Import post-processor](https://developer.hashicorp.com/packer/integrations/digitalocean/digitalocean/latest/components/post-processor/digitalocean-import). This steps requires DigitalOcean's [Spaces Object Storage](https://www.digitalocean.com/products/spaces) as a temporary staging area for the image before it is imported as a custom image. This image can then be used to spin up lab boxes on DigitalOcean.

## Prerequisites

 1. This Packer configuration depends on [VirtualBox](https://www.virtualbox.org/). You will need to install it on your system prior to running the builder.
 2. The builder uses DigitalOcean's Spaces Object Storage to upload the newly built image. You will need to create a Spaces Bucket and provide the `spaces_name`, `spaces_region`, `spaces_key`, and `spaces_secret` values in [config.yaml](../config.yaml) accordingly. See [How to Create a Spaces Bucket](https://docs.digitalocean.com/products/spaces/how-to/create/) and [How to Manage Administrative Access to Spaces](https://docs.digitalocean.com/products/spaces/how-to/manage-access/) for details.

## Usage

If this is the first time invoking `packer`, you need to initialize it:
```bash
$ packer init kali.pkr.hcl
```

Then, to build the image, run this:
```bash
$ packer build kali.pkr.hcl
```

Get yourself a cup of 🍵, the build process takes 30-60 mins depending on your system configuration, uploading the image may take another 20 mins based on your network speed, and finally the custom image import can take up to 1 hour.