import base64
import json
import boto3
from datetime import datetime, timedelta


def handler(event):
    for partition in event['records']:
        for record in event['records'][partition]:
            message_as_str = base64.b64decode(record['value']).decode("utf-8")
            message = json.loads(message_as_str)
            print(message)

            dynamodb_resource = boto3.resource('dynamodb')
            table = dynamodb_resource.Table('user_terms')
            
            response = table.get_item(
                Key={
                    'user_id': message['user_id'],
                },
            )
            
            if not response['Item']['optout']:
                scheduler = boto3.client('scheduler')
                
                now_with_more_one_min = datetime.now() + timedelta(minutes=1)
                schedule_time = now_with_more_one_min.strftime('%Y-%m-%dT%H:%M:%S')
            
                response_scheduler = scheduler.create_schedule(
                    ActionAfterCompletion='NONE',
                    Name=f"InvocarEnvioNotificacoes-{message['user_id']}-{message['notification_type']}",
                    ScheduleExpression=f'at({schedule_time})',
                    Target={
                        'RoleArn':'arn:aws:iam::172486191248:role/scheduler-notifications',
                        'Arn': 'arn:aws:lambda:sa-east-1:172486191248:function:send-notifications',
                        'Input': message_as_str,
                    },
                    FlexibleTimeWindow={
                        'Mode':'OFF'
                    },
                    ScheduleExpressionTimezone='Etc/UTC',
                    State='ENABLED',
                ),
                
                print(response_scheduler)
