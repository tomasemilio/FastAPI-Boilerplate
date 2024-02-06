import bcrypt


def get_hash(value: str) -> str:
    return bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_hash(value: str, hashed: str) -> bool:
    return bcrypt.checkpw(value.encode("utf-8"), hashed.encode("utf-8"))
