import logging
from uuid import UUID

from app.config import config
from app.database import local_session
from app.database.dependencies import sessDep
from app.models.auth.role import Role
from app.models.user import User

logger = logging.getLogger(__name__)


async def create_admin_user() -> User:
    async with local_session() as async_session:
        admin = await User.find(async_session, email=config.ADMIN_EMAIL, raise_=False)
        if not admin:
            logger.info("Admin user not found. Creating one.")
            admin = await User(
                name="admin",
                email=config.ADMIN_EMAIL,
                password=config.ADMIN_PASSWORD,
                verified=True,
                scope=[Role.ADMIN],
            ).save(async_session=async_session)
        return admin


async def load_user(async_session: sessDep, id: UUID) -> User:
    return await User.get(
        async_session=async_session, id=id, relationships=[User.posts, User.tags]
    )
