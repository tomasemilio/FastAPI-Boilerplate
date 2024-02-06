from jose import jwt
from jose.exceptions import ExpiredSignatureError

from app.config import config
from app.functions.exceptions import expired_token, unauthorized_bearer


def encode(**kwargs) -> str:
    return jwt.encode(kwargs, config.SECRET_KEY, algorithm=config.ALGORITHM)


def decode(token: str) -> dict:
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    except ExpiredSignatureError:
        raise expired_token(msg="Token has expired")
    except Exception:
        raise unauthorized_bearer()
