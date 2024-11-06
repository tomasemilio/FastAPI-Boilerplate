from datetime import UTC, datetime
from typing import Literal, Self, Sequence, overload
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, joinedload, mapped_column
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.types import TIMESTAMP

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

    async def save(
        self,
        async_session: AsyncSession,
        relationships: list[QueryableAttribute] | None = None,
    ) -> Self:
        async_session.add(self)
        await async_session.commit()
        if relationships:
            return await self.__class__.get(async_session, self.id, relationships)
        return self

    @classmethod
    async def get(
        cls,
        async_session: AsyncSession,
        id: UUID,
        relationships: list[QueryableAttribute] | None = None,
    ) -> Self:
        stmt = select(cls).where(cls.id == id)
        if relationships:
            stmt = stmt.options(*[joinedload(r) for r in relationships])
        result = await async_session.scalar(stmt)
        if not result:
            raise not_found(msg=f"{cls.__name__} not found")
        return result

    @classmethod
    async def all(cls, async_session: AsyncSession) -> Sequence[Self]:
        result = await async_session.execute(select(cls))
        return result.scalars().all()

    async def delete(self, async_session: AsyncSession):
        await async_session.delete(self)
        await async_session.commit()

    async def update(self, async_session: AsyncSession, **kwargs) -> Self:
        for key, value in kwargs.items():
            setattr(self, key, value)
        await async_session.commit()
        return self

    @overload
    @classmethod
    async def find(
        cls,
        async_session: AsyncSession,
        raise_: Literal[True],
        relationships: list[QueryableAttribute] | None = None,
        **kwargs,
    ) -> Self: ...

    @overload
    @classmethod
    async def find(
        cls,
        async_session: AsyncSession,
        raise_: Literal[False],
        relationships: list[QueryableAttribute] | None = None,
        **kwargs,
    ) -> Self | None: ...

    @classmethod
    async def find(
        cls,
        async_session: AsyncSession,
        raise_: bool = True,
        relationships: list[QueryableAttribute] | None = None,
        **kwargs,
    ) -> Self | None:
        stmt = select(cls).filter_by(**kwargs)
        if relationships:
            stmt = stmt.options(*[joinedload(r) for r in relationships])
        resp = await async_session.scalar(stmt)
        if not resp and raise_:
            raise not_found(msg=f"{cls.__name__} not found")
        return resp
