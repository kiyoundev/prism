const WHITESPACE_REGEX = /\s+/g;
const NON_ALNUM_REGEX = /[^a-z0-9-]/g;

export const slugify = (value: string): string =>
	value.toLowerCase().trim().replace(WHITESPACE_REGEX, '-').replace(NON_ALNUM_REGEX, '').replace(/-+/g, '-').replace(/^-|-$/g, '');
