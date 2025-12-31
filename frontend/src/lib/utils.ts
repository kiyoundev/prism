import { type BrandSeed, BRAND_SEEDS, Category, CATEGORY_KEYWORDS } from './brand_seeds';
import unhomoglyph from 'unhomoglyph';
import { search, fuzzy } from 'fast-fuzzy';
import { distance } from 'fastest-levenshtein';
import natural from 'natural';

// import { nGrams } from 'wink-nlp-utils'; // npm i wink-nlp-utils

// Use deterministic edit-distance variants for short tokens; skip stochastic unless testing

// 1. Deterministic edit-distance ≤1 variants
// • For very short brand tokens (length 2–4), generate variants that are one operation away:
// ▫ Substitution: ups → uos, ups → uρs (if not using a confusables map)
// ▫ Deletion: ups → up, us
// ▫ Insertion: ups → upss, uups
// ▫ Transposition: ups → usp
// • Limit to alphabet set a–z and a confusable set; keep the count small to avoid false positives.
// • Use a higher threshold and require co-occurring category cues (e.g., delivery words) before accepting a match.

// 2. Stochastic transforms (mutators)
// • Apply simple random mutations for robustness tests or when you want broader coverage:
// ▫ insertChar(str, idx, ch), deleteChar(str, idx), swapAdjacent(str, idx), replaceChar(str, idx, ch)
// • Use them sparingly and only for specific seeds (UPS, RBC, TD, BMO) where corpus shows lots of obfuscation.

// 3. Homoglyphs/confusable substitutions

// export const extractBrand = (msg: string): string => {
// 	// console.log(BRAND_SEEDS);
// 	// Check against name, and alias using fuzzy match
// 	// COURIER_BRANDS.forEach((brand) => {
// 	// 	msg.includes();
// 	// });
// };

// export function messageNgrams(norm: string, min = 2, max = 5): string[] {
// 	const tokens = norm.split(' ').filter(Boolean);
// 	const grams: string[] = [];
// 	for (let n = min; n <= max; n++) {
// 		grams.push(...nGrams(tokens, n).map((g) => g.join(' ')));
// 	}
// 	return grams;
// }

// export function isEd1NearMatch(messageNorm: string, token: string): boolean {
// 	// Quick containment first
// 	if (messageNorm.includes(token)) return true;

// 	// Only apply ED<=1 checks for very short tokens
// 	if (!SHORT_BRANDS.has(token) || token.length > 4) return false;

// 	// Check token against message n-grams (length 1–2 tokens)
// 	const words = messageNorm.split(' ').filter(Boolean);
// 	for (const w of words) {
// 		if (Math.abs(w.length - token.length) > 1) continue; // small pruning
// 		if (lev(w, token) <= 1) return true;
// 	}
// 	// Also check 2-token grams collapsed (e.g., "my ups" -> "myups")
// 	for (let i = 0; i < words.length - 1; i++) {
// 		const w2 = words[i] + words[i + 1];
// 		if (lev(w2, token) <= 1) return true;
// 	}
// 	return false;
// }

const MIN_VARIANT_CHAR_LENGTH = 3;
const NGrams = natural.NGrams;
const tokenizer = new natural.AggressiveTokenizer();

let classifier: natural.BayesClassifier | null = null;

export const getClassifier = () => {
	if (!classifier) {
		const clf = new natural.BayesClassifier();
		for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
			keywords.forEach((keyword) => clf.addDocument(keyword, category));
		}
		clf.train();
		classifier = clf;
	}
	return classifier;
};

// export const predictCategory = (clf: natural.BayesClassifier, msg: string) => {
// 	// const norm = normalize(msg);
// 	const stems = msg.split(' ').map((t) => natural.PorterStemmer.stem(t));
// 	const label = clf.classify(stems);
// 	const probs = clf.getClassifications(stems); // [{label, value}]
// 	const prob = probs.find((p) => p.label === label)?.value ?? 0;
// 	return { label, prob };
// };

export const mapTokens = (tokens: string[]) => {
	const tokensMap = new Map<number, Set<string>>();
	for (const token of tokens) {
		const len = token.split(' ').filter(Boolean).length;
		if (!tokensMap.has(len)) tokensMap.set(len, new Set());
		tokensMap.get(len)!.add(token);
	}
	return tokensMap;
};

// lowercase → unhomoglyph → strip accents → remove punctuation → collapse spaces.
export function normalize(input: string): string {
	const base = unhomoglyph(input.toLowerCase());
	const deaccent = base
		.normalize('NFKD') // remove diacritics
		.replace(/[\u0300-\u036f]/g, ''); // strip accents
	return deaccent
		.replace(/\u00a0/g, ' ') // NBSP
		.replace(/[^a-z0-9 ]+/g, ' ') // punctuation
		.replace(/\s+/g, ' ') // collapse whitespace
		.trim();
}

