import os
from dotenv import dotenv_values
from core.interfaces.secret import Secret
from core.exceptions.configuration import ConfigurationException
import logging

logger = logging.getLogger(__name__)


class EnvironSecret(Secret):

    def __init__(self):
        pass

    def get(self, key):
        try:
            return os.environ[key]
        except KeyError:
            raise ConfigurationException(f'Secret {key} is missing')


class FileSecret(Secret):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._secrets = self._load_secrets(kwargs.get('env_file_path'))

    def _load_secrets(self, env_file_path):
        if env_file_path is None:
            raise ConfigurationException("env_file_path is missing")
        return dotenv_values(env_file_path)
