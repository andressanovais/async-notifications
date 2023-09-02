locals {
  lambda_integrations = {
    "$disconnect" = {
      lambda_arn = module.lambda_connection_storage.arn
    },
    "sendUserId" = {
      lambda_arn = module.lambda_connection_storage.arn
    }
  }
}

