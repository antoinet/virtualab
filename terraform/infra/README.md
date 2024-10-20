# Lab Infrastructure

This terraform configuration will deploy all resources needed during lab operation:

 * network
 * loadbalancer (serves as a HTTPS termination with the Let's Encrypt certificate)
 * firewall rules
 * jumphost
 * labbox droplets

**Note**: these resources will generate significant costs, especially when operating a large number of labbox droplets. Make sure to destroy the infra after use.


## Prerequisites

 1. Prior to deploying the infrastructure resources, make sure to deploy the resources in the [setup folder](../setup/) first.
 2. Images for the jumphost and the labboxes must be created before you can spin up the corresponding droplets. See instructions in the [packer](../../packer/) folder for details.

## Usage
If this is the first time invoking `terraform` in this folder, you need to initialize it:
```bash
$ terraform init
```

To spin up the lab infrastructure, simply execute the following command:
```bash
$ terraform apply
```

To decommission the lab infrastructure, use this command:
```bash
$ terraform destroy
```