/**
 * Build small deterministic variants from a brand's name + aliases,
 * after normalization: phrase, space-collapsed, hyphenated, two-word swap.
 */
export function deriveVariants(tokens: string[]): string[] {
	const out = new Set<string>();
	for (const token of tokens) {
		// out.add(token); // normalized phrase
		out.add(token.replace(/ /g, '')); // space-collapsed
		out.add(token.replace(/ /g, '-')); // hyphenated
		const parts = token.split(' ');
		if (parts.length === 2) out.add(`${parts[1]} ${parts[0]}`); // two-word swap
	}
	// console.log(out);
	return [...out].filter((v) => v.length >= MIN_VARIANT_CHAR_LENGTH);
}

export const deriveCategoryVariants = (seed: string[]): string[] => {
	const bases = seed.map(normalize);
	const out = new Set<string>();
	for (const base of bases) {
		out.add(base);
		out.add(base.replace(/ /g, ''));
		out.add(base.replace(/ /g, '-'));
		out.add(base.replace(/-/g, ' '));
	}
	return [...out].filter((v) => v.length >= MIN_VARIANT_CHAR_LENGTH);
};

export const ed1MatchCheck = (tokens: string[], target: string): boolean => {
	for (let i = 0; i < tokens.length; i++) {
		const token = tokens[i];
		if (Math.abs(token.length - target.length) > 1) continue;
		if (distance(token, target) <= 1) return true;
		if (i < tokens.length - 1) {
			const pair = token + tokens[i + 1];
			if (Math.abs(pair.length - target.length) <= 1 && distance(pair, target) <= 1) return true;
		}
	}
	return false;
};

/* 
Normalize text, detect multi-word cues with n‑grams, confirm with a classifier, then pick the category

Here’s the extraction flow focused only on category/topic:
 • Normalize the message so matching is consistent across casing, accents, punctuation, and homoglyphs.
 • Tokenize and build 2–5 word n-grams, then check them against your high-signal category phrases first; tally single-keyword hits only if no phrase matched.
 • Construct classifier features separately: use normalized tokens, optional stemming, and simple flags (e.g., presence of “return to sender,” “verification code,” “notice of assessment”).
 • Run a lightweight topic classifier to get a label with probability; treat it as a probabilistic vote.
 • Reconcile: if the classifier’s probability is high and it agrees with n-gram phrase hits, lock that category; if they disagree or confidence is low, prefer the n-gram result for precision.
 • Return the final category plus the phrase hits you used as evidence; use this category later to gate ED≤1 for short brand slugs and to build the ID’s topic.

 	//   1. normalize
	//   2. tokenize
	//   3. stem/lemmatize
	//   4. build features (bag‑of‑words, n‑grams, phrase flags)
	//   5. topic prediction.

	// 	1. Normalize input text (lowercase, collapse whitespace, optional stemming).
	//  2. Match multi-word phrases first, then single keywords per category.
	//  3. Tally matches per category and pick the best; support thresholds and ties.
	//  4. Return both the chosen category and match evidence for debugging.
	//  5. Provide a drop-in function you can call anywhere.
 */

export const extractCategory = (msg: string, threshold: number = 0.009) => {
	const msg_norm = normalize(msg);
	const tokens_msg = tokenizer.tokenize(msg_norm);

	console.log(CATEGORY_KEYWORDS);

	for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
		const tokens_keywords = keywords.map(normalize);
		const tokens_keywords_map = mapTokens(tokens_keywords);
		let tally: { cat: Category; score: number; hits: string[] }[] = [];

		console.log(tokens_keywords_map);

		// n-gram + phrase-first scoring
		for (const [size, tokens] of tokens_keywords_map.entries()) {
			const ngrams = NGrams.ngrams(tokens_msg, size).map((t) => t.join(' '));

			// for (const window of windows) {
			// 	// if (tokens.has(window)) return category;
			// }
		}
	}

	/*
		const norm = normalize(msg);
		const grams = new Set(makeNgrams(norm, 2, 5));
		let tally: { cat: Category; score: number; hits: string[] }[] = [];

		// n-gram + phrase-first scoring
		for (const [cat, cues] of Object.entries(CATEGORY_KEYWORDS) as [Category, string[]][]) {
			let score = 0; const hits: string[] = [];
			for (const cue of cues) {
			const q = cue.toLowerCase();
			const isPhrase = q.includes(' ');
			const hit = isPhrase ? grams.has(q) || norm.includes(q) : norm.includes(q);
			if (hit) { score += isPhrase ? 1.0 : 0.6; hits.push(cue); }
			}
			tally.push({ cat, score, hits });
		}
		tally.sort((a, b) => b.score - a.score || b.hits.length - a.hits.length);
		const phrasePick = tally[0] ?? { cat: 'generic', score: 0, hits: [] };
	*/

	// const classifier = getClassifier();
	// const label_predicted = classifier.classify(msg);
	// const predictedScore = classifier.getClassifications(msg).find((s) => s.label === label_predicted);
};

