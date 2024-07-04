from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    content: str


class PostOut(PostIn):
    id: str
    user_id: str
