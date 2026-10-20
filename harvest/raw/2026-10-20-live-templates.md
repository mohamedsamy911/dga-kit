# Raw capture — DGA's rendered Service and e-Participation templates, 2026-10-20

The Assessment Checklist asks for the service page's *"same terms and headings, such as: Steps,
Requirements, Required Documents, Service Details Card, and others, without any modification"*
(item 8), and for *"the 8 main sections as per the template"* on e-Participation (item 9). The
template guideline pages do not list those headings in text: they show the template as an image.
DGA's site also serves templates as live pages; this file records two.

**Method.** The live build (`index-BO_6JOKP.js`, sha256
`4b8aa21d37ab66d281ec1a1ff2dacfe3e911b2d7296a9c5ea89e668c18af0340`) routes `/templates/*` to
rendered templates. `https://design.dga.gov.sa/templates/service` and
`https://design.dga.gov.sa/templates/e-participation` were opened in a browser on 2026-10-20, once
with the site language set to English and once to Arabic (`localStorage` `i18nextLng`), and the
displayed text and `h1`–`h4` headings were read. Only text that was displayed is recorded; the
build also carries strings these pages did not show (below).

## `/templates/service`

| Part | English (displayed) | Arabic (displayed) |
|---|---|---|
| Example title | Building premit | رخصة بناء |
| Tags | Ministry · Life experience · Related platform | الجهة · رحلة الحياة · المنصة |
| Link under the description | Service Level Agreement | اتفاقية مستوى الخدمة |
| Tabs | **Steps** · **Conditions** · **Required Documents** | **الخطوات** · **شروط الاستخدام** · **المستندات المطلوبة** |
| Service card labels | Target audience · Service duration · Service channels · Service cost | الفئة المستهدفة · مدة الخدمة · قنوات الخدمة · تكلفة الخدمة |
| Further card labels | Payment channels · Frequently Asked Questions · Phone · Email · Mobile Application | قنوات الدفع · الاسئلة الشائعة · الهاتف · البريد الالكتروني · تطبيقات الجوال |
| Section | Related Services | خدمات ذات صلة |
| Card | Comments & suggestions | التعليقات والاقتراحات |
| Page end | Last Modified Date: … · Was this page useful? | تاريخ آخر تعديل: … · هل كانت هذه الصفحة مفيدة؟ |

The steps are numbered example text about a building permit. "premit" is DGA's spelling.

The build's `service` strings also include an action, "Get Started " / «بدء الخدمة», and
"Download user guide" / «تحميل دليل المستخدم». Neither was displayed on the rendered page.

## `/templates/e-participation`

Under the `h1` "Engagement Topics" / «مواضيع المشاركة», eight `h2` sections, in this order:

| # | English | Arabic (as displayed) |
|---|---|---|
| 1 | e-Participation Policy | سياسة المشاركة الإكترونية |
| 2 | Consultations | الإستشارات الإلكترونية |
| 3 | Co-Creation and Ideas | التطوير المشترك والافكار |
| 4 | Open Data | البيانات المفتوحة |
| 5 | Complaints and Suggestions | الشكاوى والمقترحات |
| 6 | Beneficiary Voice Reports | تقارير صوت المستفيد |
| 7 | Website and Services Statistics | إحصائيات الموقع والخدمات |
| 8 | Social Media | وسائل التواصل الاجتماعي |

## Observations

1. **Item 8 and the template differ on one heading.** The checklist names *"Requirements"* /
   «الشروط»; the rendered template's second tab is "Conditions" / «شروط الاستخدام». «شروط
   الاستخدام» usually means *terms of use*.
2. **Arabic spelling.** Section 1 reads «سياسة المشاركة الإكترونية», without the «ل» of
   «الإلكترونية»; section 2 spells it «الإلكترونية».
3. The checklist's *"Service Details Card"* has no displayed title on the rendered page; the card
   holds the labels above.
