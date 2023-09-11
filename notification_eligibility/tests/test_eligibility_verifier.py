from unittest.mock import patch, MagicMock

from notification_eligibility.src import eligibility_verifier


event = {
       'records': {
          'mytopic-0': [
             {
                'key': 'abcDEFghiJKLmnoPQRstuVWXyz1234==',
                'value': 'ew0KICAgICAgICAidXNlcl9pZCI6ICJhYmMiDQp9',
             }
          ]
       }
}


@patch.object(eligibility_verifier, 'Scheduler')
def test_eligible_user(scheduler_mock):
    check_eligibility_when_opt_out_equals(False)
    scheduler_mock.return_value.schedule_send_notifications.assert_called_once()


@patch.object(eligibility_verifier, 'Scheduler')
def test_ineligible_user(scheduler_mock):
    check_eligibility_when_opt_out_equals(True)
    scheduler_mock.return_value.schedule_send_notifications.assert_not_called()


def check_eligibility_when_opt_out_equals(opt_out: bool) -> None:
    repository_mock = MagicMock()
    repository_mock.get_user_item = MagicMock(return_value={
        'opt_out': opt_out,
    })

    verifier = eligibility_verifier.EligibilityVerifier(repository_mock, None)
    verifier.check_eligibility_and_schedule_notifications(event)
