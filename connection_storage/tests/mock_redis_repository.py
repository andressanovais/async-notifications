class RedisRepository:
    def __init__(self, *args):
        self.fake_cache = {}

    def set_item(self, key: str, value: str) -> None:
        self.fake_cache[key] = value

    def get_item(self, key: str) -> str:
        return self.fake_cache[key]

    def delete_item(self, key: str) -> None:
        self.fake_cache.pop(key)
