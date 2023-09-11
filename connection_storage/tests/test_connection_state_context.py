import pytest

from connection_storage.src.connection_state_context import ConnectionStateContext

path = 'connection_storage.src.connection_state_context'


def test_send_user_strategy(mocker):
    connection = get_mocked_connection(mocker)
    event = create_mock_event('sendUserId', connection)

    connection_storage_mock = mocker.patch(f'{path}.connection_state_strategies.ConnectionStorageStrategy')
    ConnectionStateContext(None).set_connection_state(event)

    set_connection_state_mock = connection_storage_mock.return_value.set_connection_state
    set_connection_state_mock.assert_called_once_with(connection)


def test_disconnect_strategy(mocker):
    connection = get_mocked_connection(mocker)
    event = create_mock_event('$disconnect', connection)

    connection_storage_mock = mocker.patch(f'{path}.connection_state_strategies.ConnectionRemovalStrategy')
    ConnectionStateContext(None).set_connection_state(event)

    set_connection_state_mock = connection_storage_mock.return_value.set_connection_state
    set_connection_state_mock.assert_called_once_with(connection)


def test_nonexistent_strategy(mocker):
    connection = get_mocked_connection(mocker)
    event = create_mock_event('routeNonexistent', connection)

    with pytest.raises(KeyError):
        ConnectionStateContext(None).set_connection_state(event)


def get_mocked_connection(mocker) -> dict:
    connection_key = 'connection:123:user'
    mocker.patch(f'{path}.get_connection_key', return_value=connection_key)

    return {
        'id': '123',
        'key': connection_key,
    }


def create_mock_event(route_key: str, connection: dict) -> dict:
    return {
        'requestContext': {
            'routeKey': route_key,
            'connectionId': connection['id']
        }
    }
