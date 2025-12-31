export type Category = 'delivery' | 'ticket' | 'banking' | 'tax' | 'verification';

export const CATEGORY_KEYWORDS: Record<Category, string[]> = {
	// Delivery & logistics (high-signal multi-word first, then supportive singles)
	delivery: [
		'return to sender',
		'missed delivery',
		'schedule delivery',
		'attempted delivery',
		'delivery window',
		'tracking number',
		'track id',
		'delivery',
		'package',
		'parcel',
		'courier',
		'signature'
	],

	// Tickets, fines, violations (Canadian wording + variants)
	ticket: ['notice of infraction', 'parking notice', 'provincial offences', 'by-law', 'bylaw', 'violation', 'penalty', 'fine', 'ticket'],

	// Banking & payments (money movement/card terms; avoid status words)
	banking: ['e-transfer', 'interac', 'wire transfer', '3d secure', 'chargeback', 'card payment', 'transaction', 'statement', 'balance'],

	// Tax & benefits (CRA / Revenue Canada)
	tax: ['notice of assessment', 'cra refund', 'tax rebate', 'revenue canada', 'assessment', 'refund', 'benefit', 'tax'],

	// Verification / security / access (auth/status)
	verification: [
		'verification code',
		'otp',
		'2fa',
		'mfa',
		'account locked',
		'unusual activity',
		'verify',
		'confirm',
		'security',
		'unlock',
		'update',
		'login',
		'sign in'
	]

	// Generic urgent language
	// generic: ['important notice', 'final notice', 'action required', 'urgent', 'immediately', 'reminder']
};
