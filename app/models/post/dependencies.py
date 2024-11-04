from typing import Annotated

from fastapi import Depends

from app.models.post import Post
from app.models.post.functions import load_post, load_post_limited

postDep = Annotated[Post, Depends(load_post)]

postDepLimit = Annotated[Post, Depends(load_post_limited)]
