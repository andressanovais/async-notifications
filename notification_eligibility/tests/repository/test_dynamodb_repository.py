import os

import boto3
from moto import mock_dynamodb

from notification_eligibility.src.repository.dynamodb_repository import DynamodbRepository


@mock_dynamodb
def test_get_user_item():
    table_name = 'my_table'
    os.environ['eligibility_table_name'] = table_name

    dynamodb = boto3.resource('dynamodb')
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'user_id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
    )

    user_id = 'abcd'
    expected_item = {'user_id': user_id, 'opt_out': False}
    table = dynamodb.Table(table_name)
    table.put_item(Item=expected_item)

    received_item = DynamodbRepository().get_user_item(user_id)
    assert received_item == expected_item
