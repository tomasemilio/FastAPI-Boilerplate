from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, Field, computed_field

from app.config import config
from app.functions.exceptions import forbidden
from app.functions.jwt import decode, encode
from app.models.auth.role import Role
from app.models.auth.schemas import TokenDecode, TokenEncode


class Token(BaseModel):
    id: str
    scope: list[Role] = [Role.USER]
    expires_in: int = config.TOKEN_EXPIRE_SECONDS
    iat: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @computed_field
    def exp(self) -> datetime:
        return self.iat + timedelta(seconds=self.expires_in)

    def encode(self) -> TokenEncode:
        token = encode(**self.model_dump())
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