export const extractBrand = (msg: string, seeds: BrandSeed[], threshold: number = 0.9) => {
	const msg_norm = normalize(msg);
	const tokens_msg = tokenizer.tokenize(msg_norm);

	for (const seed of seeds) {
		// console.log(tokens_seed); // name & aliases
		// console.log(deriveVariants(seed)); // variants derived from name & aliases
		// console.log(tokens_map);

		// 1. search with brand.name or alias: phrase-first containment
		// const tokens_seed = [seed.name, ...(seed.aliases ?? [])].map(normalize);
		// const tokens_seed_map = mapTokens(tokens_seed);
		// for (const [size, tokens] of tokens_seed_map.entries()) {
		// 	const windows = NGrams.ngrams(tokens_msg, size).map((t) => t.join(' '));
		// 	for (const window of windows) {
		// 		if (tokens.has(window)) return seed.slug;
		// 	}\
		// }

		// // 2. search with variant alias: Variant containment
		// const tokens_variants = deriveVariants(tokens_seed);
		// const tokens_variants_map = mapTokens(tokens_variants);
		// for (const [size, tokens] of tokens_variants_map.entries()) {
		// 	const windows = NGrams.ngrams(tokens_msg, size).map((t) => t.join(' '));
		// 	for (const window of windows) {
		// 		if (tokens.has(window)) return seed.slug;
		// 	}
		// }

		// // 3. fuzzy match variant alias
		// const tokens_fuzzy_map = mapTokens([...tokens_seed, ...tokens_variants]);

		// for (const [size, tokens] of tokens_fuzzy_map.entries()) {
		// 	const windows = NGrams.ngrams(tokens_msg, size).map((t) => t.join(' '));
		// 	for (const window of windows) {
		// 		const matches = search(window, [...tokens], { threshold });
		// 		if (matches.length > 0) return seed.slug;
		// 	}
		// }

		extractCategory(msg_norm);

		// 4. ED≤1 for short slugs
		// if (seed.slug.length <= 3) {
		// 	// const hasCategoryCue = CATEGORY_KEYWORDS[seed.category].some((cue) => msg_norm.includes(cue));
		// 	const tokens = msg_norm.split(' ').filter(Boolean);
		// 	const slug_norm = normalize(seed.slug);
		// 	if (ed1MatchCheck(tokens, slug_norm)) return seed.slug;
		// }

		// 5. Fallback to generic brand
	}

	return null;
};

// const addVariant = (variants: Set<string>, candidate: string) => {
// 	if (candidate.length >= MIN_VARIANT_LENGTH) {
// 		variants.add(candidate);
// 	}
// };

// export function deriveAliasVariants(alias: string): string[] {
// 	const normalized = normalize(alias);
// 	if (!normalized) return [];

// 	const tokens = normalized.split(' ').filter(Boolean);
// 	const variants = new Set<string>();

// 	addVariant(variants, normalized);
// 	if (tokens.length > 1) {
// 		addVariant(variants, tokens.join(''));
// 		addVariant(variants, tokens.join('-'));
// 		if (tokens.length === 2) {
// 			addVariant(variants, `${tokens[1]} ${tokens[0]}`);
// 		}
// 	}

// 	// Collapsed form for single-token aliases is redundant with normalized result.
// 	// Ensure multi-word aliases always include compact variant even if duplicates are filtered out.

// 	return Array.from(variants);
// }

// export function buildAliasVariantIndex(seeds: BrandSeed[]): Record<string, string[]> {
// 	return seeds.reduce<Record<string, string[]>>((acc, seed) => {
// 		const sourcePhrases = new Set<string>();
// 		sourcePhrases.add(seed.name);
// 		seed.aliases?.forEach((alias) => sourcePhrases.add(alias));

// 		const variants = new Set<string>();
// 		sourcePhrases.forEach((phrase) => {
// 			for (const variant of deriveAliasVariants(phrase)) {
// 				variants.add(variant);
// 			}
// 		});

// 		acc[seed.slug] = Array.from(variants);
// 		return acc;
// 	}, {});
// }
