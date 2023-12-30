from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union
from tempfile import SpooledTemporaryFile


class StorageException(Exception):
    pass


@dataclass
class StorageFileShare:
    id: str
    path: str
    url: str


@dataclass
class UploadFile:
    source: Union[str, bytes, SpooledTemporaryFile]
    content_type: str
    name: str


class StorageInterface(ABC):

    @abstractmethod
    def save(self, source, path: str):
        "save a file"

    def get_path(self, path: str) -> str:
        """Retrieve the path of the file, relative to the storage"""

    @abstractmethod
    def get_url(self, path: str):
        """Retrieve the url of the file"""

    @abstractmethod
    def list(self, path: str):
        "list a directory"

    @abstractmethod
    def delete(self, path: str):
        "delete a file"

    @abstractmethod
    def copy(self, source_path: str, dest_path: str):
        "copy an existing file"
