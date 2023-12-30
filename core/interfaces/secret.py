from abc import ABC, abstractmethod
from core.exceptions.configuration import ConfigurationException


class Secret(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """should populate the _secrets instance attribute"""

    def get(self, key):
        try:
            return self._secrets[key]
        except KeyError:
            raise ConfigurationException(f'Secret {key} is missing')
