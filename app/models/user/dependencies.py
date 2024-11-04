from typing import Annotated

from fastapi import Depends

from app.models.user import User
from app.models.user.functions import load_user

userDep = Annotated[User, Depends(load_user)]
