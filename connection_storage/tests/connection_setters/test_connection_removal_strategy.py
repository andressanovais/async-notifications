from unittest.mock import patch

from connection_storage.src.connection_setters import \
    connection_removal_strategy
from connection_storage.tests.mock_redis_repository import RedisRepository

user_key = 'user:userabc:connection'
connection = {
    'id': '123',
    'key': f'connection:123:user'
}


@patch.object(connection_removal_strategy, 'get_user_key', return_value=user_key)
def test_connection_being_removed(get_user_key_mock):
    fake_repository = RedisRepository()

    fake_repository.set_item(connection['key'], 'userabc')
    fake_repository.set_item(user_key, connection['id'])

    removal_strategy = connection_removal_strategy.ConnectionRemovalStrategy(fake_repository, {})
    removal_strategy.set_connection_state(connection)

    assert len(fake_repository.fake_cache) == 0
