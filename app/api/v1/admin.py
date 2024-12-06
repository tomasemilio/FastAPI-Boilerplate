from fastapi import APIRouter, Security

from app.models.auth.functions import authorize
from app.models.auth.role import Role
from app.models.user.dependencies import (
    userCreateDep,
    userDeleteDep,
    userGetDep,
    usersGetDep,
    userUpdateDep,
)
from app.models.user.schemas import UserDetailOut, UserOut

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Security(authorize, scopes=[Role.ADMIN])],
)


@router.post("/user", response_model=UserDetailOut, status_code=201)
async def create_user(user: userCreateDep):
    return user


@router.get("/user", response_model=list[UserOut], status_code=200)
async def get_users(users: usersGetDep):
    return users


@router.get("/user/{id}", response_model=UserDetailOut, status_code=200)
async def get_user(user: userGetDep):
    return user


@router.delete("/user/{id}", status_code=204)
async def delete_user(_: userDeleteDep): ...


@router.put("/user/{id}", response_model=UserDetailOut, status_code=201)
async def update_user(user: userUpdateDep):
    return user
