from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def get_item(self, item_name: str) -> str:
        pass
    
    @abstractmethod
    def set_item(self, item_name: str, value: str) -> None:
        pass

    @abstractmethod
    def delete_item(self, item_name: str) -> None:
        pass
