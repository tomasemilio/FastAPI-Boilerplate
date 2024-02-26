from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes

from app.functions.exceptions import forbidden, unauthorized_basic
from app.models.auth.role import Role
from app.models.auth.schemes import oauth2_scheme
from app.models.auth.token import Token, TokenDecode
from app.models.user import User


def authenticate(credentials: OAuth2PasswordRequestForm = Depends()) -> User:
    user = User.find(email=credentials.username)
    if not user or not user.verify_password(credentials.password):
        raise unauthorized_basic()
    elif user.verified is False:
        raise forbidden("User not verified. Request verification email.")
    return user


def authorize(
    token: Annotated[str, Depends(oauth2_scheme)],
    security_scopes: Annotated[SecurityScopes, Depends],
) -> TokenDecode:
    return Token.decode(token=token, scope=[Role(i) for i in security_scopes.scopes])


def authorize_and_load(token: Annotated[TokenDecode, Depends(authorize)]) -> User:
    return User.get(id=token.id)
