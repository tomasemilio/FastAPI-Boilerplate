from typing import Annotated, override
from uuid import UUID

from pydantic import (AfterValidator, BaseModel, EmailStr, ValidationInfo,
                      field_validator)
from sqlalchemy import JSON, Column
from sqlmodel import AutoString, Field, Relationship

from app.database.base import Base
from app.functions.exceptions import conflict
from app.functions.hash import check_hash, get_hash
from app.models.auth.role import Role
from app.models.post import Post


class User(Base, table=True):
    name: str
    password: Annotated[str, AfterValidator(get_hash)]
    email: Annotated[EmailStr, Field(index=True, sa_type=AutoString, unique=True)]
    scope: Annotated[list[Role], Field(default=[Role.USER], sa_column=Column(JSON))]
    posts: list[Post] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )

    def verify_password(self, password: str) -> bool:
        return check_hash(password, self.password)

    @field_validator("email")
    @classmethod
    def check_email(cls, email: EmailStr) -> EmailStr:
        if cls.find(email=email):
            conflict("Email already exists.")
        return email

    @override
    def update(self, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = get_hash(kwargs["password"])
        return super().update(**kwargs)

class UserIn(BaseModel):
    name: str
    password: str
    confirm_password: str
    email: EmailStr
    scope: list[Role] = [Role.USER]

    @field_validator("confirm_password")
    @classmethod
    def password_match(cls, v: str, info: ValidationInfo) -> str:
        if v != info.data["password"]:
            raise ValueError("password and confirm_password do not match")
        return v


class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    scope: list[Role]
