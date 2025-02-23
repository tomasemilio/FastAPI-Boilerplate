from fastapi import APIRouter

router = APIRouter(prefix="/v1")

from app.api.v1.admin import router as admin_router
from app.api.v1.auth import router as auth_router
from app.api.v1.post import router as post_router
from app.api.v1.tag import router as tag_router
from app.api.v1.user import router as users_router

router.include_router(admin_router)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(post_router)
router.include_router(tag_router)
