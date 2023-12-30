from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Dependencies(ABC):
    pass


@dataclass
class ConfigInterface(ABC):

    @abstractmethod
    def get(self, key: str):
        raise NotImplementedError()

    @abstractmethod
    def get_secure(self, key: str):
        raise NotImplementedError()
