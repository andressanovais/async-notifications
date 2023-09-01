resource "aws_dynamodb_table" "user_terms_table" {
  name           = "user-terms"
  billing_mode   = "PROVISIONED"
  read_capacity  = var.dynamo_rcu
  write_capacity = var.dynamo_wcu
  hash_key       = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  server_side_encryption {
    enabled = true
  }
}
