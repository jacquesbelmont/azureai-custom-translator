# Production Notes (Free-tier friendly)

This project can be deployed to production. It was designed to run safely with environment-based configuration and a clean frontend/backend separation.

This document summarizes what is production-ready today, what to configure, and what to consider when deploying on free tiers.

## Recommended free-tier deployment

- **Backend:** Render (FastAPI)
- **Frontend:** Netlify (Astro static)
- **Database:** Neon (PostgreSQL)

See the step-by-step guide: `docs/DEPLOYMENT.md`.

## What is production-ready

- **Backend API** implemented with FastAPI and typed request/response models.
- **CORS** can be configured using `CORS_ALLOW_ORIGINS`.
- **Secrets** (Azure/OpenAI keys, Postgres DSN) are read from environment variables.
- **Graceful degradation:**
  - If Postgres is down/unconfigured, `/translate/text` and `/translate/url` still work.
  - `/translate/db` returns a clear 503 when Postgres is unavailable.
- **PostgreSQL caching** reduces translation cost and improves speed.

## Security notes

## Runtime config endpoint (`POST /config`)

- `POST /config` is **localhost-only** by design.
- In production you should configure the backend via environment variables (Render dashboard), not via runtime override.

## CORS

In production, set:

- `CORS_ALLOW_ORIGINS=https://<your-netlify-site>.netlify.app`

If you use a custom domain, add it too (comma-separated).

## Data storage

Postgres is used for:

- cache table (`translation_cache`)
- batch processing (`source_texts` -> `translated_texts`)

On Neon, you need to create tables manually (Neon does not run Docker init scripts).

Minimum schema for batch:

```sql
CREATE TABLE IF NOT EXISTS source_texts (
  id TEXT PRIMARY KEY,
  source_text TEXT NOT NULL
);
```

Cache table is created automatically by the backend at runtime when Postgres is available.

## Operational considerations (free tier)

- **Cold starts:** Render free tier may sleep; first request can be slower.
- **Timeouts / rate limits:** Azure/OpenAI have quotas and rate limiting.
- **Logging:** Use Render logs for debugging.

## Recommended environment variables (backend)

Azure:

- `AZURE_TRANSLATOR_ENDPOINT`
- `AZURE_TRANSLATOR_KEY`
- `AZURE_TRANSLATOR_REGION`
- `AZURE_TRANSLATOR_CATEGORY` (optional)

OpenAI (optional):

- `OPENAI_API_KEY`
- `OPENAI_MODEL`

Postgres:

- `POSTGRES_DSN`

CORS:

- `CORS_ALLOW_ORIGINS`

## Quick verification checklist

- Backend health: `GET /health` returns `{ "status": "ok" }`
- Frontend loads and can translate text
- Browser has no CORS errors
- Batch endpoint works when Postgres is configured
