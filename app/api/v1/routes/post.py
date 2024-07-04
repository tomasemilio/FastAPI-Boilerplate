from fastapi import APIRouter, Depends

from app.database.dependencies import sessDep
from app.models.auth.functions import authorize, authorize_and_load
from app.models.auth.token import TokenDecode
from app.models.post import Post
from app.models.post.schemas import PostIn, PostOut
from app.models.user import User

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("", response_model=PostOut, status_code=201)
async def create_post(
    post_in: PostIn,
    async_session: sessDep,
    token: TokenDecode = Depends(authorize),
):
    return await Post(**post_in.model_dump(), user_id=token.id).save(async_session)


@router.get("", response_model=list[PostOut], status_code=200)
async def get_posts(user: User = Depends(authorize_and_load)):
    return await user.awaitable_attrs.posts


@router.get("/{id}", response_model=PostOut, status_code=200)
async def get_post(
    async_session: sessDep, id: str, token: TokenDecode = Depends(authorize)
):
    return await Post.find(async_session, id=id, user_id=token.id, raise_=True)


@router.delete("/{id}", status_code=204)
async def delete_post(
    async_session: sessDep, id: str, token: TokenDecode = Depends(authorize)
):
    post = await Post.find(async_session, id=id, user_id=token.id, raise_=True)
    await post.delete(async_session)  # type: ignore
