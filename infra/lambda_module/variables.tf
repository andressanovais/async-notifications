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
