import json

from connection_storage.src.connection_setters.connection_storage_strategy import ConnectionStorageStrategy
from connection_storage.tests.mock_redis_repository import RedisRepository


def test_connection_being_stored(mocker):
    user_id = 'userabc'
    user_key = f'user:{user_id}:connection'
    mocker.patch(
        'connection_storage.src.connection_setters.connection_storage_strategy.get_user_key',
        return_value=user_key,
    )

    fake_repository = RedisRepository()
    event = {'body': json.dumps({'user_id': user_id})}
    connection = {
        'id': '123',
        'key': 'connection:123:user',
    }

    storage_strategy = ConnectionStorageStrategy(fake_repository, event)
    storage_strategy.set_connection_state(connection)

    assert len(fake_repository.fake_cache) == 2
    assert fake_repository.fake_cache[user_key] == connection['id']
    assert fake_repository.fake_cache[connection['key']] == user_id
