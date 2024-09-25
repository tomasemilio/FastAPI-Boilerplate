from typing import Annotated

from fastapi import Depends, Security

from app.models.auth.functions import (
    authenticate,
    authenticate_and_token,
    authorize,
    authorize_and_load,
    authorize_limited,
)
from app.models.auth.role import Role
from app.models.auth.schemas import TokenDecode
from app.models.user import User

authDep = Annotated[TokenDecode, Depends(authorize)]

userDep = Annotated[User, Depends(authenticate)]

authLoadDep = Annotated[User, Depends(authorize_and_load)]

authTokenDep = Annotated[User, Depends(authenticate_and_token)]

resetLoadDep = Annotated[User, Security(authorize_and_load, scopes=[Role.RESET])]

authDepLimit = Annotated[TokenDecode, Depends(authorize_limited)]
