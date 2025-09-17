from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


class AuthResp(BaseModel):
    success: bool = Field(default=False)
    token: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)


class TokenPayload(BaseModel):
    name: str
    role: str
    email: str
    exp: datetime = Field(default=datetime.utcnow() + timedelta(minutes=120))
