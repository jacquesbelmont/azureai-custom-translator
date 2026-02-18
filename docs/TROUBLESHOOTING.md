# Troubleshooting

## Backend fails on startup with PostgreSQL connection refused

If you see:

- `psycopg.OperationalError: connection ... port 5432 ... Connection refused`

Fix:

- Start PostgreSQL:

```bash
docker compose up -d
```

Notes:

- The backend can run without PostgreSQL for `/translate/text` and `/translate/url`.
- `/translate/db` requires PostgreSQL.

## `/translate/db` returns 503

This indicates PostgreSQL is not reachable using the current DSN.

- Start Postgres via Docker Compose
- Or update the DSN in Settings (or `POSTGRES_DSN` in `backend/.env`)

## Frontend shows 404 `/lib/config.ts`

This can happen if an old tab is still running an older build.

Fix:

- Hard refresh the browser tab (Cmd+Shift+R)
- Close old tabs and restart `npm run dev`

## Azure Translator returns 401/403

- Check `AZURE_TRANSLATOR_KEY`
- Check `AZURE_TRANSLATOR_REGION`
- Confirm the resource is a Translator resource (not a different Cognitive Service)

## Azure Translator returns 429

- Rate limit / quota reached. Wait and retry or increase quota.

## OpenAI post-edit not applied

- Ensure `OPENAI_API_KEY` is configured
- Ensure **AI Post-Edit** is enabled in the UI

## Article translation fails

Common causes:

- The URL blocks bots / requires JS rendering
- The HTML is not readable by the extractor

Try:

- A different URL
- Translating plain text instead
