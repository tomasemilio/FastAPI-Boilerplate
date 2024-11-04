from typing import Annotated, ClassVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, model_validator

from app.database.schemas import BaseOut
from app.functions.exceptions import unprocessable_entity
from app.models.auth.role import Role


class UserIn(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "example@example.com",
            },
        }
    )
    name: str
    email: EmailStr
    password: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    verified: bool = False
    scope: list[Role] = [Role.USER]


class PasswordsIn(BaseModel):
    password: SecretStr = Field(..., examples=["123"])
    confirm_password: SecretStr = Field(..., examples=["123"])

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password.get_secret_value() != self.confirm_password.get_secret_value():
            raise unprocessable_entity("Passwords do not match")
        return self


class UserOut(BaseOut):
    name: str
    email: EmailStr
    verified: bool
    scope: list[Role]


from app.models.post.schemas import PostOut


class UserDetailOut(UserOut):
    posts: list[PostOut]
