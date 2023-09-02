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


resource "aws_iam_role" "scheduler_role" {
  name = "${var.lambda_name}_policy"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "scheduler.amazonaws.com"
      },
      "Effect": "Allow",
    }
  ]
}
EOF
}

resource "aws_iam_policy" "scheduler_policy" {
  name   = "invoke_send_notifications_policy"
  policy = file(var.policy_path)
}

resource "aws_iam_role_policy_attachment" "scheduler_role_policy" {
  role       = aws_iam_role.scheduler_role.name
  policy_arn = aws_iam_policy.scheduler_policy.arn
}
