import { getClassifier } from './utils';
import { predictCategory } from './utils';

describe('classification', () => {
	const msg = `Purolator Delivery Update – Action Required

We were unable to deliver your package on August 07 because a signature was required and no one was available. a0
To avoid your shipment being returned to the sender, you must schedule a new delivery or select a pick-up location by August 09.

Please choose your preferred option now:

https://purolator.com-payrp.vip/ca

Available options:
・ Set a new delivery date and time
・ Redirect your package to a Purolator pick-up point

If no action is taken by August 09, your package will automatically be returned to the sender.

To activate the link, reply 'Y', close and reopen this message, or copy and paste it into your Safari browser.`;

	const clf = getClassifier();
	it('should return the correct category', () => {
		expect(predictCategory(clf, msg)).toEqual('delivery');
	});

	// describe('', () => {
	// 	const msg = ``;
	// 	it('should return the correct category', () => {
	// 		expect(getClassifier().classify(msg)).toEqual('courier');
	// 	});
	// });
});
