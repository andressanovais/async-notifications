import pytest

from unittest.mock import patch, MagicMock
from connection_storage.src import connection_state_context as context

path = 'connection_storage.src.connection_state_context'
connection_key = 'connection:123:user'
connection = {
    'id': '123',
    'key': connection_key,
}


@patch(f'{path}.connection_state_strategies.ConnectionStorageStrategy')
@patch(f'{path}.get_connection_key', MagicMock(return_value=connection_key))
def test_send_user_strategy(connection_storage_mock):
    event = create_fake_event('sendUserId')

    context.ConnectionStateContext(None).set_connection_state(event)

    set_connection_state_mock = connection_storage_mock.return_value.set_connection_state
    set_connection_state_mock.assert_called_once_with(connection)


@patch(f'{path}.connection_state_strategies.ConnectionRemovalStrategy')
@patch(f'{path}.get_connection_key', MagicMock(return_value=connection_key))
def test_disconnect_strategy(connection_removal_mock):
    event = create_fake_event('$disconnect')

    context.ConnectionStateContext(None).set_connection_state(event)

    set_connection_state_mock = connection_removal_mock.return_value.set_connection_state
    set_connection_state_mock.assert_called_once_with(connection)


def test_nonexistent_strategy():
    event = create_fake_event('routeNonexistent')

    with pytest.raises(KeyError):
        context.ConnectionStateContext(None).set_connection_state(event)


def create_fake_event(route_key: str) -> dict:
    return {
        'requestContext': {
            'routeKey': route_key,
            'connectionId': connection['id']
        }
    }
