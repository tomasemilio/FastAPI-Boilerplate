from fastapi import APIRouter, status

from app.models.auth.dependencies import userDep
from app.models.auth.schemas import TokenDecode, TokenEncode
from app.models.auth.token import Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenEncode, status_code=status.HTTP_200_OK)
async def token(user: userDep):
    return Token(id=user.id, scope=user.scope).encode()


@router.get("/introspect", response_model=TokenDecode, status_code=status.HTTP_200_OK)
async def introspect(token: str):
    return Token.decode(token)
