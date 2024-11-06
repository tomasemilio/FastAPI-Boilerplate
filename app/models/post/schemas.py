from pydantic import BaseModel

from app.database.schemas import BaseOut
from app.models.user.schemas import UserOut


class PostIn(BaseModel):
    title: str
    content: str


class PostOut(PostIn, BaseOut): ...


from app.models.tag.schemas import TagOut


class PostDetailOut(PostIn, BaseOut):
    user: UserOut
    tags: list["TagOut"]
