-- This migration creates the scam_brand_aliases table and a policy to allow public read access.
create table if not exists public.scam_brand_aliases (
  brand    text primary key,
  aliases text[] not null default '{}'
);

drop policy if exists "public can read scam_brand_aliases"
	on public.scam_brand_aliases;

create policy "public can read scam_brand_aliases"
	on public.scam_brand_aliases
	for select
	to anon
	using (true);
