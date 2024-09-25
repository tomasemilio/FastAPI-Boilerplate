from uuid import UUID

from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    content: str


class PostOut(PostIn):
    id: UUID
    user_id: UUID
