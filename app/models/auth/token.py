from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import BaseModel, computed_field

from app.config import config
from app.functions.exceptions import forbidden
from app.functions.jwt import decode, encode
from app.models.auth.role import Role


class TokenEncode(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    scope: list[Role] = [Role.USER]


class TokenDecode(BaseModel):
    id: str
    iat: datetime
    exp: datetime
    scope: list[Role]

    @computed_field
    def expires_in(self) -> int:
        return int((self.exp - datetime.now(UTC)).total_seconds())


class Token:
    def __init__(
        self,
        id: Any,
        scope: Role | list[Role],
        expires_in: int = config.TOKEN_EXPIRE_SECONDS,
    ):
        self.id = id
        self.expires_in = expires_in
        self.scope = scope if isinstance(scope, list) else [scope]
        self.iat: datetime = datetime.now(UTC)
        self.exp: datetime = self.iat + timedelta(seconds=expires_in)

    def encode(self) -> TokenEncode:
        token = encode(**self.__dict__)
        return TokenEncode(
            access_token=token, expires_in=self.expires_in, scope=self.scope
        )

    @classmethod
    def decode(cls, token: str, scope: list[Role] | None = None) -> TokenDecode:
        decoded = decode(token)
        if scope:
            if "admin" in decoded["scope"]:
                ...
            elif not all(i in decoded["scope"] for i in scope):
                raise forbidden(msg="Insufficient scope.")
        return TokenDecode.model_validate(decoded)
