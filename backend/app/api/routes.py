from fastapi import APIRouter

from app.api.config import router as config_router
from app.api.translate import router as translate_router

router = APIRouter()
router.include_router(config_router, tags=["config"])
router.include_router(translate_router, prefix="/translate", tags=["translate"])
