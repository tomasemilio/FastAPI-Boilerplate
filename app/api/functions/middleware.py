import logging
import time
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, Request

from app.config import config
from app.database.functions import create_all, drop_all
from app.functions.logger import setup_logger
from app.models.user.functions import create_admin_user

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logger()
    logger.warning(f"Starting the application: ENV={config.ENV_STATE}")
    await create_all()
    await create_admin_user()
    yield
    await drop_all()
    logger.warning("Shutting down the application")


async def add_process_time_header(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(f"Processing time: {process_time: .6f}")
    return response
