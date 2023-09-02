from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def get_user_item(self, user_id: str) -> dict:
        pass
