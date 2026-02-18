# Usage Guide

## Pages

## 1) Translate Text (`/text`)

- Set **From**, **To**, and optional **Category**
- Toggle **AI Post-Edit** (requires OpenAI key)
- Click **Translate**

What happens:

- Calls `POST /translate/text`
- Uses Azure Translator (and Custom Translator if category is provided)
- Optionally post-edits the output using OpenAI

## 2) Translate Article (`/article`)

- Paste an article URL
- Set **From**, **To**, and optional **Category**
- Click **Process & Translate**

What happens:

- Calls `POST /translate/url`
- Backend fetches the page, extracts main content, converts to Markdown
- Translates the Markdown and optionally post-edits it

## 3) Batch Jobs (`/batch`)

Requires PostgreSQL.

- Choose **limit**, languages, optional category
- Click **Start Batch Job**

What happens:

- Calls `POST /translate/db`
- Backend reads rows from `SOURCE_TABLE` (default: `source_texts`)
- Writes results into `TARGET_TABLE` (default: `translated_texts`)
- Uses PostgreSQL cache table (default: `translation_cache`) to avoid re-translation

## 4) Settings (`/settings`)

- Stores config in `localStorage`
- Can apply runtime config to backend via `POST /config` (localhost-only)

Recommended workflow:

1. Start backend
2. Start frontend
3. Open Settings
4. Set keys/region/DSN
5. Click **Apply to backend**
6. Use Text/Article/Batch pages
