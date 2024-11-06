from fastapi import APIRouter

from app.database.dependencies import sessDep
from app.functions.exceptions import conflict
from app.models.auth.dependencies import authDep, authLoadDep
from app.models.post.dependencies import postDep
from app.models.tag import Tag
from app.models.tag.dependencies import tagDep
from app.models.tag.schemas import TagDetailOut, TagIn, TagOut

router = APIRouter(prefix="/tag", tags=["Tag"])


@router.post("", response_model=TagDetailOut, status_code=201)
async def create_tag(tag_in: TagIn, async_session: sessDep, token: authDep):
    if await Tag.find(
        async_session=async_session, name=tag_in.name, user_id=token.id, raise_=False
    ):
        raise conflict(msg="Tag already exists")
    return await Tag(**tag_in.model_dump(), user_id=token.id).save(
        async_session, relationships=[Tag.user, Tag.posts]
    )


@router.get("", response_model=list[TagOut], status_code=200)
async def get_tags(user: authLoadDep):
    return user.tags


@router.get("/{tag_id}", response_model=TagDetailOut, status_code=200)
async def get_tag(tag: tagDep):
    return tag


@router.post("/{tag_id}/post/{post_id}", response_model=TagDetailOut, status_code=201)
async def associate_post(async_session: sessDep, tag: tagDep, post: postDep):
    if post not in tag.posts:
        tag.posts.append(post)
    return await tag.save(async_session)
