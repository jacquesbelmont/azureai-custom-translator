from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.settings import settings
from app.db.cache import ensure_cache_table

app = FastAPI(title="Azure AI Custom Translator Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    try:
        ensure_cache_table()
    except Exception as e:
        # Allow running without Postgres for local demos.
        print(f"[startup] Postgres/cache not available yet: {type(e).__name__}: {e}")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(router)
