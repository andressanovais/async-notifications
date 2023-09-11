from unittest.mock import MagicMock, patch

with patch.dict('sys.modules', {
    'boto3': MagicMock(),
    'repository.dynamodb_repository': MagicMock(),
}):
    from notification_eligibility.src import lambda_function

import pytest


@patch.object(lambda_function, 'EligibilityVerifier')
def test_success(eligibility_mock):
    lambda_function.handler({})

    eligibility_mock.return_value.check_eligibility_and_schedule_notifications.assert_called_once()


@patch.object(lambda_function, 'EligibilityVerifier', side_effect=Exception('boom'))
def test_failure(eligibility_mock):
    with pytest.raises(Exception):
        lambda_function.handler({})
