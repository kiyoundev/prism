<!-- 
 • Topic detection: Train a lightweight classifier on labeled scam snippets for your categories (delivery, ticket, banking, tax, verification, generic). Feed it normalized tokens and high‑signal phrases. Use its prediction as an extra vote alongside your n‑gram matches; when both agree, promote confidence and lock the category.

 • Sentiment analysis: Treat sentiment as a secondary signal. Many scam texts are urgent/negative (“final notice,” “penalty,” “suspend”). If sentiment is strongly negative/urgent, modestly boost confidence; if neutral (e.g., plain tracking updates), don’t over‑weight it. Never let sentiment alone decide category or “known scam.”

 • Tokenization: Use a robust tokenizer (winkNLP) to produce clean word tokens before classification. This stabilizes features for topic detection and improves your ED≤1 short‑slug check.
 
 • Stemming/normalization: Apply stemming or lemmatization to reduce variants (“refunds” → “refund”). Since you already normalize, add stemming only to the classifier’s feature pipeline, not to your ID text hashing.
 -->

# Rule Engine Implementation & Pipeline Details

## 1. Inputs, Sources, and Policies
- **Seeds** `src/lib/brand_seeds.ts`
  - **Minimum payload** `slug`, `name`, `aliases` (canonical phrases only – no typos or homoglyphs).
  - **Runtime-only variants** Generate alias permutations in-memory; never persist to Supabase.
- **Rule catalog** `data/rules/known-scams.md`
  - Authored in Markdown, published through the pipeline described in `docs/architecture/rule-engine.md`.
- **Message normalization**
  - Apply `normalize()` from `src/lib/utils.ts` to both inbound messages and seed phrases.
  - Pipeline: lowercase → unhomoglyph (comparison only) → NFKD + strip diacritics → collapse whitespace → remove punctuation → normalize NBSP.
- **Threshold policy**
  - Brand inclusion score must be ≥ `0.9` to appear in the deterministic ID.
  - Short slugs (`ups`, `rbc`, `td`, `bmo`) require category corroboration even after ED≤1 boost.

## 2. Canonical Alias Variant Generation for Brands(Runtime, `deriveBrandAliasVariants`)
- **Variant derivation** (for every normalized alias):3
  - Exact phrase: `"canada post"`.
  - Space-collapsed: `"canadapost"`.
  - Hyphenated: `"canada-post"`.
  - Two-word swap (only when alias has exactly two tokens): `"post canada"`.
  - Filter out variants shorter than three characters.
- **Implementation notes**
  - Encapsulate logic with `deriveBrandAliasVariants()` in `src/lib/utils.ts`.
  - Cache per request to avoid recomputation during multi-step evaluations.

## 3. Brand Matching Pipeline (`extractBrand()`)
- **Phrase-first containment**
  - If any variant is contained in the normalized message, set brand score to `1.0` (highest confidence).
- **Fuzzy fallback**
  - When no containment hits, compute similarity per variant using `fast-fuzzy` or `rapidfuzz-js`; compare phrases, not the entire message blob.
- **Deterministic ED≤1 boost**
  - Only for allowlisted short slugs.
  - Compare slug against single tokens and adjacent token pairs (`"my ups"` → `"myups"`).
  - If distance ≤ `1`, raise score near threshold (suggested `0.92`) but still require category cues.
- **Scoring outcome**
  - Track `(brandSlug, score, signals)` for downstream ID decision and telemetry.

## 4. Category & Topic Extraction Pipeline (`extractCategory()`)

<!-- 
Classifier pipeline: 
  1. normalize 
  2. tokenize
  3. stem/lemmatize
  4. build features (bag‑of‑words, n‑grams, phrase flags)
  5. topic prediction. 
Here stemming helps collapse forms like “refunds/refunded” to “refund” so the model generalizes.

 • Feature pipeline: normalize → tokenize → optional stemming → build features from high‑signal phrases (return to sender, schedule delivery, verification code), plus token n‑grams. This is only for the classifier; do not use stems for the ID text.
 • Train a lightweight topic classifier on your categories: delivery, ticket, banking, tax, verification, generic. Use “natural” (Naive Bayes) for simplicity.
 • At runtime: get the classifier’s predicted topic and probability. If probability is high (e.g., ≥ 0.8) and your n‑gram detector finds matching phrases for the same category, lock that topic for the ID.
 • If the classifier is uncertain or disagrees with n‑grams, prefer the n‑gram result. This keeps precision on phrase-heavy scams.
 • Sentiment: use as a minor confidence booster only; never as the topic decider.

