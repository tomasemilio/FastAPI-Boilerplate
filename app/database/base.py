from datetime import UTC, datetime
from typing import Annotated, Any, Self, Sequence
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlmodel import Field, Session, SQLModel, select

from app.database import engine
from app.functions.exceptions import not_found


class Base(SQLModel):
    id: Annotated[UUID, Field(default_factory=uuid4, primary_key=True, index=True)]
    created_at: Annotated[
        datetime,
        Field(
            default_factory=lambda: datetime.now(UTC),
            nullable=False,
            sa_column_kwargs={"server_default": text("current_timestamp")},
        ),
    ]
    updated_at: Annotated[
        datetime,
        Field(
            default_factory=lambda: datetime.now(UTC),
            nullable=False,
            sa_column_kwargs={
                "server_default": text("current_timestamp"),
                "onupdate": text("current_timestamp"),
            },
        ),
    ]

    def __init__(self, *args, **kwargs):
        self.model_config["table"] = False
        super().__init__(*args, **kwargs)
        self.model_config["table"] = True

    def get_property(self, name: str) -> Any | None:
        with Session(engine) as session:
            statement = select(type(self)).where(type(self).id == self.id)
            instance = session.exec(statement).first()
            return getattr(instance, name) if hasattr(instance, name) else None

    @classmethod
    def get(cls, id: UUID) -> Self:
        with Session(engine) as session:
            statement = select(cls).where(cls.id == id)
            resp = session.exec(statement).first()
            if resp is None:
                raise not_found(f"{cls.__name__} not found.")
            return resp

    @classmethod
    def find(cls, **kwargs) -> Self | None:
        with Session(engine) as session:
            statement = select(cls)
            for key, value in kwargs.items():
                statement = statement.where(getattr(cls, key) == value)
            return session.exec(statement).first()

    @classmethod
    def all(cls) -> Sequence[Self]:
        with Session(engine) as session:
            statement = select(cls)
            return session.exec(statement).all()

    def update(self, **kwargs) -> Self:
        with Session(engine) as session:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            session.add(self)
            session.commit()
            session.refresh(self)
        return self

    def delete(self):
        with Session(engine) as session:
            session.delete(self)
            session.commit()

    def save(self) -> Self:
        with Session(engine) as session:
            session.add(self)
            session.commit()
            session.refresh(self)
        return self
