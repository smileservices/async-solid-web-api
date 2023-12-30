from __future__ import annotations
from os import environ
from typing import Optional
from dataclasses import dataclass
from core.interfaces import repository, secret, message_queue, config
from core.exceptions.configuration import ConfigurationException
import logging

logger = logging.getLogger(__file__)


class PydanticConfig:
    arbitrary_types_allowed = True


@dataclass
class ConfigService(config.ConfigInterface):
    _secret_manager: secret.Secret
    _secure_manager: Optional[secret.Secret] = None

    def get(self, key):
        return self._secret_manager.get(key)

    def get_secure(self, key):
        # get highly secure secrets (private keys, passwords, etc)
        if not self._secure_manager:
            raise NotImplementedError("No secure manager declared")
        return self._secure_manager.get(key)
