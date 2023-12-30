from abc import ABC, abstractmethod
from typing import Callable


class MessageQueue(ABC):

    @abstractmethod
    def publish(self, message: str, topic: str):
        """send the message to the corresponding topic"""

    @abstractmethod
    def subscribe(self, topic: str, consume_callback: Callable):
        """consume the messages of a certain topic"""

    @abstractmethod
    def consume_all(self):
        """trigger consuming all messages"""
