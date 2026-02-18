# Setup Guide

## Prerequisites

- Node.js (recommended: 18+)
- Python 3.9+
- Docker + Docker Compose (recommended for PostgreSQL)

## 1) Clone and install

Frontend:

```bash
cd frontend
npm install
```

Backend:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## 2) Configure environment (backend)

```bash
cp backend/.env.example backend/.env
```

Minimum required for Azure Translator:

- `AZURE_TRANSLATOR_KEY`
- `AZURE_TRANSLATOR_REGION`

Optional:

- `AZURE_TRANSLATOR_CATEGORY` (Custom Translator category)
- `OPENAI_API_KEY` / `OPENAI_MODEL` (post-edit)

## 3) Start PostgreSQL (recommended)

This project includes a `docker-compose.yml` that starts PostgreSQL on `localhost:5432` and initializes:

- `source_texts` (with a few demo rows)

Start it:

```bash
docker compose up -d
```

Default DSN:

```text
postgresql://postgres:postgres@localhost:5432/postgres
```

If you do not start PostgreSQL:

- `/translate/text` and `/translate/url` will still work
- cache and `/translate/db` will be unavailable

## 4) Run the app

Backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm run dev
```

Open:

- Frontend: `http://localhost:4321`
- API docs: `http://localhost:8000/docs`

## 5) Configure using the Settings UI (recommended)

Open `http://localhost:4321/settings`.

- The UI stores settings in `localStorage`.
- You can click **Apply to backend** to set runtime config via `POST /config`.

Important:

- Runtime config is allowed only from **localhost** and is intended for local demos.
- In production, do not expose runtime key configuration.
