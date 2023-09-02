from notifications.notification_strategies import get_strategies


class NotificationContext():
    def __init__(self):
        self.notification_strategies = get_strategies()
 
    def send_notification(self, event: dict):
        notification_type = event['notification_type']
    
        strategy = self.notification_strategies[notification_type](event)
        strategy.send_notification()
