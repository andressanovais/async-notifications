import redis


class RedisRepository:
    def __init__(self, host: str, port: int, password: str):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            ssl=True,
            decode_responses=True,
        )
    
    def get_item(self, item_name: str):
        self.redis_client.get(item_name)
