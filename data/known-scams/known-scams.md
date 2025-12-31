<!--
    Format: sms-<brand|authority>-<topic>-<variant>
    Channel prefix: always sms-
    Brand/authority: lowercase kebab slug of the sender being spoofed (e.g., purolator, canada-post, ontario-transport)
    Topic: short descriptive slug like delivery-update, parking-ticket, account-login
    Variant: optional numeric suffix (-01, -02, …) when multiple distinct samples exist for the same brand/topic
-->

<!-- 
    "id": "Stable kebab-case identifier for this rule entry.",
    "title": "Human-readable label summarizing the scam.",
    "pattern": "Snippet or phrase the matcher searches for.",
    "message": "Representative scam message used for tests and reference.",
    "tags": "Array of categorical keywords used for scoring/explanations.",
    "notes": "Optional implementation notes (e.g., unicode obfuscation)."
-->

## 1.

### message
Purolator Delivery Update – Action Required

We were unable to deliver your package on August 07 because a signature was required and no one was available.
To avoid your shipment being returned to the sender, you must schedule a new delivery or select a pick-up location by August 09.

Please choose your preferred option now:

https://purolator.com-payrp.vip/ca

Available options:
・ Set a new delivery date and time
・ Redirect your package to a Purolator pick-up point

If no action is taken by August 09, your package will automatically be returned to the sender.

To activate the link, reply 'Y', close and reopen this message, or copy and paste it into your Safari browser.

### data
| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-purolator-delivery-01`                                                |
| title    | `Purolator Schedule Delivery`                                              |
| category | `delivery`                                                                 |
| pattern  | `['schedule', 'reply "Y"', 'return to sender']` |
| tags     | `['delivery', 'link', 'schedule', 'unicode']`                              |
| notes    | `Message retains a non-breaking space (\u00a0) and other Unicode glyphs for reference.` |
| links    | `[{display: 'https://purolator.com-payrp.vip/ca', href: 'https://purolator.com-payrp.vip/ca'}]` |
| attachments | `[]` |
| message  | `` 

## 2.

### message
[Purolator] – Package On Hold Notification

Your parcel is currently being processed. Due to an invalid postal code, it cannot be delivered and has been temporarily held. Please verify your postal code within 24 hours using the link below.​

https://purolator.etcydh.vip/ca

(Reply Y and re-open this message to click the link, or copy it to your browser.)

### data
| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-purolator-package-on-hold-01`                                         |
| title    | `Purolator Package On Hold Notification`                                   |
| category | `delivery`                                                                 |
| pattern  | `['invalid postal code', 'reply "Y"', 'within 24 hours']`|
| tags     | `['delivery', 'link', 'package-on-hold']`                                  |
| notes    | `Includes zero-width space (\u200b) immediately before the URL.`             |
| links    | `[{display: 'https://purolator.etcydh.vip/ca', href: 'https://purolator.etcydh.vip/ca'}]` |
| attachments | `[]` |
| message  | `` 

## 3.

### message
ᎡоցеrѕԜіrеⅼеѕѕ-5Ꮐ
Τhіѕ іѕ а rеⅿіοⅾер thат уоսr ѕеrⅴісеѕ соսⅼⅾ bе іοтеrrսρтеⅾ ⅾսе tο а ⅿіѕѕеⅾ раўⅿеոτ. То еοѕսrе уοսr ѕеrⅴісе rеⅿаіοѕ асτіⅴе, рⅼеаѕе սρⅾаτε уοսr раўⅿеոτ іοƒοrⅿаτιοո ат:  https://myrogers5g-mobility-en.net

### data
| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-rogers-payment-reminder-01`                                           |
| title    | `Rogers 5G Payment Reminder`                                               |
| category | `payment`                                                                  |
| pattern  | `['reminder', 'service interruption', 'missed payment']` |
| tags     | `['payment', 'link', 'unicode']`                                           |
| notes    | `Spoofs Rogers with extensive homoglyph substitutions and a fake mobility portal.` |
| links    | `[{display: 'https://myrogers5g-mobility-en.net', href: 'https://myrogers5g-mobility-en.net'}]` |
| attachments | `[]` |
| message  | `` 

## 4.

### message
Ticket #2686349
Heads Up! Your unpaid ticket #18973679 has initiated a review of your license. Take action now to keep your driving privileges intact.
https://google.com/url?q=https://parking-canada-ticket.com

### data
| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-parking-canada-unpaid-ticket-01`                                      |
| title    | `Parking Canada Unpaid Ticket`                                             |
| category | `ticket`                                                                   |
| pattern  | `['unpaid ticket', 'license review', 'take action']`         |
| tags     | `['ticket', 'link']`                                                       |
| notes    | `Uses a Google redirector link to obscure the destination domain.`           |
| links    | `[{display: 'https://google.com/url?q=https://parking-canada-ticket.com', href: 'https://parking-canada-ticket.com'}]` |
| attachments | `[]` |
| message  | `` 

