from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.tag.association import Association

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.user import User


class Tag(Base):
    __tablename__ = "tag"
    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(default=None)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tags", lazy="select")
    posts: Mapped[list["Post"]] = relationship(
        secondary=Association.__tablename__, back_populates="tags", lazy="select"
    )
    __table_args__ = (UniqueConstraint("name", "user_id"),)
