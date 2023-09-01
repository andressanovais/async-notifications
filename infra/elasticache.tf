/* So possui implementacao local no LocalStack Pro, por isso estou comentando
resource "aws_elasticache_replication_group" "web-notifications-cache" {
  replication_group_id = "connections-web-notification"

  node_type = "cache.t3.micro"
  port      = 7236

  subnet_group_name          = aws_elasticache_subnet_group.default.name
  num_cache_clusters         = 2
  automatic_failover_enabled = true

}

resource "aws_elasticache_subnet_group" "cache-subnets" {
  name       = "web-notifications-subnets"
  subnet_ids = var.subnet_ids
}
 */