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


def authorize(
    token: Annotated[str, Depends(oauth2_scheme)],
    security_scopes: Annotated[SecurityScopes, Depends],
) -> TokenDecode:
    decoded_token = Token.decode(
        token=token, scope=[Role(i) for i in security_scopes.scopes]
    )
    logger.info(f"Authorizing user {decoded_token.id=} with {decoded_token.scope=}")
    return decoded_token


def authorize_limited(token: Annotated[TokenDecode, Depends(authorize)]) -> TokenDecode:
    rate_limiter(token.id.hex)
    return token


class Authenticate:
    def __init__(self, load_relationships: bool = False):
        self.relationships = [User.posts, User.tags] if load_relationships else None

    async def __call__(
        self, async_session: sessDep, credentials: OAuth2PasswordRequestForm = Depends()
    ) -> User:
        user = await User.find(
            async_session,
            email=credentials.username,
            raise_=False,
            relationships=self.relationships,
        )
        if not user or not user.check_password(credentials.password):
            raise unauthorized_basic()
        elif user.verified is False:
            raise forbidden("User not verified. Request reset password.")
        logger.info(
            f"Authenticating {user.id=} and {user.email=} relationships={self.relationships}"
        )
        return user

    async def from_token(
        self, async_session: sessDep, token: Annotated[TokenDecode, Depends(authorize)]
    ) -> User:
        user = await User.get(
            async_session, id=token.id, relationships=self.relationships
        )
        logger.info(f"Authorizing token and loading {user.id=} and {user.email=}")
        return user

    @classmethod
    async def to_token(
        cls,
        async_session: sessDep,
        credentials: OAuth2PasswordRequestForm = Depends(),
    ) -> TokenEncode:
        user = await cls()(async_session, credentials)
        logger.info(f"Generating token for {user.id=} and {user.email=}")
        return Token(id=user.id, scope=user.scope).encode()
