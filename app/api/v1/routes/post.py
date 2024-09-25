from uuid import UUID

from fastapi import APIRouter

from app.database.dependencies import sessDep
from app.models.auth.dependencies import authDep, authDepLimit, authLoadDep
from app.models.post import Post
from app.models.post.schemas import PostIn, PostOut

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("", response_model=PostOut, status_code=201)
async def create_post(post_in: PostIn, async_session: sessDep, token: authDep):
    return await Post(**post_in.model_dump(), user_id=token.id).save(async_session)


@router.get("", response_model=list[PostOut], status_code=200)
async def get_posts(user: authLoadDep):
    return await user.awaitable_attrs.posts


@router.get("/{id}", response_model=PostOut, status_code=200)
async def get_post(async_session: sessDep, id: UUID, token: authDep):
    return await Post.find(async_session, id=id, user_id=token.id, raise_=True)


@router.get("/rate-limited/{id}", response_model=PostOut, status_code=200)
async def get_post_rate_limited(async_session: sessDep, id: UUID, token: authDepLimit):
    return await Post.find(async_session, id=id, user_id=token.id, raise_=True)


@router.delete("/{id}", status_code=204)
async def delete_post(async_session: sessDep, id: UUID, token: authDep):
    post = await Post.find(async_session, id=id, user_id=token.id, raise_=True)
    await post.delete(async_session)
