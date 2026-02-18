from fastapi import APIRouter, HTTPException

from app.models.requests import DbTranslateRequest, TextTranslateRequest, UrlTranslateRequest
from app.models.responses import DbTranslateResponse, TextTranslateResponse, UrlTranslateResponse
from app.services.pipeline import translate_text_pipeline, translate_url_pipeline, translate_db_pipeline

router = APIRouter()


@router.post("/text", response_model=TextTranslateResponse)
def translate_text(req: TextTranslateRequest) -> TextTranslateResponse:
    try:
        return translate_text_pipeline(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/url", response_model=UrlTranslateResponse)
def translate_url(req: UrlTranslateRequest) -> UrlTranslateResponse:
    try:
        return translate_url_pipeline(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/db", response_model=DbTranslateResponse)
def translate_db(req: DbTranslateRequest) -> DbTranslateResponse:
    try:
        return translate_db_pipeline(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
