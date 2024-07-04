from fastapi import APIRouter, Depends, status

from app.models.auth.functions import authenticate
from app.models.auth.token import Token, TokenDecode, TokenEncode
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenEncode, status_code=status.HTTP_200_OK)
async def token(user: User = Depends(authenticate)):
    return Token(id=user.id, scope=user.scope).encode()


@router.get("/introspect", response_model=TokenDecode, status_code=status.HTTP_200_OK)
async def introspect(token: str):
    return Token.decode(token)
