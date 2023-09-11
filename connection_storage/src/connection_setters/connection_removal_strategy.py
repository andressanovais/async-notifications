from connection_setters.connection_setter_strategy import \
    ConnectionSetterStrategy
from repository.redis_keys import get_user_key
from repository.redis_repository import RedisRepository


class ConnectionRemovalStrategy(ConnectionSetterStrategy):
    def __init__(self, repository: RedisRepository, event: dict) -> None:
        super().__init__(repository, event)
    
    def set_connection_state(self, connection: dict) -> None:
        user_id = self.repository.get_item(connection['key'])

        self.repository.delete_item(connection['key'])
        self.repository.delete_item(get_user_key(user_id))
