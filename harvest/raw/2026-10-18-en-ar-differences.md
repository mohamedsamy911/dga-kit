# Raw capture — where DGA’s Arabic and English pages differ, 2026-10-18

Evidence for the "Where DGA’s Arabic pages differ from its English" table in content.md. Each pair is
the same key from the English and Arabic i18n tables in DGA’s live bundle `assets/index-BO_6JOKP.js`,
verbatim with markup stripped (which is why some Arabic lines lose an element name; the rendered
Arabic page loses it too). Every Arabic passage was confirmed displayed on the rendered Arabic page
(language set to `ar`) in a browser on 2026-10-18; the English ones on the English page. Found by
pairing all 743 DGA sentences with a normative English word and reading both languages (Codex and
agy independently), plus a number-by-number comparison of all 6,182 shared keys.

---

## `/guidelines/components/loading-and-status/skeleton` — `skeleton.Variants_list.0.desc`

English:

<!-- dga -->
> Displays a circular placeholder typically used for profile pictures, icons, or logos in user interfaces. With multiple size options between 24px to 240px to fit different layouts.
<!-- /dga -->

Arabic:

<!-- dga -->
> تُستخدم كعنصر دائري مؤقت لعرض صور الملفات الشخصية، الأيقونات، أو الشعارات في واجهات المستخدم. تتوفر بأحجام متعددة بين 24px إلى 48px لتتناسب مع مختلف التخطيطات.
<!-- /dga -->

---

## `/guidelines/templates/search-page` — `templatesObj.search.section7.list.0.desc`

English:

<!-- dga -->
> It is a means to organize and display links when there is a large amount of data or links that cannot be displayed on a single page.Pagination should be placed at the bottom of the content list so that the user can access it after browsing through the 10 available items. The page the user is currently on should be clearly highlighted, helping the user understand their current position within the page sequence. "Next" and "Previous" buttons (arrows) should be included to allow the user to quickly navigate between adjacent pages, providing a better user experience, especially if they don’t wish to jump to a distant specific page.
<!-- /dga -->

Arabic:

<!-- dga -->
> هو وسيلة لتنظيم وعرض المحتوى عندما يكون هناك كمية كبيرة من البيانات أو العناصر التي لا يمكن عرضها على صفحة واحدة. يجب وضع ترقيم الصفحات في الجزء السفلي من قائمة المحتوى بحيث يصل إليه المستخدم بعد تصفح جميع العناصر المتاحة في الصفحة الحالية. ويمكن أيضًا إضافة ترقيم الصفحات في أعلى الصفحة إذا كانت القائمة طويلة جدًا، مما يمنح المستخدمين خيار التنقل دون الحاجة إلى التمرير للأسفل. الصفحة التي يتواجد فيها المستخدم حاليًا يجب أن تكون مميزة بوضوح. هذا يساعد المستخدم على معرفة مكانه الحالي ضمن تسلسل الصفحات. يجب تضمين أزرار (أسهم) "التالي" و"السابق" للسماح للمستخدم بالتنقل بسرعة بين الصفحات المجاورة، مما يوفر تجربة مستخدم أفضل خاصة إذا كان لا يريد الانتقال لصفحة محددة بعيدة.
<!-- /dga -->

---

## `/guidelines/foundations/typography` — `typo.Using_Saudi_Font_in_Platform_Code_desc`

English:

<!-- dga -->
> Saudi Font is reserved exclusively for national and seasonal occasions, such as National Day and Founding Day. It should be limited to main headings only. Using the font in paragraph text or long-form content is not recommended, in order to maintain readability and ease of browsing.
<!-- /dga -->

Arabic:

<!-- dga -->
> يُخصَّص الخط السعودي للاستخدام في المناسبات الوطنية والموسمية فقط، مثل اليوم الوطني ويوم التأسيس وغيرها، على أن يقتصر استخدامه على العناوين الرئيسية فقط. ويُحظر استخدام الخط في نصوص الفقرات أو المحتوى الطويل؛ وذلك حفاظًا على وضوح المقروئية وسهولة التصفح.
<!-- /dga -->

