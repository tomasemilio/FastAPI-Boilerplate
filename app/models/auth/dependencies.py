from typing import Annotated

from fastapi import Depends, Security

from app.models.auth.functions import Authenticate, authorize, authorize_limited
from app.models.auth.role import Role
from app.models.auth.schemas import TokenDecode, TokenEncode
from app.models.user import User

authorizeDep = Annotated[TokenDecode, Depends(authorize)]

authorizeLimitDep = Annotated[TokenDecode, Depends(authorize_limited)]

authorizeLoadDep = Annotated[User, Depends(Authenticate().from_token)]

authorizeLoadRelationshipsDep = Annotated[User, Depends(Authenticate(True).from_token)]

authenticateDep = Annotated[User, Depends(Authenticate())]

authenticateTokenDep = Annotated[TokenEncode, Depends(Authenticate.to_token)]

authenticateRelationshipsDep = Annotated[User, Depends(Authenticate(True))]

resetLoadDep = Annotated[User, Security(Authenticate().from_token, scopes=[Role.RESET])]

__all__ = [
    "authorizeDep",
    "authorizeLimitDep",
    "authorizeLoadDep",
    "authorizeLoadRelationshipsDep",
    "authenticateDep",
    "authenticateTokenDep",
    "authenticateRelationshipsDep",
    "resetLoadDep",
]
