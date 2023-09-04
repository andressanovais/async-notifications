from abc import ABC, abstractmethod

from repository.redis_repository import RedisRepository


class ConnectionSetterStrategy(ABC):
    def __init__(self, repository: RedisRepository, event: dict) -> None:
        self.repository = repository
        self.event = event

    @abstractmethod
    def set_connection_state(self, connection: dict) -> None:
        pass
