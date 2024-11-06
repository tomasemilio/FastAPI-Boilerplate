from uuid import UUID

from app.database.dependencies import sessDep
from app.models.auth.dependencies import authDep
from app.models.tag import Tag


async def load_tag(async_session: sessDep, tag_id: UUID, token: authDep) -> Tag:
    return await Tag.find(
        async_session,
        id=tag_id,
        user_id=token.id,
        raise_=True,
        relationships=[Tag.user, Tag.posts],
    )
