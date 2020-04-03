terraform {
  required_version = "> 0.12.0"

  backend "s3" {
    bucket = "rlt-terraform-state"
    key    = "noe-backend.tfstate"
    region = "eu-west-3"
  }
}
