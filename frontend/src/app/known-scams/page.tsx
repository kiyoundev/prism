import { createClient } from '@/lib/server';

export default async function KnownScamsPage() {
	const supabase = await createClient();
	const { data: knownScamEntries } = await supabase.from('known_scams').select();
	return <pre>{JSON.stringify(knownScamEntries, null, 2)}</pre>;
}
