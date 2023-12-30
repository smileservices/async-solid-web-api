from pydantic import BaseModel


class AccountSerializer(BaseModel):
    id: str
    meta: dict
