from notification_context import NotificationContext


def lambda_handler(event):
    NotificationContext(event).send_notification()
    
    return {
        'statusCode': 200,
    }
