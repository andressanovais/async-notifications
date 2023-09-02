def get_user_key(user_id: str) -> str:
    return f'user:{user_id}:connection'


def get_connection_key(connection_id: str) -> str:
    return f'connection:{connection_id}:user'
