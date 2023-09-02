provider "aws" {
  access_key                  = "mock_access_key"
  region                      = "sa-east-1"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    dynamodb    = "http://localhost:4566"
    lambda      = "http://localhost:4566"
    cloudwatch  = "http://localhost:4566"
    iam         = "http://localhost:4566"
    logs        = "http://localhost:4566"
    ssm         = "http://localhost:4566"
    eventbridge = "http://localhost:4566"
  }
}

resource "aws_security_group" "vpc_sg" {
  name_prefix = "vpc_sg"
  vpc_id      = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "vpc_sg_ingress" {
  security_group_id = aws_security_group.vpc_sg.id

  cidr_ipv4   = var.vpc_cidr
  from_port   = 0
  to_port     = 65535
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "vpc_sg_egress" {
  security_group_id = aws_security_group.vpc_sg.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 0
  to_port     = 65535
  ip_protocol = "tcp"
}
