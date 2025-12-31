// • Delivery & postal:
//     ▫ Canada Post: canadapost, postecanada, canada‑post, canadapost‑ca, cpost, cndpost, cp‑tracking, cp‑delivery
//     ▫ Purolator: purolator‑support, purolatornotify, purolatr, purolator‑express, puro‑tracking
//     ▫ FedEx/UPS/DHL: fedex‑id, fedexupdate, fədex (unicode), fdx‑tracking, ups‑info, upsresched, dhl‑express, dhlupd, dhl‑fee
//     ▫ USPS/Royal Mail: uspsconfrim, usps‑alert, usps‑delivery, royalmail‑uk, royal‑mail, evri/hermes: evri‑tracking, hermes‑parcel
//     ▫ Lure words: missed delivery, reschedule, delivery attempt, customs fee, import duty, final notice, last attempt, tracking code
//  • Retail & marketplaces:
//     ▫ Amazon/eBay: amazon‑verify, amaz0n, amzn‑otp, amazn‑prime, ebay‑alert, ebai‑signin, ebay‑verify
//     ▫ Walmart/Best Buy: walmart‑order, walmrt, bestbuy‑confirm, best‑buy support
//     ▫ Rides/food: uber‑receipt, uber‑susp., doordash‑update, skip‑thedishes, door‑dash, lyft‑account
//  • Finance & payments:
//     ▫ PayPal/cards: paypal‑notice, pay‑pal, paypaI (capital i), pypal, pp‑support, amex‑secure, amx, visa‑3dsecure, vlsa, mastercad, mɑstercard (unicode)
//     ▫ Banks (Canada): td‑alert, tdbnk, rbc‑verify, rbcbank, scotia‑secure, scotia‑online, cibc‑notice, bmo‑fraud, interac‑etransfer, interac‑auto‑deposit
//     ▫ Crypto/pay apps: coinbase‑secure, c0inbase, binance‑kyc, kraken‑login, cashapp‑support, venmo‑verify, zelle‑payment
//  • Tech platforms & email/cloud:
//     ▫ Apple/Microsoft/Google: apple‑id, applеid (unicode), icloud‑lock, microsoft‑account, micr0soft, ms‑secure, google‑verify, g00gle, gmail‑alert
//     ▫ Streaming/social: netflix‑payment, netflx, spotify‑update, disneyplus‑verify, facebook‑security, meta‑support, instagram‑help, ig‑confirm, whatsapp‑code, tiktok‑unlock, linkedin‑recovery
//     ▫ Storage/dev: adobe‑sign, dropbox‑share, onedrive‑file, steam‑guard, discord‑verify, metamask‑secure, ledger‑update, trezor‑notice
//  • Government & telecom + obfuscation tricks:
//     ▫ Government/tax: CRA‑refund, cra‑secure, servicecanada, svc‑canada, CBSA‑duty, IRS‑refund, HMRC‑rebate
//     ▫ Telecom/carriers: rogers‑bill, rogers‑win, bell‑prize, bell‑invoice, telus‑reward, fido‑bonus, koodo‑notice, at&t‑secure, verizon‑account, t‑mobile‑support
//     ▫ Generic lures: verify account, payment failed, account suspended, limited access, urgent, final reminder, confirm identity, KYC, 2FA, OTP, MFA, unlock now
//     ▫ Homoglyphs/typos: 0↔O, l↔1, rn↔m, a↔ɑ, e↔е, i↔ɪ, s↔ʂ; doubled/missing letters (canadapostt, fedx), swapped words (post canada)
//     ▫ Domain/TLD bait: brand‑support[.]top, brand‑secure[.]lol, brand‑update[.]icu, brand‑help[.]cn, support‑brand[.]xyz; fake subdomains like brand‑secure.login.example[.]com
//     ▫ Short‑link/redirect: bit.ly, tinyurl, ow.ly, goo.gl, lnk[.]today; tracking‑looking paths (/track/ID123, /delivery/confirm, /refund/submit)

