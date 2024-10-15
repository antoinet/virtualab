# Jumphost Packer Configuration

<img alt="Apache Guacamole" src="https://guacamole.apache.org/images/logos/guac-classic-logo.svg" width="100px"/>

This directory contains the resources required to create the jumphost image. It's based on a plain [Ubuntu Linux](https://ubuntu.com/) image, on which [Apache Guacamole](https://guacamole.apache.org/) is installed.

The configuration in [jumphost.pkr.hcl](jumphost.pkr.hcl) uses the [DigitalOcean Packer builder](https://developer.hashicorp.com/packer/integrations/digitalocean/digitalocean/latest/components/builder/digitalocean). According to the documentation:

> The builder takes a source image, runs any provisioning necessary on the image after launching it, then snapshots it into a reusable image. This reusable image can then be used as the foundation of new servers that are launched within DigitalOcean.

In this case, the builder spins up a `ubuntu-24-04-x64` base image from DigitalOcean, applies a modified version of [itiligent/Guacamole-Installer](https://github.com/itiligent/Guacamole-Installer) and saves it as a snapshot. For lab operation, the jumphost is spun up from this snapshot.

## Usage
If this is the first time invoking `packer`, you need to initialize it:
```bash
$ packer init
```

To create the jumphost image, simply execute the following command:
```bash
$ packer build jumphost.pkr.hcl
```