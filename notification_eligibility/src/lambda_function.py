import boto3
from elegibility_verifier import ElegibilityVerifier
from repository.dynamodb_repository import DynamodbRepository

repository = DynamodbRepository()
scheduler_client = boto3.client('scheduler')


def handler(event):
    verifier = ElegibilityVerifier(
        repository,
        scheduler_client,
    )

    verifier.check_eligibility_and_schedule_notifications(event)
