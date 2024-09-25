from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, computed_field

from app.models.auth.role import Role


class TokenEncode(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    scope: list[Role] = [Role.USER]


class TokenDecode(BaseModel):
    id: UUID
    iat: datetime
    exp: datetime
    scope: list[Role]

    @computed_field()
    def expires_in(self) -> float:
        return (self.exp - datetime.now(UTC)).total_seconds()
