import logging
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes

from app.database.dependencies import sessDep
from app.functions.exceptions import forbidden, unauthorized_basic
from app.functions.limiter import rate_limiter
from app.models.auth.role import Role
from app.models.auth.schemas import TokenDecode, TokenEncode
from app.models.auth.schemes import oauth2_scheme
from app.models.auth.token import Token
from app.models.user import User

logger = logging.getLogger(__name__)


async def authenticate(
    async_session: sessDep, credentials: OAuth2PasswordRequestForm = Depends()
) -> User:
    user = await User.find(async_session, email=credentials.username)
    if not user or not user.check_password(credentials.password):
        raise unauthorized_basic()
    elif user.verified is False:
        raise forbidden("User not verified. Request reset password.")
    logger.info(f"Authenticating user id:{user.id} and email:{user.email}")
    return user


async def authenticate_and_token(user: User = Depends(authenticate)) -> TokenEncode:
    logger.info(f"Generating token for user id:{user.id} and email:{user.email}")
    return Token(id=user.id, scope=user.scope).encode()


def authorize(
    token: Annotated[str, Depends(oauth2_scheme)],
    security_scopes: Annotated[SecurityScopes, Depends],
) -> TokenDecode:
    logger.info(f"Authorizing token:{token}")
    return Token.decode(token=token, scope=[Role(i) for i in security_scopes.scopes])


def authorize_limited(token: Annotated[TokenDecode, Depends(authorize)]) -> TokenDecode:
    rate_limiter(token.id)
    return token


async def authorize_and_load(
    async_session: sessDep, token: Annotated[TokenDecode, Depends(authorize)]
) -> User:
    user = await User.get(async_session, id=token.id)
    logger.info(f"Authorizing and loading user id:{token.id} and email:{user.email}")
    return user
