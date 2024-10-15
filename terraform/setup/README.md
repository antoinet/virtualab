# Lab Setup

This terraform configuration will deploy permament/"immortal" resources use for `virtualab`:

 * the digitalocean project `virtualab`
 * a DNS zone for the lab domain
 * a Let's Encrypt certificate

**Note**: these resources do not generate any costs.

## Prerequisites
You need to delegate your lab DNS domain to digitalocean. For details, see the [setup instructions](../README.md).

## Usage
If this is the first time invoking `terraform`, you need to initialize it:
```bash
$ terraform init
```

To set up the resources, simply execute the following command:
```bash
$ terraform apply
```

As mentioned above, the resources in this folder are intended to be permanent. Eventually, if you definitely want to delete all virtualab resources, use this command:
```bash
$ terraform destroy
```