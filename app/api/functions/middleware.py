import logging
import time
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, Request

from app.database.create import create
from app.functions.logger import setup_logger

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logger()
    logger.info("Starting the application")
    create()
    yield
    logger.info("Shutting down the application")


async def add_process_time_header(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
