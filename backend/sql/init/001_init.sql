CREATE TABLE IF NOT EXISTS source_texts (
  id TEXT PRIMARY KEY,
  source_text TEXT NOT NULL
);

-- Optional seed data (safe to keep; uses upsert)
INSERT INTO source_texts (id, source_text) VALUES
  ('demo-001', 'Hello! This is a demo row for batch translation.'),
  ('demo-002', 'Azure AI Translator supports custom categories for domain adaptation.'),
  ('demo-003', 'PostgreSQL is used here for caching and batch jobs.')
ON CONFLICT (id) DO UPDATE SET
  source_text = EXCLUDED.source_text;
