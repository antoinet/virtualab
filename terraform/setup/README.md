# Lab Setup

This terraform configuration will deploy permament/"immortal" resources use for `virtualab`:

 * the digitalocean project `virtualab`
 * a DNS zone for the lab domain
 * a Let's Encrypt certificate

**Note**: these resources do not generate any costs.

# Prerequisites
You need to delegate your lab DNS domain to digitalocean. For details, see the setup instructions.