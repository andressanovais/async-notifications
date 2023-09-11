from unittest.mock import patch

from connection_storage.src import lambda_function
import pytest

path = 'connection_storage.src.lambda_function'


@patch(f'{path}.ConnectionStateContext')
def test_success(connection_context_mock):
    response = lambda_function.handler({})
    assert response['statusCode'] == 200
    connection_context_mock.return_value.set_connection_state.assert_called_once()


@patch(f'{path}.ConnectionStateContext', side_effect=Exception('boom'))
def test_failure(connection_context_mock):
    with pytest.raises(Exception):
        lambda_function.handler({})