// • Delivery & postal:
//     ▫ FedEx, UPS, DHL, Purolator, Canada Post, USPS, Royal Mail, Hermes/Evri, Yodel, Parcelforce, Australia Post
// • Retail & marketplaces:
//     ▫ Amazon, eBay, Walmart, Costco, Best Buy, Home Depot, Facebook Marketplace, Etsy, Airbnb, Booking.com, Uber, Lyft, DoorDash, Uber Eats, SkipTheDishes
// • Finance & payments:
//     ▫ PayPal, American Express, Visa, Mastercard, Interac e‑Transfer (Canada), TD, RBC, Scotiabank, CIBC, BMO, Capital One, Chase
// ▫ Cash App, Venmo, Zelle (US), Coinbase, Binance, Kraken
//     • Tech platforms & email/cloud:
//     ▫ Apple/iCloud, Microsoft, Google, Gmail, Outlook, Yahoo Mail, AOL Mail
//     ▫ Netflix, Spotify, Disney+, Hulu
//     ▫ Facebook, Instagram, WhatsApp, Snapchat, TikTok, LinkedIn
//     ▫ Adobe, Dropbox, OneDrive, Steam, Discord, MetaMask, Ledger, Trezor
// • Telecom & carriers:
//     ▫ Rogers, Bell, Telus, Fido, Koodo, Virgin Plus, Freedom Mobile, AT&T, Verizon, T‑Mobile
// • Government & services:
//     ▫ Canada Revenue Agency (CRA), Service Canada, ServiceOntario, CBSA/customs duty notices

export type BrandCategory = 'courier' | 'government' | 'finance' | 'tech' | 'telecom' | 'generic';

export type BrandSeed = {
	category: BrandCategory;
	slug: string; // machine-safe stable identifier, e.g. 'canada-post'
	name: string; // human-facing display name, e.g. 'Canada Post'
	aliases?: string[]; // optional localized or canonical alternatives
};

// prettier-ignore
export const GENERIC_BRANDS: BrandSeed[] = [
	{ category: 'generic', slug: 'courier-generic',    name: 'Courier',        aliases: ['delivery service', 'parcel service', 'courier'] },
	{ category: 'generic', slug: 'retail-generic',     name: 'Retailer',       aliases: ['store', 'marketplace', 'order service'] },
	{ category: 'generic', slug: 'telecom-generic',    name: 'Carrier',        aliases: ['mobile carrier', 'cell provider', 'phone company'] },
	{ category: 'generic', slug: 'tech-generic',       name: 'Tech Platform',  aliases: ['online account'] },
	{ category: 'generic', slug: 'government-generic', name: 'Government',     aliases: ['tax department', 'service center'] },
	{ category: 'generic', slug: 'banking-generic',    name: 'Bank',           aliases: ['financial institution'] }
];

// prettier-ignore
export const COURIER_BRANDS: BrandSeed[] = [
	{ category: 'courier', slug: 'canada-post', 			   name: 'Canada Post',  		 aliases: ['poste canada'] },
	{ category: 'courier', slug: 'purolator',   			   name: 'Purolator',    		 aliases: ['puro'] },
	{ category: 'courier', slug: 'fedex',       			   name: 'FedEx' },
	{ category: 'courier', slug: 'ups', 					   name: 'UPS', 				 aliases: ['myups', 'united parcel service'] },
	{ category: 'courier', slug: 'usps',        			   name: 'USPS',         		 aliases: ['united states postal service', 'us postal service'] },
	{ category: 'courier', slug: 'dhl',         			   name: 'DHL',          		 aliases: ['dhl express'] }
];

// prettier-ignore
export const GOVERNMENT_BRANDS: BrandSeed[] = [
	// Federal (Canada)
	{ category: 'government', slug: 'cbsa',            name: 'CBSA',             aliases: ['canada border services agency', 'canadian customs'] },
	{ category: 'government', slug: 'cra',             name: 'CRA',              aliases: ['canada revenue agency', 'revenue canada'] },
	{ category: 'government', slug: 'service-canada',  name: 'Service Canada' },

	// Provincial (Ontario)
	{ category: 'government', slug: 'service-ontario', name: 'ServiceOntario',   aliases: ['service ontario'] },
	{ category: 'government', slug: 'ontario-transport', name: 'Ministry of Transportation Ontario', aliases: ['mto', 'ontario ministry of transportation', 'ontario transport'] },
];

