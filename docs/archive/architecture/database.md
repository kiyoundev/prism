This documents the Supabase database tables that support model training, keyword lookup, and storage of user-submitted data for the rule engine.

*** CONFIG TABLES ***

## brand_seeds

- **slug**: `TEXT` PRIMARY KEY.
- **name**: `TEXT` NOT NULL.
- **category**: `TEXT` NOT NULL CHECK in (`'courier'`, `'government'`, `'finance'`, `'tech'`, `'telecom'`, `'generic'`).
- **aliases**: `TEXT[]` NOT NULL DEFAULT `'{}'`.
- **updated_at**: `TIMESTAMPTZ` NOT NULL DEFAULT `now()`.

## category_keywords

- **category**: `TEXT` PRIMARY KEY CHECK in (`'delivery'`, `'ticket'`, `'banking'`, `'tax'`, `'verification'`).
- **keywords**: `TEXT[]` NOT NULL.
- **updated_at**: `TIMESTAMPTZ` NOT NULL DEFAULT `now()`.

## idf_cues *(optional, for TF-IDF weighting)*

- **cue**: `TEXT` PRIMARY KEY.
- **idf**: `NUMERIC` NOT NULL.
- **built_at**: `TIMESTAMPTZ` NOT NULL DEFAULT `now()`.

*** TRAINING CORPUS (GROUND TRUTH) ***

## corpus_known_scams

- **id**: `UUID` PRIMARY KEY DEFAULT `gen_random_uuid()`.
- **channel**: `TEXT` NOT NULL CHECK in (`'sms'`, `'email'`, `'dm'`).
- **message_raw**: `TEXT` NOT NULL.
- **message_norm**: `TEXT` NOT NULL. // normalized once, deterministic
- **sha256_norm**: `TEXT` UNIQUE NOT NULL. // dedupe key
- **category**: `TEXT` NOT NULL CHECK in (`'delivery'`, `'ticket'`, `'banking'`, `'tax'`, `'verification'`, `'generic'`).
- **topic_key**: `TEXT` NULL. // e.g., `'schedule-delivery'`, `'return-to-sender'`
- **brand_slug**: `TEXT` NULL REFERENCES `brand_seeds(slug)`.
- **signals**: `JSONB` NULL. // `{phraseHits:[], urls:[], urgency:true, …}` for audit
- **created_at**: `TIMESTAMPTZ` NOT NULL DEFAULT `now()`.

Indexes:

- **UNIQUE (sha256_norm)**.
- **INDEX (category, topic_key)**.
- **INDEX (brand_slug)**.

*** RUNTIME RECORDS (FINAL IDs AND EVIDENCE) ***

## known_scams

- **id**: `UUID` PRIMARY KEY DEFAULT `gen_random_uuid()`.
- **dia_id**: `TEXT` UNIQUE NOT NULL. // `sms-<brand|topic>-<hash>`
- **message_raw**: `TEXT` NOT NULL.
- **message_norm**: `TEXT` NOT NULL.
- **category**: `TEXT` NOT NULL CHECK in (`'delivery'`, `'ticket'`, `'banking'`, `'tax'`, `'verification'`, `'generic'`).
- **topic_key**: `TEXT` NOT NULL. // e.g., `'schedule-delivery'`, `'return-to-sender'`
- **brand_slug**: `TEXT` NULL REFERENCES `brand_seeds(slug)`.
- **confidence**: `NUMERIC` NOT NULL. // `0..1`
- **signals**: `JSONB` NOT NULL. 
// `{ phraseHits: string[], tfidfScore?: number, classifierProb?: number, brandMatchPath: 'contains' | 'fuzzy' | 'ed1' | null, urlRisk?: { riskyTLD: bool, shortLink: bool, domains: string[] }, links?: [{ display, href, kind }], mediaTypes?: string[] }`
- **created_at**: `TIMESTAMPTZ` NOT NULL DEFAULT `now()`.

Indexes:

- **UNIQUE (dia_id)**.
- **INDEX (category, topic_key)**.
- **INDEX (brand_slug)**.
- **INDEX (created_at)**.

*** OPTIONAL OPERATIONAL TABLES ***

## topic_models *(optional, if you persist classifier configs)*

- **model_id**: `TEXT` PRIMARY KEY.
- **kind**: `TEXT` NOT NULL CHECK in (`'naive_bayes'`, `'logreg'`).
- **config**: `JSONB` NOT NULL. // tokenizer/normalization, features
- **metrics**: `JSONB` NULL. // validation scores
- **created_at**: `TIMESTAMPTZ` NOT NULL DEFAULT `now()`.

## links *(optional normalization of URLs)*

- **id**: `UUID` PRIMARY KEY DEFAULT `gen_random_uuid()`.
- **known_scams_id**: `UUID` NOT NULL REFERENCES `known_scams(id)` ON DELETE CASCADE.
- **display**: `TEXT` NOT NULL.
- **href**: `TEXT` NOT NULL.

*** WHY THIS SPLIT WORKS ***

- **Config tables** (`brand_seeds`, `category_keywords`, `idf_cues`) stay small, versionable, and hydrate runtime logic.
- **Training corpus** (`corpus_known_scams`) stores immutable, labeled samples for TF-IDF and classifiers, enabling reweighting without touching production identifiers.
- **Runtime records** (`known_scams`) append final decisions with `dia_id`, labels, and evidence for deterministic audit trails.

*** DETERMINISM AND CONSTRAINTS ***

- **Stable IDs**: Compute `dia_id` variants from `message_norm` using a short SHA-256 so dedupe is trivial.
- **Normalization discipline**: Keep stemming/lemmatization inside training; never alter `message_norm` used for hashing or display.
- **Strict constraints**: Enforce CHECKs and foreign keys to prevent data drift across enumerated values and brand references.