---

## `/guidelines/components/actions/dropdown` — `drop.Focus_Management_desc`

English:

<!-- dga -->
> When the dropdown opens, focus should typically be moved to the currently selected option, if any, or the first option otherwise.
<!-- /dga -->

Arabic:

<!-- dga -->
> عند فتح القائمة المنسدلة يجب نقل التركيز إلى الخيار المحدد حاليًا إن وجد، أو الخيار الأول.
<!-- /dga -->

---

## `/guidelines/components/feedback/tooltip` — `tooltip.Accessibility_list.value4`

English:

<!-- dga -->
> Use aria-describedby on the element that triggers the tooltip, pointing to the ID of the tooltip container. This attribute should be dynamically added when the tooltip is visible and removed when it is not. <button aria-describedby="tooltip1">Info</button> <div role="tooltip" id="tooltip1" style="display:none;">More information here</div>
<!-- /dga -->

Arabic:

<!-- dga -->
> استخدم aria-description على العنصر الذي يشغل حافة التلميح مع الإشارة إلى معرف حاوية حافة التلميح. يجب إضافة هذه السمة ديناميكيًا عندما يكون طرف التلميح مرئيًا وإزالته عندما لا يكون كذلك. <button aria-describedby="tooltip1">Info</button> <div role="tooltip" id="tooltip1" style="display:none;">للمزيد من المعلومات هنا</div>
<!-- /dga -->

---

## `/guidelines/components/feedback/tooltip` — `tooltip.Accessibility_list.value5`

English:

<!-- dga -->
> Tooltips should only appear on hover or focus and disappear when focus and hover are removed. Ensure they do not cover other interactive elements and are positioned close to the element they describe.
<!-- /dga -->

Arabic:

<!-- dga -->
> ضع في الاعتبار إضافة تأخير طفيف قبل إظهار وإخفاء حافة التلميح لمنعها من الظهور بسرعة كبيرة أو بشكل متكرر. التأكد من عدم تغطيتها لعناصر تفاعلية أخرى ووضعها بالقرب من العنصر الذي تريد وصفه.
<!-- /dga -->

---

## `/guidelines/components/forms-and-inputs/input` — `input.Accessibility_list.5`

English:

<!-- dga -->
> Use aria-describedby to link any additional descriptive text or error messages to the input, helping users understand constraints or corrections. &ltinput type="text" id="username" aria-describedby="usernameHelp"> &ltsmall id="usernameHelp">Your username must be 8-20 characters long.&lt/small>
<!-- /dga -->

Arabic:

<!-- dga -->
> استخدم "aria-describe" لربط أي نص وصفي إضافي أو في الرسائل التي تشير إلى خطأ بالمدخل، مما يساعد المستخدمين على فهم القيود أو التصحيحات. يجب أن يكون اسم المستخدم الخاص بك من 8-20 حرف
<!-- /dga -->

---

## `/guidelines/components/search-and-filters/tags` — `tags.Accessibility_list.4`

English:

<!-- dga -->
> Interactive tags should be marked up as &ltbutton> when they perform an action (like removing a tag). This automatically provides keyboard accessibility and the correct semantic role.
<!-- /dga -->

Arabic:

<!-- dga -->
> يعمل بشكل تلقائي على توفير إمكانية الوصول إلى لوحة المفاتيح والدور الدلالي الصحيح.
<!-- /dga -->

---

## `/guidelines/components/navigational/breadcrumbs` — `breadcrumb.Variants_States_desc`

English:

<!-- dga -->
> Breadcrumbs have seven states for items — enabled, hover, active, focus, visited, disabled, and read-only.
<!-- /dga -->

Arabic:

<!-- dga -->
> يحتوي مسار التصفح على سبع حالات للعناصر — المفعلة، التمرير، التركيز، تم زيارته، المعطل، والقابل للقراءة فقط.
<!-- /dga -->
