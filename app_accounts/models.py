from dataclasses import dataclass


@dataclass
class Account:
    """ primary account unit on this platform; permissions is a bitmap """
    id: str
    order: int
    meta: dict
