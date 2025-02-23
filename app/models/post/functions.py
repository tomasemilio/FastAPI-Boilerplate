from uuid import UUID

from app.database.dependencies import sessDep
from app.models.auth.dependencies import authorizeDep, authorizeLimitDep
from app.models.post import Post


async def load_post(async_session: sessDep, post_id: UUID, token: authorizeDep) -> Post:
    return await Post.find(
        async_session,
        id=post_id,
        user_id=token.id,
        raise_=True,
        relationships=[Post.user, Post.tags],
    )


async def load_post_limited(
    async_session: sessDep, post_id: UUID, token: authorizeLimitDep
) -> Post:
    return await Post.find(
        async_session,
        id=post_id,
        user_id=token.id,
        raise_=True,
        relationships=[Post.user, Post.tags],
    )
