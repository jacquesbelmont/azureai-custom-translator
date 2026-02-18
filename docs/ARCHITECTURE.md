# Architecture

This project is a local-first demo of Azure AI Translator with optional OpenAI post-editing and PostgreSQL-backed caching/batch jobs.

## High-level components

- **Frontend (Astro + TypeScript)**
  - Pages: `/text`, `/article`, `/batch`, `/settings`
  - Stores configuration in browser `localStorage`
  - Can apply runtime config to the backend via `POST /config` (**localhost only**)

- **Backend (FastAPI)**
  - Endpoints:
    - `GET /health`
    - `GET /config` / `POST /config`
    - `POST /translate/text`
    - `POST /translate/url`
    - `POST /translate/db`
  - Translation pipeline:
    - Azure Translator (supports `category`)
    - Optional OpenAI post-editing
    - Optional PostgreSQL cache

- **PostgreSQL (Docker Compose)**
  - Used for:
    - translation cache (`translation_cache`)
    - batch jobs source/target tables (`source_texts` -> `translated_texts`)

## Dataflow diagram

```mermaid
flowchart LR
  U[User] --> F[Frontend\nAstro + TS]

  F -->|POST /translate/text| API[FastAPI Backend]
  F -->|POST /translate/url| API
  F -->|POST /translate/db| API
  F -->|POST /config (localhost only)| API

  API --> P1[Pipeline\nresolve languages/category\ncache key]

  P1 -->|cache_get (optional)| DB[(PostgreSQL)]
  DB -->|cache hit| API

  P1 -->|cache miss| AZ[Azure AI Translator\n/translate + category]
  AZ --> P2[translated text/markdown]

  P2 -->|if enabled + key present| OAI[OpenAI Post-Edit\nResponses API]
  OAI --> P3[post-edited result]

  P3 -->|cache_put (optional)| DB

  API --> F
```

## Request-level flows

## 1) Text translation (`POST /translate/text`)

- Input: text + `source_language` + `target_language` + optional `category`
- Backend:
  - Computes cache key (text + langs + category)
  - Checks PostgreSQL cache (if available)
  - If miss:
    - Calls Azure Translator
    - Optionally calls OpenAI to post-edit
    - Saves result to cache (if available)

## 2) Article translation (`POST /translate/url`)

- Input: URL + langs + optional category
- Backend:
  - Fetches HTML
  - Extracts main content
  - Converts to Markdown
  - Translates Markdown using Azure
  - Optionally post-edits Markdown via OpenAI
  - Caches by Markdown content

## 3) Batch translation (`POST /translate/db`)

- Requires PostgreSQL.
- Backend:
  - Reads rows from `SOURCE_TABLE`
  - Uses cache to avoid re-translation
  - Writes to `TARGET_TABLE`

## Configuration sources and precedence

The backend resolves settings in this order:

1. **Request payload** (per call)
2. **Runtime overrides** from `POST /config` (localhost only)
3. **Environment variables** (`backend/.env`)

Notes:

- Runtime configuration is intended for local demos only.
- For production, configure via environment variables / secret manager.
