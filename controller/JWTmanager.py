import jwt
from pydantic import BaseModel, Field

from models.response import AuthResp, TokenPayload


class JWTSettings(BaseModel):
    """JWT Configuration Settings"""

    secret_key: str = Field(default="SECRET_KEY")


class JWTmanager:
    """JWT MANAGEMENT"""

    def __init__(self, setting: JWTSettings) -> None:
        self.settings = setting

    def verify(self, token: str) -> AuthResp:
        try:
            jwt.decode(token, self.settings.secret_key, algorithm="HS256")
            return AuthResp(success=True)
        except jwt.ExpiredSignatureError:
            return AuthResp(success=False, error="Token Expired")
        except jwt.InvalidTokenError:
            return AuthResp(success=False, error="Invalid Token")

    def encode(self, payload: TokenPayload):
        token = jwt.encode(
            payload.__dict__, self.settings.secret_key, algorithm="HS256"
        )
        return AuthResp(success=True, token=token)
