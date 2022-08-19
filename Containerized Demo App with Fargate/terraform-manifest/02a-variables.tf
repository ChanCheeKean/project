variable "project_name" {
  description = "Name of project to be created"
  type        = string
  default     = "test-docker"
}

variable "region" {
  description = "Region in which AWS resources to be created"
  type        = string
  default     = "us-east-1"
}

variable "lambda_function_name" {
  description = "Directory for each lambda function"
  type        = string
  default     = "my-docker-dash"
}

locals {
  # if workspace is default then env is dev
  deploy-env = terraform.workspace == "default" ? "dev" : terraform.workspace
}



