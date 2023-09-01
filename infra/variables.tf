variable "vpc_id" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "dynamo_table_name" {
  type = string
}

variable "dynamo_rcu" {
  type = string
}

variable "dynamo_wcu" {
  type = string
}
