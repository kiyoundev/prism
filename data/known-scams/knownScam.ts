import { type KnownScam } from './definition';

// {
// 	id: '',
// 	title: '',
// 	pattern: '',
// 	message: '',
// 	tags: [],
// 	notes: '',
// 	links: [
// 		{
// 			display: '',
// 			href: ''
// 		}
// 	],
// 	attachments: [
// 		{
// 			type: '',
// 			filename: '',
// 			extractedText: '',
// 			sha256: '',
// 			phash: ''
// 		}
// 	]
// }

// Format: sms-<brand|authority>-<topic>-<variant>
// Channel prefix: always sms-
// Brand/authority: lowercase kebab slug of the sender being spoofed (e.g., purolator, canada-post, ontario-transport)
// Topic: short descriptive slug like delivery-update, parking-ticket, account-login
// Variant: optional numeric suffix (-01, -02, …) when multiple distinct samples exist for the same brand/topic

// sms-purolator-delivery-update-01
// sms-purolator-delivery-update-02
// sms-rogers-payment-reminder-01
// sms-ontario-transport-ticket-03

// "_meta": {
//     "description": "Curated SMS scams for deterministic rule detection.",
//     "fields": {
//         "id": "Stable kebab-case identifier for this rule entry.",
//         "type": "Channel of scam content (currently only 'sms').",
//         "title": "Human-readable label summarizing the scam.",
//         "pattern": "Snippet or phrase the matcher searches for.",
//         "message": "Representative scam message used for tests and reference.",
//         "tags": "Array of categorical keywords used for scoring/explanations.",
//         "notes": "Optional implementation notes (e.g., unicode obfuscation)."
//     },
//     "idConvention": "sms-<brand-or-authority>-<topic>-<variant>"
// },



// | Field    | Value                                                                      |
// |----------|----------------------------------------------------------------------------|
// | id       | `sms-purolator-delivery-01`                                                |
// | title    | `Purolator Schedule Delivery`                                              |
// | category | `delivery`                                                                 |
// | pattern  | `['schedule', 'reply "Y"', 'return to sender']` |
// | tags     | `['delivery', 'link', 'schedule', 'unicode']`                              |
// | notes    | `Message retains a non-breaking space (\u00a0) and other Unicode glyphs for reference.` |
// | links    | `[{display: 'https://purolator.com-payrp.vip/ca', href: 'https://purolator.com-payrp.vip/ca'}]` |
// | attachments | `[]` |
// | message  | `` 


export const KNOWN_SCAMS: KnownScam[] = [
	{
		
	}
]


const data: KnownScam[] = [
	{
		id: 'sms-purolator-schedule-delivery',
		title: 'Purolator Schedule Delivery',
		pattern: 'purolator.com-payrp.vip',
		message:
			"Purolator Delivery Update – Action Required\n\nWe were unable to deliver your package on August 07 because a signature was required and no one was available.\u00a0 \nTo avoid your shipment being returned to the sender, you must schedule a new delivery or select a pick-up location by August 09.\n\nPlease choose your preferred option now:\n\nhttps://purolator.com-payrp.vip/ca\n\nAvailable options:\n・ Set a new delivery date and time\n・ Redirect your package to a Purolator pick-up point\n\nIf no action is taken by August 09, your package will automatically be returned to the sender.\n\nTo activate the link, reply 'Y', close and reopen this message, or copy and paste it into your Safari browser.",
		tags: ['delivery', 'schedule', 'link', 'unicode'],
		notes: 'Message retains a non-breaking space (\u00a0) and other Unicode glyphs for reference.',
		links: [
			{
				display: 'https://purolator.com-payrp.vip/ca',
				href: 'https://purolator.com-payrp.vip/ca'
			}
		],
		attachments: []
	},
	{
		id: 'sms-purolator-package-on-hold',
		title: 'Purolator Package On Hold Notification',
		pattern: 'purolator.etcydh.vip',
		message:
			'[Purolator] – Package On Hold Notification\n\nYour parcel is currently being processed. Due to an invalid postal code, it cannot be delivered and has been temporarily held. Please verify your postal code within 24 hours using the link below.\u200b\n\nhttps://purolator.etcydh.vip/ca\n\n(Reply Y and re-open this message to click the link, or copy it to your browser.)',
		tags: ['delivery', 'link'],
		notes: 'Includes zero-width space before the line break preceding the URL.',
		links: [
			{
				display: 'https://purolator.etcydh.vip/ca',
				href: 'https://purolator.etcydh.vip/ca'
			}
		],
		attachments: []
	}
];
