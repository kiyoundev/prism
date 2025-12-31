-- This migration creates the known_scams table and a policy to allow public read access.
create table if not exists public.known_scams (
	id text primary key,
	title text not null,
	patterns text[] not null default '{}',
	message text not null,
	tags text[] not null default '{}',
	notes text,
	links jsonb not null default '[]'::jsonb,
	attachments jsonb
);

drop policy if exists "public can read known_scams"
	on public.known_scams;

create policy "public can read known_scams"
	on public.known_scams
	for select
	to anon
	using (true);
