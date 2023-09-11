from connection_setters import connection_state_strategies
from repository.redis_keys import get_connection_key
from repository.redis_repository import RedisRepository


class ConnectionStateContext:
    def __init__(self, repository: RedisRepository) -> None:
        self.repository = repository
        self.connection_state_strategies = connection_state_strategies.get_connection_state_strategies()

    def set_connection_state(self, event):
        route = event['requestContext']['routeKey']
        strategy = self.connection_state_strategies[route]
        connection_state = strategy(self.repository, event)

        connection_id = event['requestContext']['connectionId']
        connection_state.set_connection_state({
            'id': connection_id,
            'key': get_connection_key(connection_id),
        })
