from abc import ABC, abstractmethod
from typing import Iterable, List
from uuid import UUID


class AuditRepositoryInterface(ABC):
    """Abstract interface for storing user actions logs"""

    @abstractmethod
    def log(self, actor: UUID, message: str):
        """add log entry"""


class Repository(ABC):
    """Abstract interface for interacting with the datalayer"""

    @abstractmethod
    def add(self, *args, **kwargs):
        """save object"""

    @abstractmethod
    def add_bulk(self, *args, **kwargs):
        """save a list of objects"""

    @abstractmethod
    def get(self, *args, **kwargs):
        """get object"""

    @abstractmethod
    def delete(self, *args, **kwargs):
        """delete object"""

    @abstractmethod
    def filter(self, *args, **kwargs) -> Iterable:
        """get a list of iterable objects after applying some filtering"""
