import logging

from fastapi import (APIRouter, BackgroundTasks, Depends, Request, Security,
                     status)
from pydantic import EmailStr

from app.config import config
from app.functions.emailer import send_confirmation_email
from app.models.auth.functions import authorize_and_load
from app.models.auth.role import Role
from app.models.user import User, UserOut, UserRegister
from app.models.user.functions import get_verification_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def me(user: User = Depends(authorize_and_load)):
    return user


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(request: Request, user_register: UserRegister, bt: BackgroundTasks):
    user = User.model_validate(user_register).save()
    bt.add_task(request_verification, request, user.email, bt=bt)
    return user


@router.get("/request_verification/{email}", status_code=status.HTTP_200_OK)
async def request_verification(
    request: Request, email: EmailStr, bt: BackgroundTasks
) -> dict:
    token = get_verification_token(email)
    logger.debug(f"Verification token: {token}")
    if config.ENV_STATE == "test":
        return {"token": token}
    url = f"{request.url_for('verify')}?token={token}"
    logger.debug(f"Verification URL: {url}")
    bt.add_task(send_confirmation_email, email, url)
    return {"message": f"Verification email sent to {email}"}


@router.get("/verify", response_model=UserOut, status_code=status.HTTP_200_OK)
async def verify(user: User = Security(authorize_and_load, scopes=[Role.VERIFY])):
    return user.verify()
