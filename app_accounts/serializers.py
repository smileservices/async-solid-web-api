from pydantic import BaseModel


class AccountSerializer(BaseModel):
    id: str
    order: int
    meta: dict
