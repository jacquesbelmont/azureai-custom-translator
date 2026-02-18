from fastapi import APIRouter

from app.api.translate import router as translate_router

router = APIRouter()
router.include_router(translate_router, prefix="/translate", tags=["translate"])
