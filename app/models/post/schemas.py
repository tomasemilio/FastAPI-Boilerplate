from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    content: str
