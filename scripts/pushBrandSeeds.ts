// import 'dotenv/config';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';
import { BRAND_SEEDS, type BrandSeed } from '../src/lib/brand_seeds';

dotenv.config({ path: '.env.local' });

const SUPABASE_URL = process.env.SUPABASE_URL!;
const SUPABASE_SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY!;

if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY) {
	throw new Error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in environment.');
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, {
	auth: { persistSession: false, autoRefreshToken: false }
});

/**
 * Minimal validation to catch obvious issues before hitting the DB.
 */
export const validateSeed = (seed: BrandSeed): void => {
	if (!seed.slug || !/^[a-z0-9-]+$/.test(seed.slug)) {
		throw new Error(`Invalid slug '${seed.slug}'. Expected lower-case letters, numbers, or dashes.`);
	}
	if (!seed.name || seed.name.trim().length === 0) {
		throw new Error(`Name is required for slug '${seed.slug}'.`);
	}
	const categories: BrandSeed['category'][] = ['courier', 'government', 'finance', 'tech', 'telecom', 'generic'];
	if (!categories.includes(seed.category)) {
		throw new Error(`Invalid category '${seed.category}' for slug '${seed.slug}'.`);
	}
};

/**
 * Delete rows from 'brand_seeds' that are not present in the current BRAND_SEEDS list.
 * This makes the table exactly match your seed file (full sync).
 */
export const deleteMissingSeed = async (): Promise<number> => {
	// 1) Fetch all slugs in DB
	const { data: dbRows, error: selectError } = await supabase.from('brand_seeds').select('slug');

	if (selectError) {
		throw new Error(`SupabaseSelectError: ${selectError.message}`);
	}

	const seedSlugs = new Set(BRAND_SEEDS.map((b) => b.slug));
	const toDelete = (dbRows ?? []).map((r) => r.slug).filter((slug) => !seedSlugs.has(slug));

	if (toDelete.length === 0) return 0;

	// 2) Delete any slugs not present in seeds
	const { error: deleteError, count } = await supabase.from('brand_seeds').delete({ count: 'exact' }).in('slug', toDelete);

	if (deleteError) {
		throw new Error(`SupabaseDeleteError: ${deleteError.message}`);
	}

	return count ?? toDelete.length;
};

/**
 * Upsert the full list of seeds into the 'brands' table.
 * Conflict key: 'slug' (unique). Existing rows are updated, new rows are inserted.
 */

export const upsertBrandSeeds = async () => {
	const rows = BRAND_SEEDS.map((seed) => {
		validateSeed(seed);
		return {
			slug: seed.slug,
			name: seed.name.trim(),
			category: seed.category,
			aliases: seed.aliases && seed.aliases.length > 0 ? seed.aliases : [],
			updated_at: new Date().toISOString()
		};
	});

	const { data, error } = await supabase.from('brand_seeds').upsert(rows, { onConflict: 'slug', ignoreDuplicates: false }).select();

	if (error) {
		throw new Error(`SupabaseUpsertError: ${error.message}`);
	}

	return data?.length ?? 0;
};

/**
 * Supabase JS/PostgREST doesn’t expose multi-statement transactions directly,
 * but doing upsert then delete is safe for your use-case since 'slug' uniqueness maintains integrity.
 */
async function main() {
	console.log('Starting brand sync...');

	const upsertedCount = await upsertBrandSeeds();
	console.log(`Upserted/updated ${upsertedCount} rows.`);

	const deletedCount = await deleteMissingSeed();
	console.log(`Deleted ${deletedCount} rows not present in seeds.`);

	console.log('Brand sync complete.');
}

// Allow running as a script: node pushBrand.ts (or ts-node)
// ts-node: npx ts-node scripts/pushBrandSeeds.ts
if (require.main === module) {
	main().catch((err) => {
		console.error(err);
		process.exit(1);
	});
}

export { main as pushBrandSync };
