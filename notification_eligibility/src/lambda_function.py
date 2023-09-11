import boto3
from eligibility_verifier import EligibilityVerifier
from repository.dynamodb_repository import DynamodbRepository

repository = DynamodbRepository()
scheduler_client = boto3.client('scheduler')


def handler(event):
    verifier = EligibilityVerifier(
        repository,
        scheduler_client,
    )

    verifier.check_eligibility_and_schedule_notifications(event)