## 5.

### message
Ticket #18973679
Your overdue ticket has triggered a review of your driver’s license. Pay in full now to avoid losing your driving privileges.
https://google.com/url?q=https://tickets-reminder-parking.com

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-parking-canada-overdue-ticket-01`                                      |
| title    | `Parking Canada Overdue Ticket`                                             |
| category | `ticket`                                                                   |
| pattern  | `['overdue ticket', 'license review', 'pay in full']`         |
| tags     | `['ticket', 'link']`                                                       |
| notes    | `Uses a Google redirector link to obscure the destination domain.`           |
| links    | `[{display: 'https://google.com/url?q=https://tickets-reminder-parking.com', href: 'https://tickets-reminder-parking.com'}]` |
| attachments | `[]` |
| message  | `` |

## 6.

### message
[FedEx]: Your package is delayed because of incorrect address information. Please reschedule the delivery at https://google.com/amp/fedexclient-delivery.com as soon as possible.

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-fedex-delivery-update-01`                                             |
| title    | `FedEx Delayed Package`                                                     |
| category | `delivery`                                                                 |
| pattern  | `['incorrect address', 'reschedule delivery', 'delayed']` |
| tags     | `['delivery', 'link']`                                                     |
| notes    | `Abuses a Google AMP link to hide the phishing domain.`                      |
| links    | `[{display: 'https://google.com/amp/fedexclient-delivery.com', href: 'https://google.com/amp/fedexclient-delivery.com'}]` |
| attachments | `[]` |
| message  | `` |

## 7.

### message
Your Hst-Ref#76577 for $435 is now ready. See .crasecurecadeposit.com@Expires 29-01-25.

### data
| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-cra-deposit-01`                                                       |
| title    | `CRA Deposit Ready`                                                        |
| category | `tax`                                                                      |
| pattern  | `['crasecurecadeposit.com', 'HST', 'expires 29-01-25']`                    |
| tags     | `['tax', 'link']`                                                          |
| notes    | `Combines an HST reference number and expiry date to increase urgency.`     |
| links    | `[{display: 'crasecurecadeposit.com', href: 'https://crasecurecadeposit.com'}]` |
| attachments | `[]` |
| message  | `` |

## 8.

### message
Canadian Customs: You have a  parcel being cleared, due to the detection of an invalid zip code address, the parcel can not be cleared, the parcel is temporarily detained, please confirm the zip
code address information in the link
within 24 hours. 

https://canada.postscanadacuy.top/ca

(Please reply with a Y, then exit the text message and open it again to activate the link, or copy the link into your Safari browser and open it)
Have a great day from the Canada Post Team team!

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-canada-post-customs-01`                                                |
| title    | `Canada Post Customs Parcel Clearance`                                                  |
| category | `delivery`                                                                 |
| pattern  | `['invalid zip code', 'invalid address','temporarily detained', 'within 24 hours']` |
| tags     | `['delivery', 'link', 'customs']`                                                     |
| notes    | `Contains doubled spacing before “parcel” and repeats the Canada Post closing line.` |
| links    | `[{display: 'https://canada.postscanadacuy.top/ca', href: 'https://canada.postscanadacuy.top/ca'}]` |
| attachments | `[]` |
| message  | `` |

## 9.

### message
Costco Team : Your black friday award is here! Thank you for your loyalty over the years. You can redeem your cash back at; 2024annualrewards-wholesalesteam.info

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-costco-black-friday-reward-01`                                         |
| title    | `Costco Black Friday Award`                                                  |
| category | `promotion`                                                                |
| pattern  | `['black friday reward', 'cash back', 'redeem']` |
| tags     | `['promotion', 'link', 'cashback']`                                                    |
| notes    | `Uses a faux rewards domain.`                   |
| links    | `[{display: '2024annualrewards-wholesalesteam.info', href: 'https://2024annualrewards-wholesalesteam.info'}]` |
| attachments | `[]` |
| message  | `` |


## 10.

### message
ꓲꓚꓡꓳꓴꓓ ꓮꓡꓰꓣꓔ: ꓔһеrе ԝаѕ а рrоbꓲеm ԝітһ уоսr раўmеոτ ԁеտаіꓲѕ. ꓑꓲеаѕе rеνіеԝ аոԁ սρԁаտе уоսr ԁеտаіꓲѕ ат manage-account-detail.com

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-icloud-account-update-01`                                         |
| title    | `iCloud Account Payment Details Alert`                                                  |
| category | `account`                                                                |
| pattern  | `['payment details', 'review', 'update']` |
| tags     | `['account', 'link', 'unicode']`                                                    |
| notes    | `Sender name relies on stylized glyphs while the payload uri is plain text.`                   |
| links    | `[{display: 'manage-account-detail.com', href: 'https://manage-account-detail.com'}]` |
| attachments | `[]` |
| message  | `` |


