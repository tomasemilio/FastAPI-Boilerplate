from fastapi import APIRouter, Security, status

from app.models.auth.functions import authorize
from app.models.auth.role import Role
from app.models.auth.token import Token, TokenEncode
from app.models.user import User, UserIn, UserOut

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Security(authorize, scopes=[Role.ADMIN])],
)


@router.get("/token", response_model=TokenEncode, status_code=status.HTTP_200_OK)
async def get_admin_token(id: str, scope: Role, expires_in: int):
    return Token(id=id, scope=[scope], expires_in=expires_in).encode()


@router.post("/user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserIn):
    return User.model_validate(user_in).save()


@router.get("/user", response_model=list[UserOut], status_code=status.HTTP_200_OK)
async def read_users():
    return User.all()


@router.get("/user/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def read_user(id: str):
    return User.get(id=id)


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    User.get(id=id).delete()


@router.patch("/user/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(id: str, user_in: UserIn):
    user = User.get(id=id)
    return user.update(**user_in.model_dump(exclude_unset=True))
