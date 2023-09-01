locals {
  lambda_integrations = {
    "$disconnect" = {
      lambda_arn = module.lambda_connection_state_store.arn
    },
    "sendUserId" = {
      lambda_arn = module.lambda_connection_state_store.arn
    }
  }
}