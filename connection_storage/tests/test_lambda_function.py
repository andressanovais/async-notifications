from connection_storage.src import lambda_function
import pytest

path = 'connection_storage.src.lambda_function'


def test_success(mocker):
    mocker.patch(f'{path}.ConnectionStateContext')
    response = lambda_function.handler({})
    assert response['statusCode'] == 200


def test_failure(mocker):
    mocker.patch(
        f'{path}.ConnectionStateContext',
        side_effect=Exception('boom'),
    )

    with pytest.raises(Exception):
        lambda_function.handler({})