// prettier-ignore
export const FINANCE_BRANDS: BrandSeed[] = [
	{ category: 'finance', slug: 'banking-generic',  name: 'Bank',             aliases: ['financial institution'] },
	{ category: 'finance', slug: 'american-express', name: 'American Express', aliases: ['amex'] },
	{ category: 'finance', slug: 'bmo',              name: 'BMO',              aliases: ['bank of montreal'] },
	{ category: 'finance', slug: 'capital-one',      name: 'Capital One',      aliases: ['cap1'] },
	{ category: 'finance', slug: 'cibc',             name: 'CIBC',             aliases: ['canadian imperial bank of commerce', 'canadian imperial bank'] },
	{ category: 'finance', slug: 'interac',          name: 'Interac',          aliases: ['interac e-transfer', 'etransfer', 'e-transfer'] },
	{ category: 'finance', slug: 'mastercard',       name: 'Mastercard',       aliases: ['master card'] },
	{ category: 'finance', slug: 'paypal',           name: 'PayPal',           aliases: ['pay pal'] },
	{ category: 'finance', slug: 'rbc',              name: 'RBC',              aliases: ['royal bank', 'royal bank of canada'] },
	{ category: 'finance', slug: 'scotiabank',       name: 'Scotiabank',       aliases: ['scotia', 'bank of nova scotia'] },
	{ category: 'finance', slug: 'td',               name: 'TD',               aliases: ['td canada trust'] },
	{ category: 'finance', slug: 'visa',             name: 'Visa',             aliases: ['visa secure'] },
	{ category: 'finance', slug: 'wealthsimple',     name: 'Wealthsimple' },
	{ category: 'finance', slug: 'questrade',        name: 'Questrade' }
];

// prettier-ignore
export const TECH_BRANDS: BrandSeed[] = [
	{ category: 'tech', slug: 'adobe',        name: 'Adobe',        aliases: ['adobe sign', 'adobesign', 'adobe-sign'] },
	{ category: 'tech', slug: 'apple',        name: 'Apple',        aliases: ['icloud', 'apple id', 'appleid'] }, // collapse Apple ID/iCloud to Apple
	{ category: 'tech', slug: 'discord',      name: 'Discord' },
	{ category: 'tech', slug: 'disney-plus',  name: 'Disney+' },
	{ category: 'tech', slug: 'gmail',        name: 'Gmail',        aliases: ['google mail'] },
	{ category: 'tech', slug: 'google',       name: 'Google' },
	{ category: 'tech', slug: 'microsoft',    name: 'Microsoft',    aliases: ['microsoft account'] },
	{ category: 'tech', slug: 'netflix',      name: 'Netflix' },
	{ category: 'tech', slug: 'steam',        name: 'Steam',        aliases: ['steam guard'] },
	{ category: 'tech', slug: 'whatsapp',     name: 'WhatsApp' }
];

// prettier-ignore
export const TELECOM_BRANDS: BrandSeed[] = [
	{ category: 'telecom', slug: 'bell',            name: 'Bell' },
	{ category: 'telecom', slug: 'rogers',          name: 'Rogers',           aliases: ['rogers communications', 'rogers wireless'] },
	{ category: 'telecom', slug: 'telus',           name: 'TELUS' },
	{ category: 'telecom', slug: 'fido',            name: 'Fido',             aliases: ['fido solutions'] },
	{ category: 'telecom', slug: 'koodo',           name: 'Koodo',            aliases: ['koodo mobile'] },
	{ category: 'telecom', slug: 'freedom-mobile',  name: 'Freedom Mobile',   aliases: ['freedom mobile', 'freedom'] },
	{ category: 'telecom', slug: 'virgin-plus',     name: 'Virgin Plus',      aliases: ['virgin mobile', 'virgin mobile canada'] },
	{ category: 'telecom', slug: 'verizon',         name: 'Verizon',          aliases: ['verizon wireless'] },
	{ category: 'telecom', slug: 't-mobile',        name: 'T-Mobile',         aliases: ['tmobile', 't mobile'] },
	{ category: 'telecom', slug: 'att',             name: 'AT&T',             aliases: ['at&t', 'att'] },
];

export const BRAND_SEEDS = [...COURIER_BRANDS, ...GOVERNMENT_BRANDS, ...FINANCE_BRANDS, ...TECH_BRANDS, ...TELECOM_BRANDS];
