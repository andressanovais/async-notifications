from connection_setters.connection_state_strategies import get_connection_storage_strategies
from repository.redis_keys import get_connection_key


class ConnectionStateContext:
    def __init__(self) -> None:
        self.strategies = get_connection_storage_strategies()

    def set_connection_state(self, event):
        route = event['requestContext']['routeKey']

        connection_id = event['requestContext']['connectionId']
        connection = {
            'connection_id': connection_id,
            'connection_key': get_connection_key(connection_id),
        }

        connection_state = self.strategies[route](event, connection)
        connection_state.set_connection_state()
