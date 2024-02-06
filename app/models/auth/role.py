from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
