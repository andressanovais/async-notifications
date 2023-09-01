resource "aws_cloudwatch_log_group" "api_logs" {
  name = "api-web-notifications"
}

resource "aws_apigatewayv2_api" "api" {
  name                       = "web-notifications"
  protocol_type              = "WEBSOCKET"
  route_selection_expression = "$request.body.action"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_logs.arn
    format          = "$context.identity.sourceIp - - [$context.requestTime] \"$context.httpMethod $context.routeKey $context.protocol\" $context.status $context.responseLength $context.requestId $context.integrationErrorMessage"
  }
}

resource "aws_apigatewayv2_route" "lambda_integration_routes" {
  for_each = local.lambda_integrations

  api_id    = aws_apigatewayv2_api.api.id
  route_key = each.key
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integrations[each.key].id}"
}

resource "aws_apigatewayv2_integration" "lambda_integrations" {
  for_each = local.lambda_integrations

  api_id           = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"
  integration_uri  = each.value.lambda_arn
}

resource "aws_apigatewayv2_route" "connect_route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "$connect"
  target    = "integrations/${aws_apigatewayv2_integration.connect_integration.id}}"
}

resource "aws_apigatewayv2_integration" "connect_integration" {
  api_id           = aws_apigatewayv2_api.api.id
  integration_type = "MOCK"

  request_templates = {
    "200" : "{ \"statusCode\" : \"200\" }"
  }
  template_selection_expression = "200"
}

resource "aws_apigatewayv2_integration_response" "mock_integration_response" {
  api_id                   = aws_apigatewayv2_api.api.id
  integration_id           = aws_apigatewayv2_integration.connect_integration.id
  integration_response_key = "/200/"
  response_templates = {
    "200" : "{ \"statusCode\" : \"200\" }"
  }
}
