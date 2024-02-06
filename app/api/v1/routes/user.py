from fastapi import APIRouter, Depends, status

from app.models.auth.functions import authorize_and_load
from app.models.user import User, UserOut

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def me(user: User = Depends(authorize_and_load)):
    return user
