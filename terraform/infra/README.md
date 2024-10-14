# Lab Infrastructure

This terraform configuration will deploy all resources needed during lab operation:

 * network
 * loadbalancer (serves as a HTTPS termination with the Let's Encrypt certificate)
 * firewall rules
 * jumphost
 * labbox droplets

**Note**: these resources will generate significant costs, especially when operating a large number of labbox droplets.
Make sure to destroy the infra after use:
```
$ terraform destroy
```

## Prerequisites
Prior to deploying the infrastructure resources, make sure to apply the terraform resources in the setup first.