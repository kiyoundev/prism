## Phase 0 — Preprocessing & Extraction

Phase 0 runs before any scoring. It normalizes the raw SMS, extracts structured artifacts, and classifies the message — all outputs are bundled into `artifacts{}` and passed downstream to Phase 1, Phase 2, and Phase 3.

### Steps

1. **URL Extraction** — pull all URLs from raw text before normalization, preserving the original form for display and heuristics
2. **Normalization**
   - Lowercase conversion
   - Punctuation stripping
   - Unicode NFKD normalization (`unicodedata`) — accented characters reduced to base form (e.g., "é" → "e")
   - Homoglyph flattening (`unidecode`) — Cyrillic/mathematical substitutes reduced to ASCII equivalents
   - Zero-width character removal (`​`, `‌`, etc.) — used by scammers to break keyword matching
3. **Tokenization, N-grams & Fuzzy Matching**
   - Split normalized text into word tokens
   - Generate bi-gram and tri-gram sequences for phrase detection
   - Apply fuzzy matching (edit-distance via `rapidfuzz`) to catch near-miss brand names and keyword variants that exact matching would miss (e.g., "Cañada Post" → "Canada Post")
4. **Brand & Category Extraction** — see [Category Extraction Strategy](#category-extraction-strategy) below

---

## Category Extraction Strategy

The engine determines the intent/category of a message (e.g., Delivery, Banking, Tax) to enable context-aware rule scoring. This allows detection of contradictions (e.g., a "Delivery" message using a "Streaming" brand link).

1.  **Brand-Based Classification (Primary)**
    *   **Source:** `backend/app/core/rules/config/brand_variants.json`
    *   **Logic:** Match normalized tokens against known brand slugs and aliases.
    *   **Example:** If "Canada Post" or "Poste Canada" is found, the category is definitively resolved to `delivery`.
    *   **Behavior:** Brand matches take precedence over generic keywords because they imply a specific expected context (e.g., valid domains for that brand).

2.  **Keyword-Based Classification (Fallback)**
    *   **Source:** `backend/app/core/rules/config/category_keywords.json`
    *   **Logic:** If no specific brand is detected, the engine counts hits for category-specific phrases (n-grams).
    *   **Example:** Phrases like "return to sender", "missed package", or "tracking number" suggest `delivery` even without a brand name.
    *   **Behavior:** The category with the highest keyword density wins, provided it meets a minimum confidence threshold.

3.  **Default State**
    *   **Result:** `unknown`
    *   **Logic:** If neither brands nor sufficient keywords are matched, the category is set to `unknown`. This prevents applying category-specific strict rules (like "Banking URL Allowlist") to generic messages.

### Detailed Implementation Steps

1.  **Preprocessing (The "Clean" Phase)**
    *   **Normalization:** Convert text to lowercase. Apply `unicodedata.normalize('NFKD', text)` to handle accented chars (e.g., "é" -> "e").
    *   **Obfuscation Removal:** Strip zero-width characters (e.g., `\u200b`) which scammers use to break keyword matching.
    *   **Tokenization:** Split text into word tokens. Generate bi-gram and tri-gram sequences for phrase matching. Apply fuzzy matching (edit-distance) to catch near-miss brand names and keyword variants that exact matching would miss.

2.  **Brand Extraction (Exact/Phrase Match)**
    *   **Input:** Normalized tokens (Non-lemmatized).
    *   **Why:** Brands are proper nouns ("Rogers", "Tim Hortons"). Lemmatizing them (e.g., "Rogers" -> "Roger") can cause false positives.
    *   **Algorithm:**
        *   Iterate through `brand_variants.json`.
        *   Check if any brand alias (multi-word phrase or single token) exists in the message.
        *   **Priority:** Longest match wins (e.g., "Canada Post" > "Canada").
    *   **Output:** If match found, return `category` immediately (e.g., `delivery`).

3.  **Keyword Scoring (Lemma Match)**
    *   **Input:** Lemmatized tokens (e.g., "delivered" -> "delivery").
    *   **Why:** Captures variations like "shipping", "shipped", "ships" under a single root.
    *   **Algorithm:**
        *   Load `category_keywords.json`.
        *   For each category, count how many keywords appear in the lemmatized tokens.
        *   Apply weights (rare words = higher score, common words = lower).
    *   **Output:** Calculate a score per category.

5.  **Resolution**
    *   If **URL Brand** detected: Use URL's category (Confidence: 1.0).
    *   Else if **Text Brand** detected: Use Brand's category (Confidence: 0.9).
    *   Else if **Top Keyword Score** > Threshold (e.g., 2 hits): Use Top Category (Confidence: 0.8).
    *   Else: Return `unknown` (Confidence: 0.0).

## URL Checker

1. **Normalize and parse.** Lowercase the URL, strip surrounding punctuation, decode punycode/percent-encoding, and run it through a robust parser (e.g., `urllib.parse`). This ensures downstream checks operate on the true hostname/path rather than the user-facing representation.
2. **Extract the registered domain.** Use a public-suffix list helper (`tldextract`) to derive the effective second-level domain. This distinguishes legitimate subdomains (`tracking.purolator.com`) from lookalike hostnames (`purolator.com-secure.vip`).
3. **Allowlist / denylist checks.** Compare the registered domain against brand-specific allowlists (canonical domains for Purolator, CRA, banks) and global denylists of known bad hosts, URL shorteners, or previously-seen typosquats. Allowlist hits can immediately boost confidence; deny hits add strong risk.
4. **Heuristic scoring.** When a domain misses both lists, apply fast heuristics: homoglyph/punycode detection, suspicious or free-hosting TLDs, over-hyphenated brand keywords, entropy of the hostname, or WHOIS-age (flag domains registered within the last N days).
5. **Network and reputation lookups (optional).** Resolve DNS to capture IP/ASN/country mismatches and query reputation services (Google Safe Browsing, PhishTank, VirusTotal) when latency budgets allow. Cache these results to avoid repeated external calls.
6. **Emit rule signals.** Convert the outcomes (allowlist match, deny hit, heuristic score, reputation verdict) into structured signals that feed the rule engine. Each signal can contribute weighted points plus human-readable explanations for the final report.
