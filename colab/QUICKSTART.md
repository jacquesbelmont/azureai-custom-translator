# Google Colab Quickstart

This repository is Colab-friendly. The backend is a normal FastAPI app, and you can run it inside Colab or call the core translation functions directly.

## Option A: Call the translation pipeline directly (recommended for Colab)

1. Upload this repo (or just the `backend/` folder) to Colab.
2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Create `backend/.env` from the example:

```bash
cp backend/.env.example backend/.env
```

4. Fill:

- `AZURE_TRANSLATOR_KEY`
- `AZURE_TRANSLATOR_REGION`
- (optional) `AZURE_TRANSLATOR_CATEGORY`
- (optional) `OPENAI_API_KEY`

5. Run the demo script:

```bash
python backend/colab_demo.py
```

## Option B: Run FastAPI in Colab

You can run Uvicorn, but exposing it publicly requires a tunneling tool (ngrok/cloudflared). This repo does not ship a tunneling dependency by default.

Local run (still useful in Colab just to validate startup):

```bash
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Notes

- The `/translate/db` endpoint requires a reachable PostgreSQL server. In Colab, that typically means using an external hosted Postgres (Render/Neon/Supabase/etc.).
