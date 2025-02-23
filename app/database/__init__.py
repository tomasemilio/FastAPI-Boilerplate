from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import config

connect_args = (
    {"check_same_thread": False} if config.DB_URL.startswith("sqlite") else {}
)

engine = create_async_engine(
    config.DB_URL, connect_args=connect_args, pool_pre_ping=True
)

local_session = async_sessionmaker(engine, expire_on_commit=False)

