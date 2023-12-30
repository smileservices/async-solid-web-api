from abc import ABC, abstractmethod


class CacheInterface(ABC):

    @abstractmethod
    def set(self, key: str, value: str, expire=None):
        raise NotImplemented()

    @abstractmethod
    def get(self, key: str):
        raise NotImplemented()

    @abstractmethod
    def delete(self, key: str):
        raise NotImplemented()

    @abstractmethod
    def exists(self, key: str):
        raise NotImplemented()
