from abc import ABC, abstractmethod


class Storage(ABC):
    def __call__(self):
        return self

    @abstractmethod
    async def insert(self, item: dict):
        pass

    @abstractmethod
    async def select(self, item: dict):
        pass

    @abstractmethod
    async def delete(self, item: dict):
        pass

    @abstractmethod
    async def update(self, item: dict, prop: dict):
        pass

    @abstractmethod
    async def select_items(self, fltr: dict, **kwargs):
        pass
