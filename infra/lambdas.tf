module "lambda_connection_state_store" {
  source = "./lambda_module"

  lambda_name           = "connection-state-store"
  policy_path           = "./iam_policies/policy_connection_state_store.json"
  subnet_ids            = var.subnet_ids
  vpc_security_group_id = aws_security_group.vpc_sg.id
}

module "lambda_notification_eligibility" {
  source = "./lambda_module"

  lambda_name           = "notification-eligibility"
  policy_path           = "./iam_policies/policy_notification_eligibility.json"
  subnet_ids            = var.subnet_ids
  vpc_security_group_id = aws_security_group.vpc_sg.id
}

module "lambda_send_notifications" {
  source = "./lambda_module"

  lambda_name           = "send-notifications"
  policy_path           = "./iam_policies/policy_send_notifications.json"
  subnet_ids            = var.subnet_ids
  vpc_security_group_id = aws_security_group.vpc_sg.id
}
