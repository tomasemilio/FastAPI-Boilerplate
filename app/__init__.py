from fastapi import FastAPI

from app.api import router as api_router
from app.api.functions.middleware import add_process_time_header, lifespan

app = FastAPI(lifespan=lifespan)

app.middleware("http")(add_process_time_header)

app.include_router(api_router)
