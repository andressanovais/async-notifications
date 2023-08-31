import logging
import os
from connection_state_store import ConnectionStateStore
from repository.redis_repository import RedisRepository
import helper

repository = None


def handler(event):
    if repository is None:
        repository = RedisRepository(
            os.getenv('db_host'),
            os.getenv('db_port'),
            password=helper.get_secret(os.getenv('db_password_secrets_name')),
        )

    ConnectionStateStore(event, repository).store_state()

    return {
        'statusCode': 200,
    }
