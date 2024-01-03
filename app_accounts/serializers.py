from pydantic import BaseModel
from typing import Optional, List


class UserAuthToken(BaseModel):
    user_id: str
    auth_time: float
    exp: Optional[int]


class AccountSerializer(BaseModel):
    id: str
    order: int
    meta: dict