## 11.

### message
Canadian Customs: You have a  parcel being cleared, due to the detection of an invalid zip code address, the parcel can not be cleared, the parcel is temporarily detained, please confirm the zip
code address information in the link
within 24 hours. 

https://canpost.com-efdsgs.top/ca

(Please reply with a Y, then exit the text message and open it again to activate the link, or copy the link into your Safari browser and open it)

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-canada-post-customs-02`                                         |
| title    | `Canada Post Customs Parcel Clearance`                                                  |
| category | `delivery`                                                                |
| pattern  | `['invalid zip code', 'invalid address', 'temporarily detained', 'within 24 hours']` |
| tags     | `['delivery', 'link', 'customs']`                                                    |
| notes    | `Variant of the customs hold message pointing to canpost.com-efdsgs.top.`                   |
| links    | `[{display: 'https://canpost.com-efdsgs.top/ca', href: 'https://canpost.com-efdsgs.top/ca'}]` |
| attachments | `[]` |
| message  | `` |

## 12.

## message
ꓮꓲеrt ꓚаոаdа ꓔісkеt ꓓераrtmеոt: ꓓеаr 19054814804, ꓔһіѕ mеѕѕаցе ѕеrνеѕ аѕ а fоrmаꓲ ոоtісе rеցаrdіոց аո սոраіd раrkіոց νіоꓲаtіоո dаtеd ꓮսցսѕt 18, 2024. ꓮѕ оf tһе dаtе оf tһіѕ ꓲеttеr, рауmеոt fоr tһе νіоꓲаtіоո һаѕ ոоt bееո rесеіνеd, dеѕріtе рrіоr ոоtіfісаtіоոѕ.
 
ꓝаіꓲսrе tо соmрꓲу ԝіtһ tһіѕ dеаdꓲіոе оf ꓳсtоbеr 20, 2024, ԝіꓲꓲ rеѕսꓲt іո tһе fоꓲꓲоԝіոց ѕеνеrе соոѕеզսеոсеѕ:

1. ꓡісеոѕе ꓢսѕреոѕіоո: ꓬоսr νеһісꓲе’ѕ rеցіѕtrаtіоո аոd ꓲісеոѕе соսꓲd bе fꓲаցցеd fоr ѕսѕреոѕіоո.
 
2. ꓚоꓲꓲесtіоո ꓮցеոсу ꓣеfеrrаꓲ: ꓔһе mаttеr mау bе tսrոеd оνеr tо а соꓲꓲесtіоո аցеոсу, ԝһісһ соսꓲd аdd аddіtіоոаꓲ fееѕ.
 
3. ꓲոсrеаѕеd ꓝіոе: ꓔһе fіոе fоr tһіѕ νіоꓲаtіоո ԝіꓲꓲ bе dоսbꓲеd.
 
4. ꓲոаbіꓲіtу tо ꓣеոеԝ ꓦеһісꓲе ꓣеցіѕtrаtіоո: ꓬоս mау bе սոаbꓲе tо rеոеԝ уоսr νеһісꓲе rеցіѕtrаtіоո оr оbtаіո а ոеԝ drіνеr’ѕ ꓲісеոѕе սոtіꓲ tһе dеbt іѕ сꓲеаrеd.
 
ꓑrеνеոt fսrtһеr асtіоո bу рауіոց уоսr оսtѕtаոdіոց bаꓲаոсе bу ꓳсtоbеr 20, 2024. ꓬоս саո ѕսbmіt рауmеոt νіа tickets-unsettled-transports-ca.com

### data
| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-canada-transport-parking-ticket-01`                                         |
| title    | `Canada Transport Unpaid Ticket`                                                  |
| category | `ticket`                                                                |
| pattern  | `['unpaid', 'license suspension', 'violation', 'failure to comply', 'severe consequences', 'collection agency', 'fine']` |
| tags     | `['ticket', 'link', 'unicode', 'unpaid parking ticket']`                                                    |
| notes    | `Enumerates four penalties and drives to tickets-unsettled-transports-ca.com.`                   |
| links    | `[{display: 'tickets-unsettled-transports-ca.com', href: 'https://tickets-unsettled-transports-ca.com'}]` |
| attachments | `[]` |
| message  | `` |

## 13.

