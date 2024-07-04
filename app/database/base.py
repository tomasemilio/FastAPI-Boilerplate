from datetime import UTC, datetime
from typing import Self, Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import TIMESTAMP

from app.database.dependencies import sessDep
from app.functions.exceptions import not_found


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: uuid4().hex,
        sort_order=-3,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        nullable=False,
        sort_order=-2,
        type_=TIMESTAMP(timezone=True),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
        sort_order=-1,
        type_=TIMESTAMP(timezone=True),
    )

    async def save(self, async_session: sessDep) -> Self:
        async_session.add(self)
        await async_session.commit()
        await async_session.refresh(self)
        return self

    @classmethod
    async def get(cls, async_session: sessDep, id: str) -> Self:
        result = await async_session.get(cls, id)
        if not result:
            raise not_found(msg=f"{cls.__name__} not found")
        return result

    @classmethod
    async def all(cls, async_session: sessDep) -> Sequence[Self]:
        result = await async_session.execute(select(cls))
        return result.scalars().all()

    async def delete(self, async_session: sessDep):
        await async_session.delete(self)
        await async_session.commit()

    async def update(self, async_session: sessDep, **kwargs) -> Self:
        for key, value in kwargs.items():
            setattr(self, key, value)
        await async_session.commit()
        await async_session.refresh(self)
        return self

    @classmethod
    async def find(
        cls, async_session: sessDep, raise_: bool = False, **kwargs
    ) -> Self | None:
        result = await async_session.execute(select(cls).filter_by(**kwargs))
        result = result.scalars().first()
        if not result and raise_:
            raise not_found(msg=f"{cls.__name__} not found")
        return result
