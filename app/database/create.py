import logging

from sqlmodel import SQLModel

from app.config import config
from app.database import engine
from app.models.auth.role import Role
from app.models.post import Post
from app.models.user import User

logger = logging.getLogger(__name__)


def create():
    SQLModel.metadata.create_all(bind=engine)

    admin_user = User.find(email=config.ADMIN_EMAIL)
    if not admin_user:
        logger.info("Creating admin user")
        admin_user = User(
            name="admin",
            email=config.ADMIN_EMAIL,
            password=config.ADMIN_PASSWORD,
            scope=[Role.ADMIN],
            verified=True,
        )
        admin_user.save()


def drop_all():
    if config.ENV_STATE == "test":
        SQLModel.metadata.drop_all(bind=engine)
    else:
        raise ValueError("You can only drop all tables in test environment")