### message
MyUPS: Reschedule your package now before it's returned to sender. To complete, go to https://redelivauthcentre.com/ Final notice from MyUPS.

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-ups-reschedule-delivery-01`                                         |
| title    | `UPS Re-schedule Delivery`                                                  |
| category | `delivery`                                                                |
| pattern  | `['reschedule your package', 'final notice', 'return to sender']` |
| tags     | `['delivery', 'link', 'ups', 'MyUPS']`                                                    |
| notes    | `Spoofs UPS automation with a fake authentication center domain.`                   |
| links    | `[{display: 'https://redelivauthcentre.com/', href: 'https://redelivauthcentre.com/'}]` |
| attachments | `[]` |
| message  | `` |

## 14.

## message
ꓮꓡꓰꓣꓔ ꓴꓠꓑꓮꓲꓓ ꓔꓲꓚꓗꓰꓔ: ꓓеаr 19054814804, ꓲ һоре tһіѕ mеѕѕаցе fіոdѕ уоս ԝеꓲꓲ. ꓪе аrе ԝrіtіոց tо rеmіոd уоս оf аո սոраіd раrkіոց tісkеt іѕѕսеd оո ꓮսցսѕt 4, 2024. ꓓеѕріtе рrіоr ոоtіfісаtіоոѕ, оսr rесоrdѕ іոdісаtе tһаt ոо рауmеոt һаѕ bееո rесеіνеd tо dаtе.
 
ꓑꓲеаѕе bе аdνіѕеd tһаt іmmеdіаtе рауmеոt іѕ rеզսіrеd. ꓔһе tоtаꓲ аmоսոt dսе mսѕt bе раіd іո fսꓲꓲ bу ꓳсtоbеr 7, 2024. ꓝаіꓲսrе tо ѕеttꓲе tһіѕ аmоսոt bу tһе ѕtаtеd dеаdꓲіոе ԝіꓲꓲ rеѕսꓲt іո ѕеνеrе соոѕеզսеոсеѕ, ԝһісһ mау іոсꓲսdе bսt аrе ոоt ꓲіmіtеd tо tһе fоꓲꓲоԝіոց:

1. ꓢսѕреոѕіоո оf уоսr νеһісꓲе rеցіѕtrаtіоո սոtіꓲ tһе оսtѕtаոdіոց аmоսոt іѕ раіd.
 
2. ꓬоսr drіνеr'ѕ ꓲісеոѕе соսꓲd bе ѕսѕреոdеd սոtіꓲ tһе dеbt іѕ сꓲеаrеd.
 
3. ꓡаtе fееѕ аոd іոtеrеѕt сһаrցеѕ ԝіꓲꓲ ассrսе, іոсrеаѕіոց tһе аmоսոt уоս оԝе.
 
4. ꓚоսrt ꓢսmmоոѕ: ꓡеցаꓲ асtіоո mау bе tаkеո, ꓲеаdіոց tо а соսrt ѕսmmоոѕ.
 
ꓲf tһе рауmеոt іѕ ոоt ѕеttꓲеd bу ꓳсtоbеr 7, 2024, ԝе ԝіꓲꓲ һаνе tо рrосееd ԝіtһ tһе ոесеѕѕаrу асtіоոѕ. ꓑауmеոtѕ саո bе соmрꓲеtеd оո оսr ԝеbѕіtе ticket-unresolved-fine.com.
 
ꓔһаոk уоս fоr rеѕоꓲνіոց tһіѕ іѕѕսе іո а tіmеꓲу mаոոеr.

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-generic-parking-ticket-01`                                         |
| title    | `Unpaid Parking Ticket`                                                  |
| category | `ticket`                                                                |
| pattern  | `['unpaid parking ticket', 'immediate payment', 'severe consequences', 'court summons', 'legal actions', 'failure to settle', 'suspension']` |
| tags     | `['ticket', 'link', 'unicode', 'unpaid parking ticket']`                                                    |
| notes    | `Warns of four escalating penalties and links to ticket-unresolved-fine.com.`                   |
| links    | `[{display: 'ticket-unresolved-fine.com', href: 'https://ticket-unresolved-fine.com'}]` |
| attachments | `[]` |
| message  | `` |


## 15.

### message
ꓮꓲеrt ꓚаոаdа ꓔісkеt ꓓераrtmеոt: ꓓеаr 19054814804,ꓲ аm ԝrіtіոց rеցаrdіոց аո оսtѕtаոdіոց раrkіոց tісkеt іѕѕսеd оո 20 ꓙսꓲу 2024 fоr νеһісꓲе. ꓮѕ оf tоdау, tһе fіոе rеmаіոѕ սոраіd. ꓑꓲеаѕе bе аdνіѕеd tһаt tһе dеаdꓲіոе fоr рауmеոt іѕ ꓢерtеmbеr 24, 2024.
 
1. ꓚоսrt ꓢսmmоոѕ: ꓚоոtіոսеd ոоո-рауmеոt mау ꓲеаd tо а соսrt ѕսmmоոѕ, роѕѕіbꓲу rеѕսꓲtіոց іո аddіtіоոаꓲ ꓲеցаꓲ fееѕ.
 
