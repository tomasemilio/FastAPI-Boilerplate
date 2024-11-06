from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Association(Base):
    __tablename__ = "association"
    post_id: Mapped[UUID] = mapped_column(ForeignKey("post.id"))
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("tag.id"))
    __table_args__ = (UniqueConstraint("post_id", "tag_id"),)
