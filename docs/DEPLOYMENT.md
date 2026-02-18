# Deployment (Free Tier)

This guide deploys without changing project structure:

- **Backend:** Render (FastAPI)
- **Frontend:** Netlify (Astro static build)
- **PostgreSQL:** Neon (serverless Postgres)

## 1) Create a Neon Postgres database

1. Sign up at Neon.
2. Create a new project/database.
3. Copy the connection string (DSN).

Example DSN format:

```text
postgresql://USER:PASSWORD@HOST/DB?sslmode=require
```

## 2) Deploy the backend to Render

### Create the Render Web Service

1. Go to Render Dashboard -> New -> **Web Service**
2. Connect your GitHub repo
3. Select the repo and set:

- **Root directory:** `backend`
- **Runtime:** Python
- **Build command:**

```bash
pip install -r requirements.txt
```

- **Start command:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Set Render Environment Variables

In Render -> Environment:

- `AZURE_TRANSLATOR_KEY` = your Azure Translator key
- `AZURE_TRANSLATOR_REGION` = your Azure Translator region
- `AZURE_TRANSLATOR_ENDPOINT` = `https://api.cognitive.microsofttranslator.com`
- `AZURE_TRANSLATOR_CATEGORY` = optional (Custom Translator category)

Optional OpenAI:

- `OPENAI_API_KEY`
- `OPENAI_MODEL` (default: `gpt-4o-mini`)

Postgres (Neon):

- `POSTGRES_DSN` = Neon DSN

CORS (IMPORTANT):

- `CORS_ALLOW_ORIGINS` = `https://<your-netlify-site>.netlify.app`

You can include multiple origins separated by commas:

```text
CORS_ALLOW_ORIGINS=https://<your-netlify-site>.netlify.app,https://your-custom-domain.com
```

### Verify backend

After deploy, open:

- `https://<your-render-service>.onrender.com/health`
- `https://<your-render-service>.onrender.com/docs`

## 3) Deploy the frontend to Netlify

### Create a Netlify site

1. Netlify -> Add new site -> **Import from Git**
2. Select your repo

Build settings:

- **Base directory:** `frontend`
- **Build command:** `npm ci && npm run build`
- **Publish directory:** `frontend/dist`

Deploy.

### Configure the app to use the Render API

The app reads API base URL from the Settings page (saved in `localStorage`).

After deploy:

1. Open `https://<your-netlify-site>.netlify.app/settings`
2. Set:
   - **Backend API Base URL**: `https://<your-render-service>.onrender.com`
   - Azure/OpenAI/Postgres values if you want to override defaults locally
3. Click **Save locally**

Notes:

- The button **Apply to backend** uses `POST /config` which is **localhost-only** and will not work in production.
- In production, configure secrets on Render environment variables.

## 4) Postgres schema (Neon)

Neon does not run Docker init SQL.

You have two options:

### Option A: Manually create the source table

Run this in Neon SQL editor:

```sql
CREATE TABLE IF NOT EXISTS source_texts (
  id TEXT PRIMARY KEY,
  source_text TEXT NOT NULL
);
```

### Option B: Disable batch

If you do not need `/translate/db`, you can skip Postgres.

## Troubleshooting

- **CORS errors in browser:**
  - Ensure `CORS_ALLOW_ORIGINS` in Render includes your Netlify domain
  - Redeploy Render after changing env vars

- **Batch returns 503:**
  - Check Neon DSN in `POSTGRES_DSN`
  - Ensure the table `source_texts` exists

- **Translator errors:**
  - Validate Azure key/region

