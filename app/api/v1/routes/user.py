from fastapi import APIRouter, Depends, status

from app.config import config
from app.models.auth.functions import authorize_and_load
from app.models.auth.role import Role
from app.models.auth.token import Token
from app.models.user import User, UserOut, UserRegister

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def me(user: User = Depends(authorize_and_load)):
    return user


@router.post("", response_model=str, status_code=status.HTTP_200_OK)
async def register(user_register: UserRegister):
    user = User.model_validate(user_register)
    token = Token(
        id=user.id, scope=[Role.VERIFY], expires_in=config.VERIFY_EXPIRE_SECONDS
    )
    return token.encode().access_token
