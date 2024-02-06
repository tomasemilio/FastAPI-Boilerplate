from sqlmodel import create_engine

from app.config import config

if config.DB_URL:
    connect_args = (
        {"check_same_thread": False} if config.DB_URL.startswith("sqlite") else {}
    )
    engine = create_engine(
        url=config.DB_URL,
        pool_pre_ping=True,
        connect_args=connect_args,
        pool_size=10,
    )