2. ꓢսѕреոѕіоո оf ꓦеһісꓲе ꓣеցіѕtrаtіоո: ꓴոраіd fіոеѕ mау rеѕսꓲt іո ѕսѕреոѕіоո оf уоսr νеһісꓲе rеցіѕtrаtіоո, mаkіոց іt іꓲꓲеցаꓲ tо drіνе սոtіꓲ ѕеttꓲеd.
 
3. ꓲոсrеаѕеd ꓝіոеѕ: ꓔһе fіոе ԝіꓲꓲ ассrսе ꓲаtе fееѕ, іոсrеаѕіոց tһе tоtаꓲ аmоսոt dսе.
 
ꓑꓲеаѕе bе сеrtаіո tо рау tһе dսе амоսոт bу ꓢерtеmbеr 24, 2024, tо аνоіd tһеѕе реոаꓲtіеѕ. ꓑауmеոтѕ саո bе mаdе tһrоսցһ services-parking-online.com

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-canada-transport-parking-ticket-02`                                         |
| title    | `Canada Transport Unpaid Parking Ticket`                                                  |
| category | `ticket`                                                                |
| pattern  | `['unpaid', 'parking ticket', 'court summons', 'suspension', 'increased fine', 'late fees']` |
| tags     | `['ticket', 'link', 'unicode']`                                                    |
| notes    | `Highlights three escalating consequences with services-parking-online.com as the CTA.`                   |
| links    | `[{display: 'services-parking-online.com', href: 'https://services-parking-online.com'}]` |
| attachments | `[]` |
| message  | `` |

## 16.

### message
ꓮꓡꓰꓣꓔ ꓪꓰꓮꓡꓔꓢꓲꓟꓑꓡꓰ : ꓴոаսtһоrіzеd ꓲоցіո аttеmрt dеtесtеd frоm ꓲꓑ 25.42.0.1 оո уоսr ассоսոt.
ꓑꓲеаѕе νіѕіt activity-wealthsimple-mobile.com tо νіеԝ tһіѕ սոаսtһоrіzеd ꓲоցіո!

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-wealthsimple-unauthorized-login-01`                                         |
| title    | `Wealthsimple Unauthorized Login`                                                  |
| category | `account`                                                                |
| pattern  | `['unauthorized login', 'IP', 'detected']` |
| tags     | `['account', 'security', 'link', 'unicode']`                                                    |
| notes    | `Includes a raw IP address and homoglyph substitutions to mimic Wealthsimple.`                   |
| links    | `[{display: 'activity-wealthsimple-mobile.com', href: 'https://activity-wealthsimple-mobile.com'}]` |
| attachments | `[]` |
| message  | `` |


## 17.

### message
Canada Post: Your package has arrived at the warehouse and has been suspended due to a missing home number in the package and cannot be delivered. Please update: 

https://canadaspost-postecanadaum.top/ca

