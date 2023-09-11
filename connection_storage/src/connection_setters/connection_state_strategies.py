from connection_setters.connection_removal_strategy import \
    ConnectionRemovalStrategy
from connection_setters.connection_storage_strategy import \
    ConnectionStorageStrategy


def get_connection_state_strategies() -> dict:
    return {
        'sendUserId': ConnectionStorageStrategy,
        '$disconnect':  ConnectionRemovalStrategy
    }
