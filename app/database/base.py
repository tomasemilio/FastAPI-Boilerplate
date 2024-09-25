from datetime import UTC, datetime
from typing import Literal, Self, Sequence, overload
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import TIMESTAMP

from app.database.dependencies import sessDep
from app.functions.exceptions import not_found


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=lambda: uuid4(), sort_order=-3
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
    async def get(cls, async_session: sessDep, id: UUID) -> Self:
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
        return self

    @overload
    @classmethod
    async def find(
        cls, async_session: sessDep, raise_: Literal[True], **kwargs
    ) -> Self: ...

    @overload
    @classmethod
    async def find(
        cls, async_session: sessDep, raise_: Literal[False], **kwargs
    ) -> Self | None: ...

    @classmethod
    async def find(
        cls, async_session: sessDep, raise_: bool = True, **kwargs
    ) -> Self | None:
        stmt = select(cls).filter_by(**kwargs)
        resp = await async_session.scalar(stmt)
        if not resp and raise_:
            raise not_found(msg=f"{cls.__name__} not found")
        return resp
