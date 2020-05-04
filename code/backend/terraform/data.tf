data "terraform_remote_state" "aws_core" {
  backend = "s3"

  config = {
    bucket = "rlt-terraform-state"
    key    = "aws-core.tfstate"
    region = "eu-west-3"
  }
}

// the term 'live' here corresponds to the aws account,
// which is currently being used for production and development purposes
// adding this local variable will make the references in other places shorter.
locals {
  core_config = data.terraform_remote_state.aws_core.outputs.account["live"].stack[terraform.workspace]
}

data "aws_ecs_cluster" "private_cluster" {
  cluster_name = local.core_config.ecs_cluster.private.cluster_name
}