Natural's clasification tokenizes and stems words by default


Classification stage
 1. Normalize input text (lowercase, collapse whitespace, optional stemming).
 2. Match multi-word phrases first, then single keywords per category.
 3. Tally matches per category and pick the best; support thresholds and ties.
 4. Return both the chosen category and match evidence for debugging.
 5. Provide a drop-in function you can call anywhere.

 -->

 • Category:
  ▫ Run n-gram phrase detection; if a single category has strong phrase hits, pick it (true/false sufficient).
  ▫ If multiple categories hit or only singles matched, use a simple weighted score to pick the best.
  ▫ Optionally confirm with classifier probability; if both agree, lock the category.

 • Add TF‑IDF style weighting: down‑weight very common words (“update,” “account”) and up‑weight rarer cues.
 • Introduce thresholds: if a category has ≥2 phrase hits, pick it outright; otherwise fall back to weighted scoring.

- *** TF-IDF Scoring System ***
 • Primary weighting: score each category as the sum of TF × IDF over its detected cues in the message.
 • Phrase bonus (optional): add a small fixed bonus for multi‑word cues to favor collocations; or rely solely on TF‑IDF if your corpus already down‑weights common single tokens.
 • Tie‑breaks: if two categories are close, prefer the one with a decisive multi‑word phrase hit; otherwise fall back to n‑gram phrase presence.
 • Thresholds: if all category scores are near zero, return generic.
 • Classifier cross‑check (optional): if you use a topic classifier, accept its label when probability is high and it agrees; otherwise keep the TF‑IDF pick.





- **N-gram construction**
  - Build 2–5 word n-grams via `natural` to capture collocations.
- **Cue matching**
  - Compare against `CATEGORY_KEYWORDS` (delivery, ticket, banking, tax, verification, generic).
  - Weight multi-word cues (e.g., `"return to sender"`, `"notice of assessment"`) higher than single tokens.
- **Collision resolution**
  - Delivery wins if phrases like `"return to sender"` or `"reschedule"` appear.
  - Verification wins when `"otp"`, `"2fa"`, `"verification code"` surface strongly.
  - Extend precedence table as categories evolve.

## 5. Deterministic ID Construction (`buildDiaId()` TBD)
- **Variant selection**
  - Pick the highest-scoring brand; include in ID only if score ≥ `0.9`.
  - Otherwise produce a category-only ID and log brand candidates to metadata.
- **Hashing**
  - Compute short hash from normalized message (e.g., `sha256` → first eight chars) for uniqueness.
- **Formats**
  - Brand confident: ``sms-{brandSlug}-{topicKey}-{hash}`` → `sms-ups-schedule-delivery-<hash>`.
  - Brand uncertain: ``sms-{topicKey}-{hash}``.
- **Metadata**
  - Store candidate brands, scores, and cue hits for later review/analytics.

## 6. Persistence Contract
- **Primary table** `public.known_scams`
  - Columns: `message_raw`, `message_norm`, `dia_id`, `category`, `topic_key`, optional `brand_slug`, `confidence`, `signals` JSONB.
- **Publishing pipeline**
  - Markdown rules → JSON normalization → Supabase upsert (see `docs/architecture/rule-engine.md`).
  - Runtime cache hydrates from Supabase; variants generated on the fly.
- **Telemetry**
  - Instrument counts of variant hits, fuzzy fallbacks, and ED≤1 boosts to gauge seed quality.

## 7. Future Enhancements & Open Questions
- **Classifier integration**
  - Lightweight topic classifier (`natural` tokenizer family) can augment category confidence; use as secondary vote only.
- **Sentiment/urgency signal**
  - Negative/urgent tone can raise suspicion score but must not solely determine category.
- **ID evolution**
  - Monitor hash collisions; adjust length if collision rate exceeds 1e-5.
- **Quality gates**
  - Consider storing last-seen timestamps and human reviewer notes in Supabase to close the loop on false positives.


