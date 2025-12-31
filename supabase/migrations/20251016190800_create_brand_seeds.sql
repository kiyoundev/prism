-- Create brand_seeds configuration table.
create table if not exists public.brand_seeds (
	slug text primary key,
	name text not null,
	category text not null check (category in ('courier', 'government', 'finance', 'tech', 'telecom', 'generic')),
	aliases text[] not null default '{}',
	updated_at timestamptz not null default now()
);

-- Optional: expose seeds for read-only consumers (e.g., seeding scripts, public lookups).
drop policy if exists "public can read brand_seeds"
	on public.brand_seeds;

create policy "public can read brand_seeds"
	on public.brand_seeds
	for select
	to anon
	using (true);
