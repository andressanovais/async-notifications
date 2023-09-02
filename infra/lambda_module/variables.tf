variable "lambda_name" {
  type = string
}

variable "lambda_runtime" {
  type    = string
  default = "python3.11"
}

variable "policy_path" {
  type = string
}

variable "subnet_ids" {
  type    = list(string)
  default = null
}

variable "vpc_security_group_id" {
  type    = string
  default = null
}

variable "lambda_base_policy_arn" {
  type = string
}

variable "environment_variables" {
  type        = map(string)
  description = "A map that defines environment variables for the Lambda Function."
}