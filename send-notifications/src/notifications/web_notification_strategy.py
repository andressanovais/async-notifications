import json
import os
import boto3
from secrets_manager import get_secret
from repository.redis_repository import RedisRepository
from repository.redis_keys import get_user_key


class WebNotificationStrategy:
    def __init__(self, event: dict) -> None:
        self.event = event
        self.repository = RedisRepository(
            os.getenv('elasticache_host'),
            os.getenv('elasticache_port'),
            password=get_secret(os.getenv('elasticache_secret_name')),
        )
    
    def send_notification(self):
        key = get_user_key(self.event['user_id'])
        connection_id = self.repository.get(key)

        client = boto3.client(
            'apigatewaymanagementapi',
            endpoint_url=os.getenv('websocket_url'),
        )

        client.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(self.event),
        )
