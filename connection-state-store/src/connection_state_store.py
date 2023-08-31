import json


class ConnectionStateStore:
    def __init__(self, event, repository):
        self.event = event
        self.repository = repository
        self.connection_id = event['requestContext']['connectionId']
        self.connection_key = f'connection:{self.connection_id}:user'

    def store_state(self):
        route = self.event['requestContext']['routeKey']

        possible_routes_that_change_connection_state = {
            'sendUserId': self.__store_connection_user_id,
            '$disconnect': self.__close_connection,
        }
        
        possible_routes_that_change_connection_state[route]()


    def __store_connection_user_id(self):
        user_id = json.loads(self.event['body'])['user_id']

        user_key = f'user:{user_id}:connection'
        
        self.repository.set_item(user_key, self.connection_id)
        self.repository.set_item(self.connection_key, user_id)


    def __close_connection(self):
        user_id = self.repository.get_item(self.connection_key)

        self.repository.delete_item(self.connection_key)
        self.repository.delete_item(f'user:{user_id}:connection')
