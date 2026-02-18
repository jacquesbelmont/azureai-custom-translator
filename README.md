# Azure AI Custom Translator Platform

A fast, practical coding-challenge project that provides a production-minded translation API.

It supports:

- **Azure AI Translator** for translation
- Optional **Custom Translator** via the `category` parameter
- Translating **plain text**, **URLs (article -> Markdown)**, and **PostgreSQL rows**
- **PostgreSQL-backed cache** to avoid duplicate Azure calls
- Optional **OpenAI post-edit** step to refine style and Markdown formatting
- A simple **Astro + TypeScript** UI that consumes the API

## Repo Layout

- `backend/`: FastAPI service
- `frontend/`: Astro UI

## 1) Azure Setup (Translator)

You said you have not configured Azure yet.

1. Create an Azure account (free tier if available in your region)
2. In Azure Portal, create a **Translator** resource
3. Open the resource -> **Keys and Endpoint**
4. Copy:
   - `AZURE_TRANSLATOR_KEY`
   - `AZURE_TRANSLATOR_REGION`
5. Use endpoint:
   - `https://api.cognitive.microsofttranslator.com`

### Custom Translator (Category) (Optional)

1. Open **Custom Translator** in Azure
2. Create a workspace linked to your Translator resource
3. Create a project (source/target languages)
4. Upload training documents (parallel corpus + glossary)
5. Train + publish
6. Copy the **Translator API Category ID** and set `AZURE_TRANSLATOR_CATEGORY`

## 2) OpenAI Setup (Optional)

If you want post-editing:

- Set `OPENAI_API_KEY`
- Set `OPENAI_MODEL` (default: `gpt-4o-mini`)

If OpenAI is not configured, the API still works (Azure-only).

## 3) Configure Backend

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`.

## 4) Run Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:

- Swagger: `http://localhost:8000/docs`

## 5) Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

- `http://localhost:4321`

## API

- `GET /health`
- `POST /translate/text`
- `POST /translate/url`
- `POST /translate/db`
