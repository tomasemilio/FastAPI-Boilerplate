from fastapi import APIRouter

router = APIRouter(prefix="/api")

from app.api.v1 import router as v1_router

router.include_router(v1_router)
