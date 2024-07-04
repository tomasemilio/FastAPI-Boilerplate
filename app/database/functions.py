import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.database import engine, local_session

logger = logging.getLogger(__name__)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with local_session() as session:
        yield session


async def create_all():
    from app.models.user import User  # noqa: F401

    async with engine.begin() as conn:
        logger.info("Creating all tables if they don't exist")
        await conn.run_sync(User.metadata.create_all)


async def drop_all():
    from app.models.user import User  # noqa: F401

    if config.ENV_STATE in config.DROP_ENVS:
        async with engine.begin() as conn:
            logger.warning("Dropping all tables")
            await conn.run_sync(User.metadata.drop_all)
    else:
        logger.warning("Dropping tables not allowed in this environment")
