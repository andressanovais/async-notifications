data "archive_file" "lambda_zip_file" {
  output_path = "${path.module}/lambda_zip/lambda-${var.lambda_name}.zip"
  source_dir  = "../${var.lambda_name}/src"
  excludes    = ["__pycache__"]
  type        = "zip"
}

resource "aws_lambda_function" "function" {
  function_name    = var.lambda_name
  handler          = "lambda_function.handler"
  filename         = data.archive_file.lambda_zip_file.output_path
  source_code_hash = data.archive_file.lambda_zip_file.output_base64sha256
  role             = aws_iam_role.lambda_role.arn
  runtime          = var.lambda_runtime
  layers           = [var.lambda_layer_arn]

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [var.vpc_security_group_id]
  }

  environment {
    variables = var.environment_variables
  }

  depends_on = [
    aws_cloudwatch_log_group.log_group
  ]
}

resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/aws/lambda/${var.lambda_name}"
  retention_in_days = 7
}

resource "aws_iam_role" "lambda_role" {
  name               = "${var.lambda_name}-role"
  assume_role_policy = file("./iam_policies/lambda_assume_role.json")
}

resource "aws_iam_policy" "lambda_policy" {
  name   = "${var.lambda_name}-policy"
  policy = file(var.policy_path)
}

resource "aws_iam_role_policy_attachment" "lambda_role_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_base_role_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = var.lambda_base_policy_arn
}

output "arn" {
  value = aws_lambda_function.function.arn
}
