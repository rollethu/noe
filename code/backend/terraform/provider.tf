
// for the time being we're using one AWS account and separating dev/live environments by aws region
locals {
  env_regions = {
    dev  = "eu-west-1"
    live = "eu-west-3"
    prod = "eu-west-3"
    noe  = "eu-central-1"
  }
}

provider "aws" {
  region = local.env_regions[terraform.workspace]
}
