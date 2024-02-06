import logging

from fastapi import HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

logger = logging.getLogger(__name__)


async def logger_exception_handler(request: Request, exc: HTTPException) -> Response:
    logger.error(f"HTTPException: {exc.status_code} - {exc.detail}")
    return await http_exception_handler(request, exc)
