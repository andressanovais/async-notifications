module "lambda_connection_storage" {
  source = "./lambda_module"

  lambda_name            = "connection_storage"
  policy_path            = "./iam_policies/policy_connection_storage.json"
  lambda_base_policy_arn = aws_iam_policy.lambda_base_policy.arn
  lambda_layer_arn       = aws_lambda_layer_version.lambda_layer.arn

  subnet_ids            = var.subnet_ids
  vpc_security_group_id = aws_security_group.vpc_sg.id

  environment_variables = {
    elasticache_host        = var.elasticache_host,
    elasticache_port        = var.elasticache_port,
    elasticache_secret_name = var.elasticache_secret_name
  }
}

module "lambda_notification_eligibility" {
  source = "./lambda_module"

  lambda_name            = "notification_eligibility"
  policy_path            = "./iam_policies/policy_notification_eligibility.json"
  lambda_base_policy_arn = aws_iam_policy.lambda_base_policy.arn
  lambda_layer_arn       = aws_lambda_layer_version.lambda_layer.arn

  subnet_ids            = var.subnet_ids
  vpc_security_group_id = aws_security_group.vpc_sg.id

  environment_variables = {
    elegibility_table_name = var.dynamo_table_name,
    lambda_to_schedule_arn = module.lambda_send_notifications.arn,
    scheduler_role_arn     = aws_iam_role.scheduler_role.arn
  }
}

module "lambda_send_notifications" {
  source = "./lambda_module"

  lambda_name            = "send_notifications"
  policy_path            = "./iam_policies/policy_send_notifications.json"
  lambda_base_policy_arn = aws_iam_policy.lambda_base_policy.arn
  lambda_layer_arn       = aws_lambda_layer_version.lambda_layer.arn

  subnet_ids            = var.subnet_ids
  vpc_security_group_id = aws_security_group.vpc_sg.id

  environment_variables = {
    elasticache_host        = var.elasticache_host,
    elasticache_port        = var.elasticache_port,
    elasticache_secret_name = var.elasticache_secret_name,
    websocket_url           = aws_apigatewayv2_stage.default.invoke_url
  }
}

resource "null_resource" "zipfile" {
  provisioner "local-exec" {
    interpreter = ["C:/Program Files/Git/bin/bash", "-c"]
    command     = "./zip_layer.sh"
    environment = {
      directory_to_zip = "../layer-${var.name_lambda_layer}"
      output           = "${var.name_lambda_layer}.zip"
    }
  }

  triggers = {
    always_run = "${timestamp()}"
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name          = var.name_lambda_layer
  filename            = "${var.name_lambda_layer}.zip"
  compatible_runtimes = ["python3.11"]

  depends_on = [null_resource.zipfile]
}
