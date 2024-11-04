from fastapi import APIRouter, BackgroundTasks
from pydantic import EmailStr

from app.config import config
from app.database.dependencies import sessDep
from app.functions.emailer import send_email
from app.models.auth.dependencies import authLoadDep, resetLoadDep
from app.models.auth.role import Role
from app.models.auth.token import Token
from app.models.user import User
from app.models.user.schemas import PasswordsIn, UserDetailOut

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserDetailOut, status_code=200)
async def me(user: authLoadDep):
    return user


@router.get("/request-reset-password/{email}", status_code=200)
async def request_reset_password(
    async_session: sessDep, email: EmailStr, bt: BackgroundTasks
) -> dict:
    user = await User.find(async_session, raise_=True, email=email)
    token = (
        Token(
            id=user.id,  # type: ignore
            scope=[Role.RESET],
            expires_in=config.RESET_EXPIRE_SECONDS,
        )
        .encode()
        .access_token
    )
    if config.ENV_STATE == "test":
        return {"message": token}
    content = f"Use the following token/link to reset your password: {token}"
    subject = "Reset Password"
    bt.add_task(send_email, email=email, subject=subject, content=content)
    return {"message": f"Reset password email sent to {email}"}


@router.post("/reset-password", status_code=200, response_model=UserDetailOut)
async def reset_password(
    async_session: sessDep,
    passwords: PasswordsIn,
    user: resetLoadDep,
    token: str | None = None,  # noqa: F841
):
    user = await User.get(
        async_session, id=user.id, relationships=[User.posts]
    )  # sessDep not cached when using Security Scopes
    return await user.update(
        async_session, verified=True, password=passwords.password.get_secret_value()
    )
