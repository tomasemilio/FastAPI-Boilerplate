from pydantic import BaseModel

from app.database.schemas import BaseOut
from app.models.user.schemas import UserOut


class PostIn(BaseModel):
    title: str
    content: str


class PostOut(PostIn, BaseOut): ...


class PostDetailOut(PostIn, BaseOut):
    user: UserOut
