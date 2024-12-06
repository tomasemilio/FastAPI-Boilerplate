import logging
from typing import Annotated, Sequence
from uuid import UUID

from fastapi import BackgroundTasks, Depends

from app.api.v1.user import request_reset_password
from app.config import config
from app.database import local_session
from app.database.dependencies import sessDep
from app.functions.exceptions import conflict
from app.models.auth.role import Role
from app.models.user import User
from app.models.user.schemas import UserIn, UserUpdate

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


async def get_user(async_session: sessDep, id: UUID) -> User:
    return await User.get(
        async_session=async_session, id=id, relationships=[User.posts, User.tags]
    )


userGetDep = Annotated[User, Depends(get_user)]


async def create_user(
    async_session: sessDep,
    bt: BackgroundTasks,
    user_in: UserIn,
    send_email: bool = True,
) -> User:
    if await User.find(async_session=async_session, email=user_in.email, raise_=False):
        raise conflict(msg="User already exists")
    user = await User(**user_in.model_dump()).save(
        async_session, relationships=[User.posts, User.tags]
    )
    if send_email:
        await request_reset_password(async_session, email=user.email, bt=bt)
    return user


async def get_users(async_session: sessDep) -> Sequence[User]:
    return await User.all(async_session)


async def delete_user(async_session: sessDep, user: userGetDep):
    await user.delete(async_session)


async def update_user(
    async_session: sessDep, user: userGetDep, user_update: UserUpdate
) -> User:
    return await user.update(async_session, **user_update.model_dump(exclude_none=True))
