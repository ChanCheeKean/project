
/* 
terraform init
terraform fmt
terraform workspace new prod
terraform workspace list
terraform workspace select prod
terraform apply -auto-approve
*/

# Terraform Block
terraform {
  required_version = "~> 1.2.2"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.0"
    }
  }
}

# Provider Block
provider "aws" {
  region  = var.region
  profile = "default"
}