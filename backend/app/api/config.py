from fastapi import APIRouter, HTTPException, Request

from app.core.runtime_config import get_all_overrides, set_overrides
from app.models.config import RuntimeConfigRequest, RuntimeConfigResponse

router = APIRouter()


def _is_localhost(request: Request) -> bool:
    host = request.client.host if request.client else ""
    return host in {"127.0.0.1", "localhost", "::1"}


@router.get("/config", response_model=RuntimeConfigResponse)
def get_config() -> RuntimeConfigResponse:
    return RuntimeConfigResponse(applied=True, overrides=get_all_overrides())


@router.post("/config", response_model=RuntimeConfigResponse)
def set_config(request: Request, payload: RuntimeConfigRequest) -> RuntimeConfigResponse:
    if not _is_localhost(request):
        raise HTTPException(status_code=403, detail="Runtime config is only allowed from localhost.")

    set_overrides(payload.model_dump(exclude_none=True))
    return RuntimeConfigResponse(applied=True, overrides=get_all_overrides())
