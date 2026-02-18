# Azure AI Custom Translator Platform

![Desafio AzureAI da DIO (PT-BR)](https://img.shields.io/badge/Desafio-AzureAI%20da%20DIO-2563EB?style=for-the-badge)
![DIO AzureAI Challenge (EN)](https://img.shields.io/badge/Challenge-DIO%20AzureAI-2563EB?style=for-the-badge)

This contains everything you need to run the app locally.

## Tech Stack

- **Backend:** Python 3.9+, FastAPI, Uvicorn
- **Azure:** Azure AI Translator (supports Custom Translator category)
- **Optional post-editing:** OpenAI API (`gpt-4o-mini` by default)
- **Database:** PostgreSQL (cache + batch jobs)
- **Frontend:** Astro + TypeScript

Key libraries:

- **HTTP:** httpx
- **Retries:** tenacity
- **Database driver:** psycopg
- **Article extraction:** trafilatura + beautifulsoup4
- **Markdown:** markdownify (backend), marked (frontend)

## Run Locally

**Prerequisites:**

- Node.js
- Python 3.9+
- Docker (recommended for PostgreSQL)

### 1) Install dependencies

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

### 2) Configure environment

Backend:

```bash
cp backend/.env.example backend/.env
```

Set at least:

- `AZURE_TRANSLATOR_KEY`
- `AZURE_TRANSLATOR_REGION`

Optional:

- `AZURE_TRANSLATOR_CATEGORY`
- `OPENAI_API_KEY`

### 3) Start PostgreSQL (recommended)

This repo includes a `docker-compose.yml` that runs PostgreSQL on `localhost:5432` and initializes a demo `source_texts` table.

```bash
docker compose up -d
```

To stop it:

```bash
docker compose down
```

Default DSN:

```text
postgresql://postgres:postgres@localhost:5432/postgres
```

## Azure Setup Notes

- **Translator resource:** create a Translator resource in Azure Portal, then copy `AZURE_TRANSLATOR_KEY` and `AZURE_TRANSLATOR_REGION` from "Keys and Endpoint".
- **Custom Translator (category):** after training/publishing a model, set `AZURE_TRANSLATOR_CATEGORY` with the Translator API Category ID.

Frontend:

```bash
cd frontend
cp .env.example .env
```

### 4) Run

Backend (Terminal 1):

```bash
uvicorn app.main:app --reload --port 8000
```

Frontend (Terminal 2):

```bash
npm --prefix frontend run dev
```

Alternative (repo root scripts):

```bash
npm run dev:backend
```

and in another terminal:

```bash
npm run dev:frontend
```

Open:

- `http://localhost:4321`

Backend API docs:

- `http://localhost:8000/docs`

## Settings Panel (recommended)

The frontend includes a Settings panel (`/settings`) that:

- stores configuration in your browser (`localStorage`)
- can apply runtime configuration to the backend via `POST /config` (**localhost only**) for easy demos

For production deployments, do not expose runtime key configuration like this.

Recommended local demo workflow:

1. Open `http://localhost:4321/settings`
2. Set:
   - Backend API Base URL: `http://localhost:8000`
   - Azure Translator Key + Region
   - (Optional) OpenAI key + model
   - PostgreSQL DSN (default should work if you started Docker Compose)
3. Click **Apply to backend**
4. Use:
   - `/text` for text translation
   - `/article` for web article localization
   - `/batch` to run batch jobs

Batch verification:

- Docker init SQL creates `source_texts` and seeds demo rows.
- Go to `/batch` and run with `limit=100`.

## API

- `GET /health`
- `POST /translate/text`
- `POST /translate/url`
- `POST /translate/db`

## Documentation

Full documentation lives under `docs/`:

- [`docs/SETUP.md`](docs/SETUP.md) (install + run + PostgreSQL via Docker Compose)
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (high-level architecture + dataflow diagram)
- [`docs/USAGE.md`](docs/USAGE.md) (how to use Text/Article/Batch/Settings)
- [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) (common errors and fixes)

PostgreSQL initialization:

- `docker-compose.yml` mounts `backend/sql/init/` into Postgres init.
- `backend/sql/init/001_init.sql` creates `source_texts` and seeds demo rows.
