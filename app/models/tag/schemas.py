from pydantic import BaseModel

from app.database.schemas import BaseOut
from app.models.post.schemas import PostOut
from app.models.user.schemas import UserOut


class TagIn(BaseModel):
    name: str
    description: str | None = None


class TagOut(TagIn, BaseOut): ...


class TagDetailOut(TagOut):
    posts: list[PostOut]
    user: UserOut
