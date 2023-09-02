/* So possui implementacao local no LocalStack Pro
resource "aws_elasticache_replication_group" "web-notifications-cache" {
  replication_group_id = "connections-web-notification"

  node_type = "cache.t3.micro"
  port      = 7236

  subnet_group_name          = aws_elasticache_subnet_group.default.name
  num_cache_clusters         = 2
  automatic_failover_enabled = true

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token = random_password.password.result
}

resource "aws_elasticache_subnet_group" "cache-subnets" {
  name       = "web-notifications-subnets"
  subnet_ids = var.subnet_ids
}
*/

 resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "_%@"
}
  
resource "aws_secretsmanager_secret" "redis_secret" {
   name = var.elasticache_secret_name
}

resource "aws_secretsmanager_secret_version" "sversion" {
  secret_id = aws_secretsmanager_secret.redis_password.id
  secret_string = random_password.password.result
}
