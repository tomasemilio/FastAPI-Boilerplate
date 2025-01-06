from typing import Annotated, Sequence

from fastapi import Depends

from app.models.user import User
from app.models.user.functions import (
    create_user,
    delete_user,
    get_users,
    update_user,
    userGetDep,
)

userCreateDep = Annotated[User, Depends(create_user)]

usersGetDep = Annotated[Sequence[User], Depends(get_users)]

userUpdateDep = Annotated[User, Depends(update_user)]

userDeleteDep = Annotated[None, Depends(delete_user)]


__all__ = ["userGetDep", "userCreateDep", "usersGetDep", "userDeleteDep"]
