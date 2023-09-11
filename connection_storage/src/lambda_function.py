import os

from connection_state_context import ConnectionStateContext
from repository.redis_repository import RedisRepository
from secrets_manager import get_secret

password = get_secret(os.getenv('elasticache_secret_name'))
repository = RedisRepository(
    os.getenv('elasticache_host'),
    os.getenv('elasticache_port'),
    password,
)


def handler(event):
    connection_context = ConnectionStateContext(repository)
    connection_context.set_connection_state(event)

    return {
        'statusCode': 200,
    }
