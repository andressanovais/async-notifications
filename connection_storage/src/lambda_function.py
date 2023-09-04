import os

from connection_state_context import ConnectionStateContext
from repository.redis_repository import RedisRepository
from secrets_manager import get_secret

repository = RedisRepository(
    os.getenv('elasticache_host'),
    os.getenv('elasticache_port'),
    password=get_secret(os.getenv('elasticache_secret_name')),
)


def handler(event):
    ConnectionStateContext(event, repository).set_connection_state()

    return {
        'statusCode': 200,
    }
