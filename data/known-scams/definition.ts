// "_meta": {
//   "description": "Curated SMS scams for deterministic rule detection.",
//   "fields": {
//     "id": "Stable kebab-case identifier for this rule entry.",
//     "type": "Channel of scam content (currently only 'sms').",
//     "title": "Human-readable label summarizing the scam.",
//     "pattern": "Snippet or phrase the matcher searches for.",
//     "message": "Representative scam message used for tests and reference.",
//     "tags": "Array of categorical keywords used for scoring/explanations.",
//     "notes": "Optional implementation notes (e.g., unicode obfuscation)."
//   },
//   "idConvention": "sms-<brand-or-authority>-<topic>-<variant>"
// },

// {
//   id: 'sms-purolator-delivery-update',
//   title: 'Purolator Delivery Update',
//   pattern: 'purolator.com-payrp.vip',
//   message:
//     "Purolator Delivery Update – Action Required\n\nWe were unable to deliver your package on August 07 because a signature was required and no one was available.\u00a0 \nTo avoid your shipment being returned to the sender, you must schedule a new delivery or select a pick-up location by August 09.\n\nPlease choose your preferred option now:\n\nhttps://purolator.com-payrp.vip/ca\n\nAvailable options:\n・ Set a new delivery date and time\n・ Redirect your package to a Purolator pick-up point\n\nIf no action is taken by August 09, your package will automatically be returned to the sender.\n\nTo activate the link, reply 'Y', close and reopen this message, or copy and paste it into your Safari browser.",
//   tags: ['delivery', 'schedule', 'link', 'unicode'],
//   notes: 'Message retains a non-breaking space (\u00a0) and other Unicode glyphs for reference.',
//   links: [
//     {
//       display: 'https://purolator.com-payrp.vip/ca',
//       href: 'https://purolator.com-payrp.vip/ca'
//     }
//   ],
//   attachments: [
//     {
//       type: '',
//       filename: '',
//       extractedText: '',
//       sha256: '',
//       phash: ''
//     }
//   ]
// }

export type KnownScam = {
	id: string;
	title: string;
	pattern: string;
	message: string;
	tags: string[];
	notes: string;
	links: {
		display: string;
		href: string;
	}[];
	attachments?: {
		type: string;
		filename: string;
		extractedText: string;
		sha256: string;
		phash: string;
	}[];
};
