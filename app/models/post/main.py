from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field, Relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class PostIn(BaseModel):
    title: str
    content: str


class Post(PostIn, Base, table=True):
    user_id: UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="posts")
