from uuid import UUID

from app.database.dependencies import sessDep
from app.models.auth.dependencies import authDep, authDepLimit
from app.models.post import Post


async def load_post(async_session: sessDep, id: UUID, token: authDep) -> Post:
    return await Post.find(
        async_session, id=id, user_id=token.id, raise_=True, relationships=[Post.user]
    )


async def load_post_limited(
    async_session: sessDep, id: UUID, token: authDepLimit
) -> Post:
    return await Post.find(
        async_session, id=id, user_id=token.id, raise_=True, relationships=[Post.user]
    )
