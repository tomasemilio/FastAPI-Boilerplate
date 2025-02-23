from typing import Annotated

from fastapi import Depends

from app.models.tag import Tag
from app.models.tag.functions import load_tag

tagDep = Annotated[Tag, Depends(load_tag)]
