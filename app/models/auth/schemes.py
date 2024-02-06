from typing import override

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from starlette.datastructures import MutableHeaders

from app.config import config


class OAuth2PasswordBearerWithQueryString(OAuth2PasswordBearer):
    @override
    async def __call__(self, request: Request) -> str | None:
        token = request.query_params.get("token")
        if token:
            new_headers = MutableHeaders(request.headers)
            new_headers["Authorization"] = f"Bearer {token}"
            request._headers = new_headers
        return await super().__call__(request)


oauth2_scheme = OAuth2PasswordBearerWithQueryString(tokenUrl=config.TOKEN_PATH)