(Please reply Y, then exit the text message, reopen the text message activation link, or copy the link into your Safari browser and open it)

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-canada-post-delivery-01`                                         |
| title    | `Canada Post Missing Home Number`                                                  |
| category | `delivery`                                                                |
| pattern  | `['missing home number', 'suspended', 'reply Y', 'copy the link']` |
| tags     | `['delivery', 'link']`                                                    |
| notes    | `Encourages the victim to reply “Y” or re-open the SMS to activate the link.`                   |
| links    | `[{display: 'https://canadaspost-postecanadaum.top/ca', href: 'https://canadaspost-postecanadaum.top/ca'}]` |
| attachments | `[]` |
| message  | `` |


## 18.

### message
ꓔһе ꓟіոіѕτгў οf ꓔгαոѕροгτατιοո οf ꓳոταγιο: ꓓеαг 19054814804,

ꓔһеѕε αςτιοηѕ ẃιΛΛ ьε τακεη ẃιτһουτ ƒυρτһәг ոοτιςε. ꓔο ανοιԁ τһеѕε ѕενегε ρεναΛτιες, ρԼεαѕε раў τһе οսτѕταοԁιηγ αμοսոτ ьу ꓐυցυστ 3, 2024. ꓑαўμеοτѕ σαո ьε μαԁε οηλιοε ατ ticket-ontario-unpaid.com

### data

| Field    | Value                                                                      |
|----------|----------------------------------------------------------------------------|
| id       | `sms-ontario-transport-outstanding-01`                                         |
| title    | `Ontario Transport Final Warning (Aug 3)`                                                  |
| category | `ticket`                                                                |
| pattern  | `['ticket-ontario-unpaid.com', 'August 3', 'final warning']` |
| tags     | `['ticket', 'link', 'unicode']`                                                    |
| notes    | `Lists five escalating threats culminating in vehicle enforcement.`                   |
| links    | `[{display: 'ticket-ontario-unpaid.com', href: 'https://ticket-ontario-unpaid.com'}]` |
| attachments | `[]` |
| message  | `` |

id: 'sms-ontario-transport-outstanding-08-03'
title: 'Ontario Transport Final Warning (Aug 3)'
category: 'ticket'
pattern: ['ticket-ontario-unpaid.com', 'August 3', 'final warning']
message: "ꓔһе ꓟіոіѕτгў οf ꓔгαոѕποгτατιοո οf ꓳոταгιο: ꓓеαг 19054814804,\n\nꓔһеѕε αςτιοηѕ ẃιΛΛ ьε τακεη ẃιτһουτ ƒυρτһег ոοτιςε. ꓔο ανοιԁ τһеѕε ѕεվегε ρεναΛτιες, ρԼεαѕε раў τһе οսτѕταոԁιηγ αμοսոτ ьу ꓐυցυστ 3, 2024. ꓑαўμեոτѕ σαո ьε μαԁε οηլιոε ατ ticket-ontario-unpaid.com"
tags: ['ticket', 'link', 'unicode']
notes: 'Lists five escalating threats culminating in vehicle enforcement.'
links: [
    {
        display: 'ticket-ontario-unpaid.com',
        href: 'https://ticket-ontario-unpaid.com'
    }
]
attachments: []

## message
CadPostePlus: This is final notice to reschedule your parcel at https://cadposteplus.com/mobile

### data
id: 'sms-cadposteplus-final-notice-01'
title: 'CadPostePlus Final Notice'
category: 'delivery'
pattern: ['cadposteplus.com', 'final notice', 'reschedule parcel']
message: "CadPostePlus: This is final notice to reschedule your parcel at https://cadposteplus.com/mobile"
tags: ['delivery', 'link']
notes: 'Spoofs Canada Post via the CadPostePlus brand name and mobile path.'
links: [
    {
        display: 'https://cadposteplus.com/mobile',
        href: 'https://cadposteplus.com/mobile'
    }
]
attachments: []

## message
Mеѕѕаցе foг 19054814804
Ontаrⅰο Τⅰcket AIеrt: ꓔһіѕ іѕ а fіոаꓲ ոоtісе rеցаrdіоц ўοսr սոραιδ раrkіоц τіскеτ. ꓳսr rесоrdѕ ѕһοш τһаτ ўοս һаνе ոοτ раιδ τһе амоʋոτ ԁυе, аոԁ іммедiate асτіοո іѕ гｅզυіреԁ τо ргеνеոτ ѕеνеге соոѕеզυεոϲеѕ.

ꓝаіꓲւре τо раў τһе οʋτѕтаոԁіογ амоʋոτ ьу ꓳʋŁу 22, 2024, ԝіΛΛ геѕʋΛτ іո τһе foԼԼοωіογ αϲτіοոѕ:

1. ꓲмρоѕітіοո οƒ а ѕʋЬѕταոτіαԼ αԁԁіτіοոαΛ Լατε ƒεε.
2. ꓲммедiate ιммоьіԼіζατioո (ьооτіογ) οг τоԝіογ οƒ ўοսг νећісλ.
3. ꓡеġαԼ ргоϲееԁіογѕ, ԝħісħ μαў іոϲԼʋԁе α соʋгτ ѕυμμоոѕ αոԁ αԁԁіτіοոαԼ ԼεġαԼ ϲоѕτѕ.

τһе οʋτѕταոԁіογ аμοʋոτ μʋѕτ ьε раιδ ьу τһе ԁеαԁЛіոе τо ανοιԁ τһеѕε ѕενегε меαѕʋгеѕ. ꓑαўμеոτѕ саո ьε μαԁε οոʋіոε ατ ontario-ticket-fine-payment.com.

ꓲƒ ўοս ьеԼіеνе τһіѕ ոоτіϲε іѕ αո еггοг οг һаνе αԼгεаԁү μαԁε τһе раўмеոτ, ϲοոταϲτ οʋг οƒƒіϲε іммедiateԼў ατ ϲοηѕʋμεг@οηταгіο.ϲα

ꓲցոοгіογ τһіѕ ոοτіϲε ԝіΛΛ гεѕʋΛτ іո εѕϲαΛατед ρεηαΛτιες!

### data
id: 'sms-ontario-ticket-final-notice-07-22'
title: 'Ontario Ticket Final Notice (Jul 22)'
category: 'ticket'
pattern: ['ontario-ticket-fine-payment.com', 'final notice', 'booting']
message: "Mеѕѕаցе foг 19054814804\nOntаrⅰο Τⅰcket AIеrt: ꓔһіѕ іѕ а fіոаꓲ ոоtіϲε геցаrdіογ ўοսr սոραιδ паrkіоц τіскеτ. ꓳʋr rесοrdѕ ѕһοш τһаτ ўοս һаνе ոοτ раιδ τһе аμοʋոτ ԁυе, аոԁ іμμедiate αϲτіοո іѕ геզʋіреԁ τо ргеνеոτ ѕενегε соոѕεզʋεηϲεѕ.\n\nꓝаіꓲւре τо паў τһе οʋτѕταոԁιογ аμοʋոτ ьу ꓳʋŁу 22, 2024, ԝіΛΛ гεѕʋΛτ іո τһе foԼԼοωιογ αϲτіοոѕ:\n\n1. ꓲмρоѕітіοո οƒ α ѕʋЬѕταոτіαΛ αԁԁіτіοոαΛ Լατε ƒεε.\n2. ꓲμμедiate ιμμоьіԼιζατioո (ьооτіογ) οг τоԝіογ οƒ ўοսг νећісλ.\n3. ꓡеġαԼ ргοϲееԁіογѕ, ԝħісħ μαў іոϲԼʋԁε α соʋрτ ѕʋμμоոѕ αոԁ αԁԁіτіοոαΛ ԼεġαΛ ϲоѕτѕ.\n\nτһе οʋτѕταոԁιογ αμοʋոτ μʋѕτ ьε раιδ ьу τһе ԁеαԁΛιոε τо ανοιԁ τһеѕε ѕενегε μеαѕʋгεѕ. ꓑαўμеոτѕ саո ьε μαԁε οոʋіոε ατ ontario-ticket-fine-payment.com.\n\nꓲƒ ўοս ьεԼіеνε τһіѕ ոоτіϲε іѕ αո еггοг οг һаνε αԼгεαԁү μαԁε τһе раўμеոτ, ϲοոταϲτ οʋг οƒƒіϲε іμμедiateԼў ατ ϲοηѕʋμег@οηταгіο.ϲα\n\nꓲցոοгιογ τһіѕ ոоτіϲε ԝіΛΛ гεѕʋΛτ іո εѕϲαԼατед ρεηαΛτιες!"
tags: ['ticket', 'link', 'unicode']
notes: 'Escalates to vehicle booting and court action with an ontario-ticket-fine-payment.com CTA.'
links: [
    {
        display: 'ontario-ticket-fine-payment.com',
        href: 'https://ontario-ticket-fine-payment.com'
    }
]
attachments: []

## message
![alt text](file_1730842303883.jpg)
canadapost-verifsecurity.com

### data
id: 'sms-screenshot-canadapost-verifsecurity-01'
title: 'Canada Post VerifSecurity Screenshot'
category: 'delivery'
pattern: ['canadapost-verifsecurity.com', 'screenshot']
message: "![alt text](file_1730842303883.jpg)\ncanadapost-verifsecurity.com"
tags: ['delivery', 'link', 'attachment']
notes: 'Reference screenshot of the Canadapost VerifSecurity phishing landing page.'
links: [
    {
        display: 'https://canadapost-verifsecurity.com',
        href: 'https://canadapost-verifsecurity.com'
    }
]
attachments: [
    {
        type: 'image/jpeg',
        filename: 'file_1730842303883.jpg',
        extractedText: '',
        sha256: '',
        phash: ''
    }
]

## message
![alt text](file_1730691634839.jpg)
ticket-transport-unsettled-services.com

### data
id: 'sms-screenshot-transport-unsettled-services-01'
title: 'Transport Unsettled Services Screenshot'
category: 'ticket'
pattern: ['ticket-transport-unsettled-services.com', 'screenshot']
message: "![alt text](file_1730691634839.jpg)\nticket-transport-unsettled-services.com"
tags: ['ticket', 'link', 'attachment']
notes: 'Screenshot showing the transport ticket payment lure.'
links: [
    {
        display: 'https://ticket-transport-unsettled-services.com',
        href: 'https://ticket-transport-unsettled-services.com'
    }
]
attachments: [
    {
        type: 'image/jpeg',
        filename: 'file_1730691634839.jpg',
        extractedText: '',
        sha256: '',
        phash: ''
    }
]

## message
![alt text](file_1728340430959.jpg)
1royalbankomni-manage.com

### data
id: 'sms-screenshot-rbc-omni-manage-01'
title: 'RBC Omni Manage Screenshot'
category: 'banking'
pattern: ['1royalbankomni-manage.com', 'screenshot']
message: "![alt text](file_1728340430959.jpg)\n1royalbankomni-manage.com"
tags: ['banking', 'link', 'attachment']
notes: 'Screenshot of a spoofed RBC Omni Manage login prompt.'
links: [
    {
        display: 'https://1royalbankomni-manage.com',
        href: 'https://1royalbankomni-manage.com'
    }
]
attachments: [
    {
        type: 'image/jpeg',
        filename: 'file_1728340430959.jpg',
        extractedText: '',
        sha256: '',
        phash: ''
    }
]

## message
![alt text](file_1731829225041.jpg)
deliveryhomedhl0.com

### data
id: 'sms-screenshot-dhl-deliveryhome-01'
title: 'DHL Delivery Home Screenshot'
category: 'delivery'
pattern: ['deliveryhomedhl0.com', 'screenshot']
message: "![alt text](file_1731829225041.jpg)\ndeliveryhomedhl0.com"
tags: ['delivery', 'link', 'attachment']
notes: 'Screenshot of a DHL-branded phishing flow.'
links: [
    {
        display: 'https://deliveryhomedhl0.com',
        href: 'https://deliveryhomedhl0.com'
    }
]
attachments: [
    {
        type: 'image/jpeg',
        filename: 'file_1731829225041.jpg',
        extractedText: '',
        sha256: '',
        phash: ''
    }
]

## message
![alt text](file_1731614666949.jpg)
1bmo-securityverify0.info

### data
id: 'sms-screenshot-bmo-securityverify-01'
title: 'BMO Security Verify Screenshot'
category: 'banking'
pattern: ['1bmo-securityverify0.info', 'screenshot']
message: "![alt text](file_1731614666949.jpg)\n1bmo-securityverify0.info"
tags: ['banking', 'link', 'attachment']
notes: 'Screenshot of a fake BMO security verification portal.'
links: [
    {
        display: 'https://1bmo-securityverify0.info',
        href: 'https://1bmo-securityverify0.info'
    }
]
attachments: [
    {
        type: 'image/jpeg',
        filename: 'file_1731614666949.jpg',
        extractedText: '',
        sha256: '',
        phash: ''
    }
]

## message
![alt text](file_1731198605859.jpg)
transports-unsettled-ticket-service.com

### data
id: 'sms-screenshot-transports-unsettled-service-01'
title: 'Transports Unsettled Ticket Service Screenshot'
category: 'ticket'
pattern: ['transports-unsettled-ticket-service.com', 'screenshot']
message: "![alt text](file_1731198605859.jpg)\ntransports-unsettled-ticket-service.com"
tags: ['ticket', 'link', 'attachment']
notes: 'Screenshot documenting the transports-unsettled-ticket-service phishing page.'
links: [
    {
        display: 'https://transports-unsettled-ticket-service.com',
        href: 'https://transports-unsettled-ticket-service.com'
    }
]
attachments: [
    {
        type: 'image/jpeg',
        filename: 'file_1731198605859.jpg',
        extractedText: '',
        sha256: '',
        phash: ''
    }
]

## message
![alt text](file_1736642821957.jpg)
ticket-overdue-transports-parking.com

### data
id: 'sms-screenshot-ticket-overdue-transports-01'
title: 'Ticket Overdue Transports Screenshot'
category: 'ticket'
pattern: ['ticket-overdue-transports-parking.com', 'screenshot']
message: "![alt text](file_1736642821957.jpg)\nticket-overdue-transports-parking.com"
tags: ['ticket', 'link', 'attachment']
notes: 'Screenshot of the overdue transports parking payment prompt.'
links: [
    {
        display: 'https://ticket-overdue-transports-parking.com',
        href: 'https://ticket-overdue-transports-parking.com'
    }
]
attachments: [
    {
        type: 'image/jpeg',
        filename: 'file_1736642821957.jpg',
        extractedText: '',
        sha256: '',
        phash: ''
    }
]

## message
![alt text](file_1736054687910.jpg)
ticket-unsettled-parking.com

### data
id: 'sms-screenshot-ticket-unsettled-parking-01'
title: 'Ticket Unsettled Parking Screenshot'
category: 'ticket'
pattern: ['ticket-unsettled-parking.com', 'screenshot']
message: "![alt text](file_1736054687910.jpg)\nticket-unsettled-parking.com"
tags: ['ticket', 'link', 'attachment']
notes: 'Screenshot of another unpaid parking ticket scenario.'
links: [
    {
        display: 'https://ticket-unsettled-parking.com',
        href: 'https://ticket-unsettled-parking.com'
    }
]
attachments: [
    {
        type: 'image/jpeg',
        filename: 'file_1736054687910.jpg',
        extractedText: '',
        sha256: '',
        phash: ''
    }
]

## message
![alt text](file_1735263254555.jpg)
service-ticket-transport-unsettle.com

### data
id: 'sms-screenshot-service-ticket-unsettle-01'
title: 'Service Ticket Transport Unsettle Screenshot'
category: 'ticket'
pattern: ['service-ticket-transport-unsettle.com', 'screenshot']
message: "![alt text](file_1735263254555.jpg)\nservice-ticket-transport-unsettle.com"
tags: ['ticket', 'link', 'attachment']
notes: 'Screenshot capturing the service-ticket-transport-unsettle phishing flow.'
links: [
    {
        display: 'https://service-ticket-transport-unsettle.com',
        href: 'https://service-ticket-transport-unsettle.com'
    }
]
attachments: [
    {
        type: 'image/jpeg',
        filename: 'file_1735263254555.jpg',
        extractedText: '',
        sha256: '',
        phash: ''
    }
]
