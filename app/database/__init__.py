from sqlmodel import create_engine

from app.config import config

engine = create_engine(url=config.DB_URL, pool_pre_ping=True)
