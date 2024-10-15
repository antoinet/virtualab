# Terraform Configuration Files

You will find two folders here:

 * [setup](setup/): contains permanent resources for the lab setup (e.g. project, DNS zone, X.509 certificate). Start by deploying this.
 * [infra](infra/): contains the resource definitions for the lab infrastructure. Deploy this to spin up the network, jumphost and lab boxes.