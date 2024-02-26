from pydantic import EmailStr

from app.config import config
from app.functions.exceptions import conflict, not_found
from app.models.auth.role import Role
from app.models.auth.token import Token
from app.models.user import User


def get_verification_token(email: EmailStr) -> str:
    user = User.find(email=email)
    if not user:
        raise not_found(msg="User not found.")
    elif user.verified:
        raise conflict("User already verified.")
    token = Token(
        id=user.id,
        scope=[Role.VERIFY],
        expires_in=config.VERIFY_EXPIRE_SECONDS,
    )
    return token.encode().access_token
