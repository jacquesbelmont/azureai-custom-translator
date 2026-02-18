export type AppConfig = {
  apiBaseUrl: string;
  defaultFrom: string;
  defaultTo: string;
  defaultCategory: string;
  enablePostEdit: boolean;

  azureEndpoint: string;
  azureKey: string;
  azureRegion: string;

  openaiApiKey: string;
  openaiModel: string;

  postgresDsn: string;
  sourceTable: string;
  sourceIdColumn: string;
  sourceTextColumn: string;
  targetTable: string;
  targetIdColumn: string;
  targetTextColumn: string;
  cacheTable: string;
};

const STORAGE_KEY = 'polyglot_ai_config_v1';

export const defaultConfig: AppConfig = {
  apiBaseUrl: 'http://localhost:8000',
  defaultFrom: 'en',
  defaultTo: 'pt-br',
  defaultCategory: '',
  enablePostEdit: true,

  azureEndpoint: 'https://api.cognitive.microsofttranslator.com',
  azureKey: '',
  azureRegion: '',

  openaiApiKey: '',
  openaiModel: 'gpt-4o-mini',

  postgresDsn: 'postgresql://postgres:postgres@localhost:5432/postgres',
  sourceTable: 'source_texts',
  sourceIdColumn: 'id',
  sourceTextColumn: 'source_text',
  targetTable: 'translated_texts',
  targetIdColumn: 'id',
  targetTextColumn: 'translated_text',
  cacheTable: 'translation_cache'
};

export function loadConfig(): AppConfig {
  if (typeof window === 'undefined') return defaultConfig;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultConfig;
    const parsed = JSON.parse(raw);
    return { ...defaultConfig, ...parsed } as AppConfig;
  } catch {
    return defaultConfig;
  }
}

export function saveConfig(cfg: AppConfig): void {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(cfg));
}

export async function applyBackendConfig(cfg: AppConfig): Promise<any> {
  const payload = {
    translation_from: cfg.defaultFrom,
    translation_to: cfg.defaultTo,
    azure_translator_category: cfg.defaultCategory || undefined,

    azure_translator_endpoint: cfg.azureEndpoint,
    azure_translator_key: cfg.azureKey || undefined,
    azure_translator_region: cfg.azureRegion || undefined,

    openai_api_key: cfg.openaiApiKey || undefined,
    openai_model: cfg.openaiModel || undefined,

    postgres_dsn: cfg.postgresDsn,
    source_table: cfg.sourceTable,
    source_id_column: cfg.sourceIdColumn,
    source_text_column: cfg.sourceTextColumn,
    target_table: cfg.targetTable,
    target_id_column: cfg.targetIdColumn,
    target_text_column: cfg.targetTextColumn,
    cache_table: cfg.cacheTable
  };

  const resp = await fetch(`${cfg.apiBaseUrl}/config`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const data = await resp.json();
  if (!resp.ok) {
    throw new Error(data?.detail ? String(data.detail) : `Config failed (${resp.status})`);
  }
  return data;
}
