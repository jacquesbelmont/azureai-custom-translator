# Deployment Checklist (Render + Netlify + Neon)

Use this as a quick execution checklist. For full details, see `docs/DEPLOYMENT.md`.

## 0) Prereqs

- GitHub repo pushed
- Azure Translator key + region ready
- Optional: OpenAI key

## 1) Neon (PostgreSQL)

1. Create a Neon project/database.
2. Copy the DSN (connection string).
3. In Neon SQL editor, run:

```sql
CREATE TABLE IF NOT EXISTS source_texts (
  id TEXT PRIMARY KEY,
  source_text TEXT NOT NULL
);
```

4. (Optional) Insert a couple of rows:

```sql
INSERT INTO source_texts (id, source_text) VALUES
  ('prod-001', 'Hello from Neon!'),
  ('prod-002', 'This row is used to test /translate/db.')
ON CONFLICT (id) DO UPDATE SET
  source_text = EXCLUDED.source_text;
```

## 2) Render (Backend)

1. Render -> New -> **Web Service**
2. Connect GitHub repo
3. Settings:

- Root directory: `backend`
- Runtime: Python
- Build command:

```bash
pip install -r requirements.txt
```

- Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

4. Environment variables:

- `AZURE_TRANSLATOR_ENDPOINT` = `https://api.cognitive.microsofttranslator.com`
- `AZURE_TRANSLATOR_KEY` = `<your key>`
- `AZURE_TRANSLATOR_REGION` = `<your region>`
- `AZURE_TRANSLATOR_CATEGORY` = optional

Optional OpenAI:

- `OPENAI_API_KEY` = optional
- `OPENAI_MODEL` = optional (default: `gpt-4o-mini`)

Postgres:

- `POSTGRES_DSN` = `<your Neon DSN>`

CORS (IMPORTANT):

- Set later after Netlify is created:
  - `CORS_ALLOW_ORIGINS` = `https://<your-netlify-site>.netlify.app`

5. Deploy.
6. Verify:

- `https://<render-service>.onrender.com/health`
- `https://<render-service>.onrender.com/docs`

## 3) Netlify (Frontend)

1. Netlify -> Add new site -> **Import from Git**
2. Build settings:

- Base directory: `frontend`
- Build command: `npm ci && npm run build`
- Publish directory: `frontend/dist`

3. Deploy.
4. Copy the Netlify site URL.

## 4) Finalize CORS on Render

1. Render -> Backend service -> Environment
2. Set:

```text
CORS_ALLOW_ORIGINS=https://<your-netlify-site>.netlify.app
```

3. Redeploy (or restart) the Render service.

## 5) Configure the app in production

1. Open: `https://<your-netlify-site>.netlify.app/settings`
2. Set:
   - Backend API Base URL: `https://<render-service>.onrender.com`
3. Click **Save locally**

Notes:

- **Do not use** "Apply to backend" in production (it is localhost-only by design).
- Secrets should be set in Render environment variables.

## 6) Production smoke test

- `/text`: translate a short text
- `/article`: translate a simple public URL
- `/batch`: run with `limit=10` and confirm it processes rows from Neon

If `/batch` returns 503:

- confirm `POSTGRES_DSN`
- confirm `source_texts` exists
- check Render logs
