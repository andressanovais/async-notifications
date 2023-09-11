from connection_storage.src.connection_setters.connection_removal_strategy import ConnectionRemovalStrategy
from connection_storage.tests.mock_redis_repository import RedisRepository


def test_connection_being_removed(mocker):
    fake_repository = RedisRepository()
    connection = {
        'id': '123',
        'key': 'connection:123:user'
    }
    user_key = 'user:userabc:connection'

    mocker.patch(
        'connection_storage.src.connection_setters.connection_removal_strategy.get_user_key',
        return_value=user_key,
    )

    fake_repository.set_item(connection['key'], 'userabc')
    fake_repository.set_item(user_key, connection['id'])

    removal_strategy = ConnectionRemovalStrategy(fake_repository, {})
    removal_strategy.set_connection_state(connection)

    assert len(fake_repository.fake_cache) == 0
