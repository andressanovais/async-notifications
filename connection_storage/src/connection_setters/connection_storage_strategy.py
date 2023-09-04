import json

from connection_setters.connection_setter_strategy import \
    ConnectionSetterStrategy
from repository.redis_keys import get_user_key
from repository.redis_repository import RedisRepository


class ConnectionStorageStrategy(ConnectionSetterStrategy):
    def __init__(self, repository: RedisRepository, event: dict) -> None:
        super().__init__(repository, event)

    def set_connection_state(self, connection: dict) -> None:
        user_id = json.loads(self.event['body'])['user_id']
        user_key = get_user_key(user_id)

        self.repository.set_item(user_key, connection['id'])
        self.repository.set_item(connection['key'], user_id)
