from fastapi import APIRouter

from app.database.dependencies import sessDep
from app.models.auth.dependencies import authDep, authLoadDep
from app.models.post import Post
from app.models.post.dependencies import postDep, postDepLimit
from app.models.post.schemas import PostDetailOut, PostIn, PostOut

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("", response_model=PostDetailOut, status_code=201)
async def create_post(post_in: PostIn, async_session: sessDep, token: authDep):
    return await Post(**post_in.model_dump(), user_id=token.id).save(
        async_session, relationships=[Post.user, Post.tags]
    )


@router.get("", response_model=list[PostOut], status_code=200)
async def get_posts(user: authLoadDep):
    return user.posts


@router.get("/{post_id}", response_model=PostDetailOut, status_code=200)
async def get_post(post: postDep):
    return post


@router.get("/rate-limited/{post_id}", response_model=PostDetailOut, status_code=200)
async def get_post_rate_limited(post: postDepLimit):
    return post


@router.delete("/{post_id}", status_code=204)
async def delete_post(async_session: sessDep, post: postDep):
    await post.delete(async_session)
