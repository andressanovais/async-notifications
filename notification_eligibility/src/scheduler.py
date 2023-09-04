import json
import os


class Scheduler:
    def __init__(self, scheduler_client) -> None:
        self.client = scheduler_client
    
    def schedule_send_notifications(self, message: dict) -> None:
        schedule_expression = f"at({message['delivery_timestamp']})"
        schedule_name = f"InvocarEnvioNotificacoes-{message['user_id']}-{message['notification_type']}"
        target = {
            'RoleArn': os.getenv('scheduler_role_arn'),
            'Arn': os.getenv('lambda_to_schedule_arn'),
            'Input': json.dumps(message),
        }

        self.client.create_schedule(
            ActionAfterCompletion='DELETE',
            Name=schedule_name,
            ScheduleExpression=schedule_expression,
            Target=target,
            FlexibleTimeWindow={ 'Mode':'OFF' },
            ScheduleExpressionTimezone='America/Sao_Paulo',
            State='ENABLED',
        )
