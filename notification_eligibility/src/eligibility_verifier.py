import base64
import json

from repository.abstract_repository import AbstractRepository
from scheduler import Scheduler


class EligibilityVerifier:
    def __init__(self, repository: AbstractRepository, scheduler_client) -> None:
        self.repository = repository
        self.scheduler_client = scheduler_client
    
    def check_eligibility_and_schedule_notifications(self, event: dict) -> None:
        for partition in event['records']:
            for record in event['records'][partition]:
                message = json.loads(base64.b64decode(record['value']))

                if self.__user_is_eligible(message['user_id']):
                    scheduler = Scheduler(self.scheduler_client)
                    scheduler.schedule_send_notifications(message)

    def __user_is_eligible(self, user_id: str) -> bool:
        item = self.repository.get_user_item(user_id)
        return not item['opt_out']
