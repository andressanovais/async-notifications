module "lambda_connection_storage" {
  source = "./lambda_module"

  lambda_name           = "connection-storage"
  policy_path           = "./iam_policies/policy_connection_storage.json"
  subnet_ids            = var.subnet_ids
  vpc_security_group_id = aws_security_group.vpc_sg.id

  environment_variables = {
    elasticache_host = var.elasticache_host,
    elasticache_port = var.elasticache_port,
    elasticache_secret_name = var.elasticache_secret_name
  }
}

module "lambda_notification_eligibility" {
  source = "./lambda_module"

  lambda_name           = "notification-eligibility"
  policy_path           = "./iam_policies/policy_notification_eligibility.json"
  subnet_ids            = var.subnet_ids
  vpc_security_group_id = aws_security_group.vpc_sg.id

  environment_variables = {
    elegibility_table_name = var.dynamo_table_name,
    lambda_to_schedule_arn = module.lambda_send_notifications.arn,
    scheduler_role_arn = aws_iam_role.scheduler_role.arn
  }
}

module "lambda_send_notifications" {
  source = "./lambda_module"

  lambda_name           = "send-notifications"
  policy_path           = "./iam_policies/policy_send_notifications.json"
  subnet_ids            = var.subnet_ids
  vpc_security_group_id = aws_security_group.vpc_sg.id

  environment_variables = {
    elasticache_host = var.elasticache_host,
    elasticache_port = var.elasticache_port,
    elasticache_secret_name = var.elasticache_secret_name,
    websocket_url = aws_apigatewayv2_stage.default.invoke_url
  }
}
