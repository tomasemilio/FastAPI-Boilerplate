from fastapi import APIRouter, Depends, status

from app.functions.exceptions import not_found
from app.models.auth.functions import authorize, authorize_and_load
from app.models.auth.token import TokenDecode
from app.models.post import Post, PostIn
from app.models.user import User

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_in: PostIn, token: TokenDecode = Depends(authorize)):
    return Post(**post_in.model_dump(), user_id=token.id).save()


@router.get("", response_model=list[Post], status_code=status.HTTP_200_OK)
async def get_posts(user: User = Depends(authorize_and_load)):
    return user.get_property("posts")


@router.get("/{id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post(id: str, token: TokenDecode = Depends(authorize)):
    return Post.find(id=id, user_id=token.id) or not_found("Post not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str, token: TokenDecode = Depends(authorize)):
    post = Post.find(id=id, user_id=token.id)
    if not post:
        raise not_found("Post not found")
    post.delete()
