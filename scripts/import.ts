// scripts/import-known-scams.ts
import 'dotenv/config';
import { createClient } from '@supabase/supabase-js';
import { KNOWN_SCAMS } from '../data/known-scams/knownScam';

const url = process.env.SUPABASE_URL!;
const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
const supabase = createClient(url, serviceKey);

async function run() {
	const { error } = await supabase.from('known_scams').upsert(KNOWN_SCAMS, { onConflict: 'id' });

	if (error) throw error;
	console.log(`Imported ${KNOWN_SCAMS.length} records.`);
}

run().catch((err) => {
	console.error(err);
	process.exit(1);
});
