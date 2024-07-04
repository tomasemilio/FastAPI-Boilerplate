from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException

from app.api import router as api_router
from app.api.functions.handlers import logger_exception_handler
from app.api.functions.middleware import add_process_time_header, lifespan

app = FastAPI(lifespan=lifespan)

app.middleware("http")(add_process_time_header)
app.add_middleware(CorrelationIdMiddleware, header_name="X-Correlation-ID")
app.exception_handler(HTTPException)(logger_exception_handler)

app.include_router(api_router)
