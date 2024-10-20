![VirtuaLab](assets/virtualab-logo.png)

Virtua Lab lets you build your own cloud virtual machine lab, whether you want to teach a class,
train professionals, run a hackathon, host a hands-on-lab, etc.

The lab infrastructure runs on DigitalOcean infrastructure. It
consists of a jumphost running [Apache Guacamole](https://guacamole.apache.org/) and as many
lab boxes as you want (or can) spin up.

## Architecture

![VirtuaLab Architecture](assets/virtualab.drawio.png)


## Prerequisites

You will need the following software to build the lab:

 * [Terraform](https://www.terraform.io/), or alternatively [OpenTofu](https://opentofu.org/) (not tested) to provision the DigitalOcean resources
 * [Packer](https://www.packer.io/) to create the VM images (jumphost and lab boxes)
 * [VirtualBox](https://www.virtualbox.org/)
 * [Python 3](https://www.python.org/)

Obviously, you will also need a DigitalOcean subscription. Get $200 of credit using the following link:

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=1ec7baf80a5d&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

## Setup Instructions

### 1 Configuration File

Copy `config.yaml.example` to `config.yaml`. This is where all the lab's configuration settings are stored.

### 2 DigitalOcean Personal Access Token

Create a full access personal access token and store it in `config.yaml` under `digitalocean.token`.

For details follow the instructions at [How to Create a Personal Access Token](https://docs.digitalocean.com/reference/api/create-personal-access-token/).

### 3 DNS Setup

You need to delegate your lab DNS domain to digitalocean. To update your domain's delegation,
set the following name server addresses at your registrar:

```
ns1.digitalocean.com
ns2.digitalocean.com
ns3.digitalocean.com
```

For details, see: [Point to DigitalOcean Name Servers From Common Domain Registrars](https://docs.digitalocean.com/products/networking/dns/getting-started/dns-registrars/).

Store the lab domain name in `config.yaml` under `digitalocean.domain`.


### 4 Add an SSH key

Add at least one SSH key to your DigitalOcean account. This will be used to access your running droplets. See [How to Add SSH Public Keys to DigitalOcean](https://docs.digitalocean.com/platform/teams/upload-ssh-keys/) for details.

By default the expected name of the SSH key is `terraform`. You can change this in `config.yaml` under `digitalocean.ssh_key_name`.

### 5 Create Droplet Images

For the lab operation, you will need to create at least two virtual machine images for the jumphost and the lab boxes.

#### 5.1 Create the Jumphost Image

See the instructions under [packer/jumphost](packer/jumphost/) to create the jumphost image. You will find corresponding configuration settings in `config.yaml` under `digitalocean.jumphost`.

#### 5.2 Create the Lab Box Image

The lab boxes are based on a snapshot or custom image of your choice. There is an example of a [Kali Linux](https://www.kali.org) image under [packer/kali](packer/kali/). You will find corresponding configuration settings in `config.yaml` under `digitalocean.labbox`.

### 6 Deploy the Initial Cloud Setup

See instructions under [terraform/setup](terraform/setup/) to deploy the initial cloud setup (e.g. DNS domain, certificate, lab project, etc).

### 7 Deploy the Lab Infrastructure

See instructions under [terraform/infra](terraform/infra/) to deploy the lab infrastructure. You can sepcify the number of lab boxes to deploy in `config.yaml` under `digitalocean.labbox.count`.

### 8 Provision Users and Connections

The last step consists in provisioning users on the jumphost and setting up corresponding RDP connections. This is achieved with the script in [utils/labmanger](utils/labmanager/).

## Tips / Tricks

### Increase Droplet Limit

If you need to create more droplets than your current limit allows, you can request an increase. See [How do I increase my Droplet limit?](https://www.digitalocean.com/community/questions/how-do-i-increase-my-droplet-limit) for details.

### DNS Negative TTL

After destroying the lab infrastructure and removing the corresponding DNS records, any DNS resolver will start caching the inexistent records as negative results. This means that if you redeploy the lab in short time, it will not be reachable for the time specicied by the TTL. The TTL is defined in [terraform/infra/dns.tf](terraform/infra/dns.tf) with a value of 300s (5mins).