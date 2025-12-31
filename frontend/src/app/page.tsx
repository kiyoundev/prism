import { sha256 } from '@/packages/shared/utils/hash';
import { join } from 'node:path';
import { cwd } from 'node:process';
import { search, fuzzy } from 'fast-fuzzy';
import natural from 'natural';
// import { buildRuleId, detectTopic, normalizeBrand } from '@/lib/brand_seeds';
// import { slugify } from '@/lib/string-utils';
// import { extractBrand } from '@/lib/utils';

import { normalize, extractBrand, extractCategory, deriveCategoryVariants, getClassifier } from '@/lib/utils';
import { BRAND_SEEDS, CATEGORY_KEYWORDS, COURIER_BRANDS } from '@/lib/brand_seeds';
import unhomoglyph from 'unhomoglyph';
import { mapTokens } from '@/lib/utils';

const NGrams = natural.NGrams;

const msg = `Purolator Delivery Update – Action Required

We were unable to deliver your package on August 07 because a signature was required and no one was available.
To avoid your shipment being returned to the sender, you must schedule a new delivery or select a pick-up location by August 09.

Please choose your preferred option now:

https://purolator.com-payrp.vip/ca

Available options:
・ Set a new delivery date and time
・ Redirect your package to a Purolator pick-up point

If no action is taken by August 09, your package will automatically be returned to the sender.

To activate the link, reply 'Y', close and reopen this message, or copy and paste it into your Safari browser.`;

export default async function Home() {
	// return <main>{sha256('test')}</main>;

	// const filePath = join(cwd(), 'data/rules/file_1736642821957.jpg');
	// const hash = await sha256(filePath);

	// console.log(normalizeBrand(msg));
	// console.log(detectTopic(msg));
	// console.log(buildRuleId(normalizeBrand(msg), detectTopic(msg), new Set()));

	// console.log(extractBrand('Reminder: your package from ups is pending customs. Track at example.com', COURIER_BRANDS));
	// console.log(extractBrand('Your Canada Post delivery is ready for pickup.', [COURIER_BRANDS[0]]));

	console.log(extractCategory(msg));

	return null;
}
