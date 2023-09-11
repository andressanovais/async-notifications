import json
from unittest.mock import patch

from connection_storage.src.connection_setters import \
    connection_storage_strategy
from connection_storage.tests.mock_redis_repository import RedisRepository

user_id = 'userabc'
user_key = f'user:{user_id}:connection'
connection = {
    'id': '123',
    'key': 'connection:123:user',
}


@patch.object(connection_storage_strategy, 'get_user_key', return_value=user_key)
def test_connection_being_stored(get_user_key_mock):
    fake_repository = RedisRepository()
    event = {'body': json.dumps({'user_id': user_id})}

    storage_strategy = connection_storage_strategy.ConnectionStorageStrategy(fake_repository, event)
    storage_strategy.set_connection_state(connection)

    assert len(fake_repository.fake_cache) == 2
    assert fake_repository.fake_cache[user_key] == connection['id']
    assert fake_repository.fake_cache[connection['key']] == user_id
