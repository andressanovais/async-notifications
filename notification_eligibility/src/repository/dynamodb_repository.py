import os

import boto3


class DynamodbRepository:
    def __init__(self) -> None:
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(os.getenv('eligibility_table_name'))
    
    def get_user_item(self, user_id: str) -> dict:
        return self.table.get_item(
            Key={
                'user_id': user_id,
            },
        )['Item']
