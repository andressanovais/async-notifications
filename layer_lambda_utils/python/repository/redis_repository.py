import redis


class RedisRepository:
    def __init__(self, host: str, port: int, password: str) -> None:
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            ssl=True,
            decode_responses=True,
        )
    
    def get_item(self, item_name: str) -> str:
        return self.redis_client.get(item_name)
    
    def set_item(self, item_name: str, value: str) -> None:
        self.redis_client.set(item_name, value)

    def delete_item(self, item_name: str) -> None:
         self.redis_client.delete(item_name)
