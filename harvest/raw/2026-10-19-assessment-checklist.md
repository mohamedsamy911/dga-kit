# Raw capture — DGA Assessment Checklist (قائمة التحقق لتطبيق نظام التصميم الموحد)

**Source:** https://design.dga.gov.sa/assets/updated-checkList.xlsx — the file behind the
**Download Checklist** buttons on `/AssessmentCriteria`, `/designing` and `/developing` (the
bundle calls `"/assets/updated-checkList.xlsx"` and saves it as
`قائمة التحقق لتطبيق التصميم الموحد.xlsx`). The browser shows a `blob:` URL; that is a local
object URL, not the source.

**Retrieved:** 2026-10-19, twice: downloaded by the owner in a browser, and fetched by `curl` from
the asset URL. Both copies are byte-identical.

| Property | Value |
|---|---|
| sha256 | `117d10c52ea5767bc3cad75bb2f4fce276323c0413885b8a73ec076674248075` |
| Size | 59,394 bytes |
| HTTP `Last-Modified` | Sun, 20 Sep 2026 12:31:10 GMT |
| Workbook properties | created 2025-06-03, last saved 2025-07-15 |
| Sheet | one sheet, `Sheet1` |

**Layout of the sheet (kit's description):** header rows ask for the entity name, platform name
and platform link. Columns: الاولوية (priority group) · رقم (number) · المعايير (criterion,
Arabic) · Criteria (English) · حالة التنفيذ (implementation status) · المرجع (reference) ·
توضيح إضافي · رابط ملفات وصور داعمه · ملاحظات. The status column is empty and offers a dropdown of
four values: `تطبيق كلي`, `تطبيق جزئي`, `غير مطبق`, `N/A لاينطبق`. A colour legend in the header
names four categories — اساسات, قوالب, عناصر, التجربة — applied as row fills; the fills are not
transcribed here.

**Counts:** 56 numbered criteria. Rows 1–43 sit under **المعايير الأساسية**, rows 44–56 under
**المعايير الثانوية**. The workbook does not map these two groups to the Mandatory / Recommended /
Optional levels on the `/AssessmentCriteria` page, and this kit does not either.

**Method:** every cell below is copied from the workbook by `openpyxl` (cached values), in sheet
order. Each fenced passage is one row: the Arabic cell, then DGA's own English cell. A numbered
criterion is followed by its unnumbered sub-rows. The "Reference column" lines are the
المرجع cells, outside the fences because they are URLs, not prose.

## المعايير الأساسية

### 1

<!-- dga -->
> التأكد من تطبيق النسخة 1.0 من نظام التصميم الموحد (كود المنصات)
>
> Ensure the Unified Design System (Platforms Code) version 1.0 is correctly implemented
<!-- /dga -->

Reference column: https://design.dga.gov.sa/

### 2

<!-- dga -->
> التأكد من استخدام الألوان المعتمدة كما في نظام التصميم الموحد (كود المنصات)
>
> Ensure the use of approved colors as defined in the Unified Design System (Platforms Code)
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/foundations/color-system

<!-- dga -->
> الالتزام باستخدام رموز ألوان التصميم (Color Design Tokens) مثل الألوان المخصصة للخلفيات، والخطوط، وغيرها، دون تعديل أو استبدال.
>
> Ensure adherence to the designated color design tokens (e.g., background, text colors, etc.) without any modifications or replacements.
<!-- /dga -->

<!-- dga -->
> في حال إضافة عناصر على خلفيات ملونة يجب التحقق من أنها تحقق متطلبات التباين والوضوح المطلوبة لضمان سهولة الاستخدام والوصولية من خلال استخدام خاصية On Color الموجودة في العناصر .
>
> Ensure that any elements placed on colored backgrounds meet the required contrast and clarity standards for usability and accessibility, by applying the On Color property provided in the component.
<!-- /dga -->
Reference column: https://webaim.org/resources/contrastchecker/ · https://www.figma.com/community/plugin/748533339900865323

### 3

<!-- dga -->
> تأكد من الالتزام باستخدام الخطوط المعتمدة، وأوزان الخطوط للعناوين، وإجراءات الخطوط سريعة الاستجابة
>
> Adhere to Typography guidelines by using approved fonts, appropriate font weights for headings, and responsive typography measures
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/foundations/typography

<!-- dga -->
> استخدام الخط المعتمد IBM Plex Sans Arabic كما هو محدد في كود المنصات.
>
> Use the approved font: IBM Plex Sans Arabic, as specified in the Platforms Code.
<!-- /dga -->

<!-- dga -->
> تطبيق متغيرات الخط الصحيحة حسب رموز خطوط التصميم (Typography Design Tokens) المخصصة: 
> - لمتغيرات العرض (Display).
> - لمتغيرات النصوص (Text).
>
> Apply the correct typography variables based on the designated Typography Design Tokens, including:
> - Display variants
> - Text variants
<!-- /dga -->

### 4

<!-- dga -->
> التأكد من تطبيق ارقام المسافات على الصفحة كما في نظام التصميم الموحد (كود المنصات)
>
> Ensure spacing values are applied according to the Unified Design System (Platforms Code)
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/foundations/layout-and-spacing

<!-- dga -->
> الالتزام بوحدات القياس المعتمدة في كود المنصات (مثل 4px، 8px، 16px...) عند تحديد المسافات بين العناصر.
>
> Adhere to the approved spacing units defined in the Platforms Code (such as 4px, 8px, 16px...) when setting spacing between elements.
<!-- /dga -->

<!-- dga -->
> الالتزام باستخدام رموز المسافات للتصميم (Global Spacing Design Tokens). مع الالتزام بعدم استخدام المسافات المخصصة للعناصر.
>
> Use only the Global spacing design tokens, as defined in the system.
<!-- /dga -->

### 5

<!-- dga -->
> التأكد من أن التصميم يتكيف بشكل فعال مع أحجام واتجاهات الشاشات المختلفة لتوفير تجربة سلسة عبر الأجهزة
>
> Ensure responsive design that adapts effectively to different screen sizes and orientations to provide a seamless experience across devices
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/foundations/layout-and-spacing

<!-- dga -->
> التصميم متجاوب ويعيد ترتيب الأعمدة والمكونات تلقائيًا حسب حجم الشاشة (Mobile, Tablet, Desktop) بناءً على الإرشادات المعتمدة.
>
> The layout must be responsive and automatically rearrange columns and components based on screen size (Mobile, Tablet, Desktop) following the approved guidelines.
<!-- /dga -->

<!-- dga -->
> التأكد من أن التطبيق/الموقع قابل للاستخدام بالكامل على الأجهزة المحمولة، مع الأخذ في الاعتبار عوامل مثل تفاعلات اللمس، وحجم إطار العرض، والوصول إلى التنقل على الشاشات الصغيرة.
>
> The application/website must be fully usable on mobile devices, considering factors like touch interactions, viewport size, and navigation accessibility.
<!-- /dga -->
Reference column: https://design.dga.gov.sa/thoughts/responsive-design

### 6

<!-- dga -->
> ضمان استخدام الأيقونات المعتمدة وفق نظام التصميم الموحد (كود المنصات)
>
> Ensure usage of approved icons as per the Unified Design System (Code of Platforms)
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/foundations/iconography

<!-- dga -->
> الالتزام باستخدام مكتبة الأيقونات في كود المنصات دون استبدال أو تعديل في الحجم أو اللون.
>
> Only use icons from the official icon library without any changes to size or color.
<!-- /dga -->

<!-- dga -->
> يتم استخدام الأيقونات في حالتين:
> - الاستخدامات التنبيهية:
> تُستخدم في هذه الحالات الأيقونات ذات الألوان التنبيهية المعتمدة (نجاح، فشل، تحذير، معلومة) حصرًا للحالات التي تتطلب لفت انتباه المستخدم، مثل: حالات النجاح، الأخطاء، التحذيرات، أو أثناء المعالجة.
> - الاستخدامات العامة وتصنيف المحتوى:
> يُستخدم في هذه الحالات أيقونات بألوان محايدة أو ألوان أساسية مثل الرمادي أو الأخضر، ويُمنع استخدام الألوان التنبيهية لأغراض غير التنبيه.
>
> Icons are used in two cases:
> - Status Icons:
> Icons with the approved status colors (success, error, warning, information) are used exclusively for situations that require drawing the user's attention, such as success messages, errors, warnings, or processing states.
> - General Use and Content Classification:
> In these cases, icons should use neutral or primary colors, such as gray or green. Status colors must not be used for non-status purposes.
<!-- /dga -->

<!-- dga -->
> في حال الاحتياج لأيقونات أكبر من 24px يجب أن يتم استخدام أيقونة مميزة (Featured icon) وتجنب تغيير ألوان وأحجام متغيراتها.
>
> For icons larger than 24px, use the "Featured icon" variant without modifying its colors or sizes.
<!-- /dga -->

<!-- dga -->
> في حال عدم وجود أيقونة تناسب الاحتياج من مكتبة الأيقونات، يجب تصميم العنصر حسب إرشادات الأيقونات، ورفع طلب للموافقة من الرابط المضمن في المرجع يسارًا في الاكسل.
>
> If no suitable icon is available in the icon library to meet the need, a custom icon must be designed in accordance with the icon design guidelines. A request for approval should then be submitted using the link provided in the reference.
<!-- /dga -->
Reference column: https://survey.dga.gov.sa/survey/start/91ed577e-38dd-4181-9d12-1b91b4456c94

### 7

<!-- dga -->
> التأكد من تطبيق قالب الصفحة الرئيسية بما يتناسب مع المنصة
>
> Ensure the homepage template is applied according to the platform
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/templates/home-page

<!-- dga -->
> الالتزام بالقسم الرئيسي واستخدام أحد أنواعه المعتمدة في Figma، سواء كانت صورة، خلفية لونية، أو كائن (Object).
>
> Adhere to using the hero section and apply one of its approved types in Figma, whether it is an image, a colored background, or an object.
<!-- /dga -->

<!-- dga -->
> في حال كانت المنصة معلوماتية فيجب أن يكون قسم الأخبار أو المعلومات هو أول قسم يراه المستخدم بعد القسم الرئيسي.
>
> For informational platforms, include a news or info section directly below the hero section.
<!-- /dga -->

<!-- dga -->
> في حال كانت المنصة خدماتية فيجب أن يكون قسم الخدمات هو أول قسم يراه المستخدم بعد القسم الرئيسي.
>
> For service platforms, include a services section directly below the hero section.
<!-- /dga -->

<!-- dga -->
> في حال وجود أقسام مقاربة للموجود في القالب من ناحية الإجراء مثل (قسم الشركاء) فيجب الالتزام بالقسم الموجود في كود المنصات.
>
> For sections similar to template actions (e.g., partners), use the standardized design.
<!-- /dga -->

<!-- dga -->
> عند تصميم أقسام جديدة غير موجودة في القالب، فيجب الالتزام باستخدام الأساسات والعناصر المعتمدة في كود المنصات (كالألوان، والخطوط، والأزرار، وغيرها).
>
> For new sections, use the approved foundations (colors, fonts, buttons, etc.).
<!-- /dga -->

### 8

<!-- dga -->
> التأكد من تطبيق قالب صفحة الخدمة
>
> Ensure the service page template is applied
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/templates/service-page

<!-- dga -->
> الالتزام الكامل بقالب صفحة الخدمة المعتمد، بما في ذلك استخدام نفس المصطلحات والعناوين مثل: الخطوات، الشروط، و المستندات المطلوبة و بطاقة تفاصيل الخدمة وغيرها، دون تعديل أو تغيير.
>
> Full adherence to the approved service page template is required, including the use of the same terms and headings, such as: Steps, Requirements, Required Documents, Service Details Card, and others, without any modification or changes.
<!-- /dga -->

<!-- dga -->
> تطبيق عنصر التقييم بجميع مكوناته كما هو معتمد في كود المنصات، دون أي تعديل على خصائصه أو سلوكياته.
>
> Apply the feedback component in full accordance with the Platforms Code specifications, maintaining all defined properties and behaviors without alterations.
<!-- /dga -->
Reference column: https://design.dga.gov.sa/guidelines/templates/rating-section

<!-- dga -->
> تطبيق عنصر التغذية الراجعة بجميع مكوناته كما هو معتمد في كود المنصات، دون أي تعديل على خصائصه أو سلوكياته.
>
> Apply the feedback component in full accordance with the Platforms Code specifications, maintaining all defined properties and behaviors without alterations.
<!-- /dga -->
Reference column: https://design.dga.gov.sa/guidelines/templates/feedback-section

### 9

<!-- dga -->
> التأكد من تطبيق قالب المشاركة الإلكترونية
>
> Ensure the e-Participation template is applied
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/templates/e-participation-page

<!-- dga -->
> الالتزام بقالب الصفحة الرئيسية للمشاركة الالكترونية بالأقسام الـ8 كما هي موجودة.
>
> Follow the 8 main sections as per the template.
<!-- /dga -->

<!-- dga -->
> في حال عدم وجود صفحات فرعية للمشاركة الإلكترونية، يمكن استخدام الروابط الموجودة في الأقسام. (للمزيد من التوضيح، يُرجى الاطلاع على الإرشادات الموجودة في القالب).
>
> If there are no subpages for e-participation, the links available in the sections may be used. (For further clarification, please refer to the guidelines provided in the template.)
<!-- /dga -->

### 10

<!-- dga -->
> التأكد من تطبيق قالب البحث
>
> Ensure the search template is applied
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/templates/search-page

<!-- dga -->
> الالتزام بقالب البحث كما هو موجود في مكتبة كود المنصات في Figma.
>
> Use the search template from the Code of Platforms in Figma.
<!-- /dga -->

<!-- dga -->
> توفر شريط البحث في صفحة النتائج.
>
> A search bar must be available on the results page.
<!-- /dga -->

<!-- dga -->
> فعالية وكفاءة وظيفة البحث، بما في ذلك مدى ملاءمة نتائج البحث وسرعتها.
>
> Ensure effectiveness and efficiency of the search (result relevance and speed).
<!-- /dga -->

<!-- dga -->
> عرض النتائج بشكل منظم حسب التصنيفات المعتمدة في المنصة (أخبار، خدمات، مقالات، إلخ...) مع إتاحة إمكانية تحديد النتائج وفق معايير يختارها المستخدم، مثل نوع المحتوى أو تاريخ النشر، لتسهيل الوصول إلى المعلومات المطلوبة بدقة.
>
> Display the results in an organized manner based on the platform’s predefined categories (such as News, Services, Articles, etc.). Allow users to filter the results using selectable criteria, like content type or publication date, to help them quickly and accurately find the information they need.
<!-- /dga -->

### 11

<!-- dga -->
> التأكد من تطبيق عنصر الختم الرقمي مع معايير التصميم الموحد (كود المنصات)
>
> Ensure digital stamp follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/content-display/digital-stamp

<!-- dga -->
> يجب وضع الختم في أعلى الصفحة.
>
> The stamp must be placed at the top of the page.
<!-- /dga -->

<!-- dga -->
> التأكد من ربط رقم الشهادة بالصفحة الخاصة بها بشكل صحيح.
>
> Verify that the certificate number is correctly linked to its corresponding certificate page.
<!-- /dga -->

<!-- dga -->
> يمكن إضافة عناصر ثانوية (مثل أزرار أو روابط) كخيارات للمشاركة أو أدوات لإمكانية الوصول، على الجانب الأيسر من الختم، مع الالتزام بعدم تجاوز عنصرين كحد أقصى.
>
> Secondary elements (such as buttons or links) for options like sharing or accessibility tools may be added to the left side of the stamp, with a maximum of two secondary elements allowed.
<!-- /dga -->

### 12

<!-- dga -->
> ضمان توافق عنصر الزر مع معايير التصميم الموحد (كود المنصات)
>
> Ensure Buttons follow the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/actions/buttons

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر (Default, Hovered, Pressed, Selected, Focused, Disabled)  كما هو معتمد في كود المنصات.
>
> Apply the component states (Default, Hovered, Pressed, Selected, Focused, Disabled) exactly as specified in the Platforms Code.
<!-- /dga -->

### 13

<!-- dga -->
> ضمان توافق عنصر القائمة المنسدلة مع معايير التصميم الموحد (كود المنصات)
>
> Ensure Dropdown Input follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/actions/dropdown

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي، إلا لزيادة عناصر خيارات القائمة (Dropdown List Item).
>
> Use the component as defined in the Platforms Code in terms of properties (shape, border-radius, color, spacing, etc.) without modifying the original design, except for adding Dropdown List Items.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر (Default, Hovered, Pressed, Focused, Read-only, Disabled) كما هو معتمد في كود المنصات.
>
> Apply component states (Default, Hovered, Pressed, Focused, Read-only, Disabled) as specified in the Platforms Code.
<!-- /dga -->

### 14

<!-- dga -->
> التحقق من أن عنصر الرابط يتماشى مع نظام التصميم الموحد (كود المنصات)
>
> Ensure Link follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/actions/link

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر (Default, Hovered, Pressed, Focused, Visited, Disabled) كما هو معتمد في كود المنصات.
>
> Apply link states (Default, Hovered, Pressed, Focused, Visited, Disabled) as defined in the Platforms Code.
<!-- /dga -->

<!-- dga -->
> في حال وجود رابط خارجي يجب أن تتواجد ايقونة (External link) مع الرابط.
>
> If the link leads to an external page, an external link icon (Link Square) must be included with it.
<!-- /dga -->

### 15

<!-- dga -->
> التأكد من استخدام عنصر الأكورديون وفقًا لمبادئ التصميم الموحد (كود المنصات)
>
> Ensure Accordions follow the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/content-display/accordion

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Pressed, Focused, Disabled) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Hovered, Pressed, Focused, Disabled) as defined in the Platforms Code.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (Expanded / Collapsed) كما هو معتمد في كود المنصات.
>
> Apply contextual states (Expanded / Collapsed) as defined in the Platforms Code.
<!-- /dga -->

### 16

<!-- dga -->
> ضمان توافق عنصر القائمة مع إرشادات التصميم الموحد (كود المنصات)
>
> Ensure Menu follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/navigational/menu

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined without modifications to properties such as shape, color, spacing, etc.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Pressed, Focused, Disabled) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Hovered, Pressed, Focused, Disabled) as defined in the Platforms Code.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (Selected) كما هو معتمد في كود المنصات.
>
> Apply contextual states (Selected) as defined in the Platforms Code.
<!-- /dga -->

### 17

<!-- dga -->
> التأكد من استخدام عنصر مبدل المحتوى بما يتماشى مع نظام التصميم الموحد (كود المنصات)
>
> Ensure Content Switcher follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/data-display/content-switcher

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Normal, Hovered, Focused) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Normal, Hovered, Focused) as defined in the Platforms Code.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (Selected) كما هو معتمد في كود المنصات.
>
> Apply contextual states (Selected) as defined in the Platforms Code.
<!-- /dga -->

### 18

<!-- dga -->
> ضمان أن عنصر الإشعارات يلتزم بمبادئ التصميم الموحد (كود المنصات)
>
> Ensure Notifications follow the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/feedback/notification

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> في حال كان الإشعار مؤقت في الواجهة، يجب استخدام الإشعارات المنبثقة (Notification Toast).
>
> If the notification is temporary, use Notification Toasts.
<!-- /dga -->

<!-- dga -->
> في حال كان الإشعار دائم، يجب استخدام الإشعارات المدمجة (Inline Alert).
>
> If the notification is permanent, use Inline Alerts.
<!-- /dga -->

<!-- dga -->
> في حال كان الاشعار دائم وله أولوية عالية بتضمينه بداية الصفحة، فيجب استخدام إشعارات (Notification).
>
> For high-priority permanent alerts at the top of the page, use Notification.
<!-- /dga -->

<!-- dga -->
> استخدام الإشعارات في سياقها المحدد، (مثل: استخدام إشعارات النجاح، للإشارة إلى إتمام إجراء بنجاح).
>
> Use notifications in their appropriate context (e.g., success notifications should be used to indicate the successful completion of an action).
<!-- /dga -->

<!-- dga -->
> تطبيق سلوك الإشعار كما هو موصى به (مثل: قابلية الإغلاق للإشعارات القابلة للتفاعل).
>
> Follow recommended notification behavior (e.g., closeable interactive alerts).
<!-- /dga -->

### 19

<!-- dga -->
> التأكد من أن عنصر النوافذ المنبثقة يتماشى مع إرشادات التصميم الموحد (كود المنصات)
>
> Ensure Modals follow the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/feedback/modal

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تخصيص النافذة المنبثقة لتبسيط التفاعل بالنسبة للمهام التي تحتاج إلى تأكيد من المستخدم أو تقديم الملاحظات أو تنبيهات هامة وعدم استخدامها في إدخال بيانات بشكل تفصيلي كبير - في حال الاحتياج لإدخال بيانات كبيرة، الرجاء استخدام قالب النموذج
>
> Customize pop-up windows to simplify user interactions for tasks that require user confirmation, feedback, or important alerts. Avoid using pop-ups for detailed data entry — for extensive data input, please use the form template.
<!-- /dga -->

### 20

<!-- dga -->
> التأكد من توافق عنصر رفع الملفات مع مبادئ التصميم الموحد (كود المنصات)
>
> Ensure File Upload follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/forms-and-inputs/file-uploader

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Drag + hover, Disabled) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Drag + Hover, Disabled).
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (Uploaded / Not Uploaded) كما هو معتمد في كود المنصات.
>
> Apply contextual states (Uploaded / Not Uploaded).
<!-- /dga -->

<!-- dga -->
> عرض اسم الملف وصيغته، حالته (جارٍ التحميل، مكتمل، فشل)، والخيارات المصاحبة (الإزالة) بطريقة واضحة ومتوافقة مع كود المنصات.
>
> Display the file name, its status (Uploading, Completed, Failed), and the associated options (e.g., Remove) in a clear and platform-consistent manner.
<!-- /dga -->

<!-- dga -->
> وجود رسائل توجيهية أو تحذيرية واضحة في حال فشل التحميل أو تجاوز الحجم أو نوع الملف غير المدعوم. ومثال مساعد لطريقة معالجة الرسالة/التحذير.
>
> Provide clear instructional or warning messages in cases of upload failure, file size exceeding the limit, or unsupported file types. Include helpful examples or guidance on how to resolve the issue.
<!-- /dga -->

### 21

<!-- dga -->
> ضمان أن عنصر مربع الاختيار يتبع النظام التصميمي الموحد (كود المنصات)
>
> Ensure Checkbox follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/forms-and-inputs/checkbox

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Focused, Read-only, Disabled) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Hovered, Focused, Read-only, Disabled).
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (Checked / Unchecked / Indeterminate) كما هو معتمد في كود المنصات.
>
> Apply the contextual states (Checked / Unchecked / Indeterminate) as defined in the Platform Code.
<!-- /dga -->

### 22

<!-- dga -->
> ضمان أن عنصر زر الاختيار يتبع النظام التصميمي الموحد (كود المنصات)
>
> Ensure Radio follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/forms-and-inputs/radio

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Focused, Read-only, Disabled) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Hovered, Focused, Read-only, Disabled).
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (Selected / Unselected) كما هو معتمد في كود المنصات.
>
> Apply the contextual states (Selected / Unselected) as defined in the Platform Code.
<!-- /dga -->

### 23

<!-- dga -->
> التأكد من أن عنصر زر التبديل يتماشى مع معايير التصميم الموحد (كود المنصات)
>
> Ensure Switch follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/forms-and-inputs/switch

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Focused, Disabled) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Hovered, Focused, Disabled).
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (On / Off) كما هو معتمد في كود المنصات.
>
> Apply contextual states (On / Off).
<!-- /dga -->

### 24

<!-- dga -->
> التحقق من استخدام عنصر منطقة النص وفقًا لمبادئ التصميم الموحد (كود المنصات)
>
> Ensure Textarea follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/forms-and-inputs/textarea

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Pressed, Focused, Read-only, Disabled) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Hovered, Pressed, Focused, Read-only, Disabled).
<!-- /dga -->

<!-- dga -->
> دعم ظهور التلميحات (Placeholder) والنصوص المساعدة بشكل متناسق مع التصميم، مع وضوح رسائل الخطأ وطريقة معالجتها عند الحاجة.
>
> Support the consistent display of placeholders and helper texts in alignment with the design, ensuring error messages are clear and properly handled when necessary.
<!-- /dga -->

### 25

<!-- dga -->
> ضمان أن عنصر علامات التبويب يتماشى مع إرشادات التصميم الموحد (كود المنصات)
>
> Ensure Tabs follow the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/navigational/tabs

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Focused, Disabled) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Hovered, Focused, Disabled).
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (Selected / Unselected) كما هو معتمد في كود المنصات.
>
> Apply contextual states (Selected / Unselected).
<!-- /dga -->

<!-- dga -->
> وضوح نص التبويب من حيث الخط، الحجم، والمحاذاة، مع الحفاظ على توازن بصري بين جميع التبويبات.
>
> Ensure the tab labels are clear in terms of font, size, and alignment, while maintaining visual balance across all tabs.
<!-- /dga -->

### 26

<!-- dga -->
> التأكد من أن عنصر العلامات يتبع النظام التصميمي الموحد (كود المنصات)
>
> Ensure Tags follow the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/search-and-filters/tags

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> يتم استخدام العلامات في حالتين:
> - الاستخدامات التنبيهية:
> تُستخدم العلامات ذات الألوان التنبيهية المعتمدة (نجاح، فشل، تحذير، معلومة) حصرًا للحالات التي تتطلب لفت انتباه المستخدم، مثل: حالات النجاح، الأخطاء، التحذيرات، أو أثناء المعالجة.
> - الاستخدامات العامة وتصنيف المحتوى:
> يُستخدم في هذه الحالات علامات بألوان محايدة أو ألوان أساسية مثل الرمادي أو الأخضر، ويُمنع استخدام الألوان التنبيهية لأغراض غير التنبيه.
>
> Tags are used in two cases:
> - Status Tags:
> Tags with the approved status colors (success, error, warning, information) are used exclusively for situations that require drawing the user's attention, such as success messages, errors, warnings, or processing states.
> - General Use and Content Classification:
> In these cases, tags should use neutral or primary colors, such as gray or green. Status colors must not be used for non-status purposes.
<!-- /dga -->

### 27

<!-- dga -->
> ضمان استخدام عنصر التذييل بما يتماشى مع معايير التصميم الموحد (كود المنصات)
>
> Ensure Footer follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/ui-shell/footer

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تصنيف الروابط في التذييل ضمن مجموعات ذات عناوين عامة أو متخصصة، مثل: "روابط مهمة" أو "الدعم والمساعدة".
>
> Categorize footer links into organized groups with clear, general, or specialized headings, such as "Important Links" or "Support & Help."
<!-- /dga -->

<!-- dga -->
> احتواء التذييل على العناصر الإلزامية مثل الروابط الرسمية، شعارات الجهة، معلومات التواصل، وسياسات الخصوصية – وفق ما هو منصوص عليه في كود المنصات.
>
> Ensure the footer includes mandatory elements like official links, organization logos, contact information, and privacy policies, as specified in the Design System (Code of Platforms).
<!-- /dga -->

### 28

<!-- dga -->
> التأكد من استخدام عنصر البطاقة وفقاً لمعايير التصميم الموحد (كود المنصات)
>
> Ensure Cards follow the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/content-display/card

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hover, Focused, Disabled) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Hover, Focused, Disabled).
<!-- /dga -->

<!-- dga -->
> يُسمح بالتغيير لحالتين فقط (تغيير المحاذاة للعناصر الداخلية أو تغيير المساحات داخل البطاقة لخلق تباين مختلف في البطاقات المتعددة).
>
> Only two adjustments are allowed: alignment of internal elements or adjusting inner spacing to create visual contrast when displaying multiple cards.
<!-- /dga -->

<!-- dga -->
> تطبيق متغيرات التصميم المحددة (مثل أنماط البطاقة بأنواعها: بمحتوى، بصورة، بظل، بدون ظل...) وفق المتغيرات المعتمدة في كود المنصات.
>
> Apply the predefined design variations (e.g., card types: with content, with image, with shadow, without shadow) as defined in the Design System.
<!-- /dga -->

<!-- dga -->
> توفر أزرار إجرائية (CTA) على البطاقات الإجرائية (القابلة للنقر). وفي حال كان الغرض من البطاقة عرض معلومات فلا يُشترط إضافة أزرار إجرائية.
>
> Actionable cards (clickable cards) must include clear Call-To-Action (CTA) buttons. For informational cards, CTA buttons are optional.
<!-- /dga -->

### 29

<!-- dga -->
> التحقق من استخدام عنصر شريط التنقل العلوي وفقاً لمعايير التصميم الموحد (كود المنصات)
>
> Ensure Nav Header follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/ui-shell/navigation-header

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق الحالات التفاعلية للتبويبات والقوائم الفرعية (Default, Hovered, Pressed, Focused, Disabled) كما هو معتمد في كود المنصات.
>
> Apply tab and submenu states (Default, Hovered, Pressed, Focused, Disabled).
<!-- /dga -->

<!-- dga -->
> تطبيق الحالات السياقية (Selected) كما هو معتمد في كود المنصات.
>
> Apply the contextual states (Selected) as defined in the Design System (Code of Platforms).
<!-- /dga -->

<!-- dga -->
> استجابة شريط التنقل لجميع أحجام الشاشات والأجهزة، مع الحفاظ على قابلية الاستخدام وسهولة التنقل.
>
> Ensure the navigation bar is responsive across all screen sizes and devices, while maintaining usability and ease of navigation.
<!-- /dga -->

<!-- dga -->
> في حال وجود تبويبات/قوائم فرعية خارجية يجب أن تتواجد أيقونة (External link) داخل التبويبة/قوائم فرعية.
>
> For external tabs or submenus, an External Link icon must be clearly displayed within the respective tab or submenu.
<!-- /dga -->

### 30

<!-- dga -->
> التأكد من استخدام عنصر مسار التصفح بما يتماشى مع نظام التصميم الموحد (كود المنصات)
>
> Ensure Breadcrumb follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/navigational/breadcrumbs

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Pressed, Focused, Disabled) كما هو معتمد في كود المنصات.
> *ملاحظة: الصفحة الحالية تكون غير قابلة للنقر (Disabled) ولا تحتوي على حالات تفاعلية.
>
> Apply interactive states (Default, Hovered, Pressed, Focused, Disabled).  *Note: Current page should be disabled and non-interactive.
<!-- /dga -->

<!-- dga -->
> وضوح مسار التصفح وسهولة التفاعل معها على جميع الأجهزة، مع استجابة كاملة ومتوافقة مع المعايير.
>
> Ensure the breadcrumb is clearly visible and easy to interact with across all devices, providing full responsiveness and alignment with accessibility standards.
<!-- /dga -->

<!-- dga -->
> اتساق مسار التصفح مع التسلسل الهيكلي لخريطة الموقع لضمان دقة التوجيه والتنقل.
>
> Maintain consistency between the breadcrumb and the hierarchical structure of the sitemap to ensure accurate navigation and user guidance.
<!-- /dga -->

### 31

<!-- dga -->
> التأكد من توافق عنصر الصورة الرمزية مع نظام التصميم الموحد (كود المنصات)
>
> Ensure Avatar follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/data-display/avatar

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> الالتزام بأنواع السياقات الثلاثة الموجودة لاستخدام عنصر الصورة الرمزية مثل الحروف المختصرة أو الصورة أو الأيقونة ـ
>
> Adhere to the three approved avatar contexts: using initials, an image, or an icon, as defined in the platform design standards.
<!-- /dga -->

### 32

<!-- dga -->
> التحقق من استخدام عنصر التقييم بما يتماشى مع نظام التصميم الموحد (كود المنصات)
>
> Ensure Rating follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/feedback/rating

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Normal, Pressed) كما هو معتمد في كود المنصات.
>
> Apply the interactive states of the component (Normal, Pressed) as defined in the Platform Design Code.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (Selected, Half) كما هو معتمد في كود المنصات.
>
> Apply the contextual states of the component (Selected, Half) as specified in the Platform Design Code.
<!-- /dga -->

### 33

<!-- dga -->
> التحقق من استخدام عنصر التلميح بما يتماشى مع نظام التصميم الموحد (كود المنصات)
>
> Ensure Tooltip follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/feedback/tooltip

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق موضع العنصر المكاني (المكان: أعلى، أسفل، يمين، يسار - والمحاذاة: البداية، الوسط، النهاية) كما هو معتمد في كود المنصات.
>
> Apply the spatial positioning of the element (placement: top, bottom, right, left; and alignment: start, center, end) as defined in the Platform Design Code.
<!-- /dga -->

### 34

<!-- dga -->
> التحقق من استخدام عنصر المدخلات بما يتماشى مع نظام التصميم الموحد (كود المنصات)
>
> Ensure Text Input follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/forms-and-inputs/input

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Pressed, Focused, Read-only, Disabled) كما هو معتمد في كود المنصات.
>
> Apply states (Default, Hovered, Pressed, Focused, Read-only, Disabled).
<!-- /dga -->

<!-- dga -->
> دعم ظهور التلميحات (Placeholder) والنصوص المساعدة بشكل متناسق مع التصميم، مع وضوح رسائل الخطأ وطريقة معالجتها عند الحاجة.
>
> Support the consistent display of placeholders and helper texts in alignment with the design, ensuring error messages are clear and properly handled when necessary.
<!-- /dga -->

### 35

<!-- dga -->
> التحقق من استخدام عنصر الجدول بما يتماشى مع نظام التصميم الموحد (كود المنصات)
>
> Ensure Tables follow the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/data-display/table

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

### 36

<!-- dga -->
> التحقق من استخدام عنصر محدد التاريخ بما يتماشى مع نظام التصميم الموحد (كود المنصات)
>
> Ensure Date Picker follows the Platforms Code Design System
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/forms-and-inputs/datepicker

<!-- dga -->
> استخدام العنصر كما هو معتمد في كود المنصات من حيث (الشكل، الحواف، اللون، المسافات، وغيرها) دون أي تعديل على التصميم الأساسي.
>
> Use the component as defined in the Platforms Code, including its properties (shape, border radius, color, spacing, etc.) without any customization to the base design.
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر التفاعلية (Default, Hovered, Pressed, Focused, Disabled ) كما هو معتمد في كود المنصات.
>
> Apply interactive states (Default, Hovered, Pressed, Focused, Disabled).
<!-- /dga -->

<!-- dga -->
> تطبيق حالات العنصر السياقية (Selected, Today, Nex/Prev) كما هو معتمد في كود المنصات.
>
> Apply contextual states (Selected, Today, Next/Prev) as specified in the platform design system.
<!-- /dga -->

### 37

<!-- dga -->
> التحقق من إنشاء خريطة الموقع لدعم تنقل المستخدم وسهولة اكتشاف المحتوى
>
> Ensure that a Sitemap is created to support user navigation and facilitate content discoverability.
<!-- /dga -->

<!-- dga -->
> تجميع بيانات هيكلة الموقع الرئيسية من عناصر التنقل (مثل Nav header, Footer, Breadcrumb)
>
> Collect the main site structure data from navigation elements (such as Nav header, Footer, Breadcrumb).
<!-- /dga -->

<!-- dga -->
> توفر خريطة موقع (Sitemap) شاملة ومحدثة تُظهر توزيع الصفحات والمحتوى بشكل يسهل فهمه من قبل المستخدمين ومحركات البحث.
>
> Provide a comprehensive and up-to-date sitemap that clearly displays the distribution of pages and content, making it easy to understand for both users and search engines.
<!-- /dga -->

### 38

<!-- dga -->
> التأكد من فعالية تصميم التفاعل في تسهيل مهام المستخدم، بما في ذلك استجابات الأزرار، والتعرف على الإيماءات، والتعليقات.
>
> Ensure that interaction design effectively facilitates user tasks, including button responses, gesture recognition, and feedback.
<!-- /dga -->

<!-- dga -->
> تفعيل استجابات بصرية فورية وواضحة عند التفاعل مع العناصر (مثل الأزرار والروابط).
>
> Enable immediate and clear visual feedback upon interacting with elements (such as buttons and links).
<!-- /dga -->

<!-- dga -->
> دعم النظام الإيماءات الأساسية (مثل السحب، النقر المطوّل، التمرير) بشكل طبيعي وسلس على الأجهزة اللمسية.
>
> Support basic gesture interactions (like swipe, long press, and scroll) naturally and smoothly on touch devices.
<!-- /dga -->

<!-- dga -->
> يُمنع إخفاء العناصر المهمة (مثل الأزرار/المحتوى) خلف رسوم أو مؤثرات حركية؛ يجب أن تكون هذه العناصر مرئية دائمًا دون الحاجة إلى التمرير أو التفاعل.
>
> Avoid hiding important elements (such as buttons or content) behind animations or effects; these elements must always be visible without requiring scrolling or additional interaction.
<!-- /dga -->

### 39

<!-- dga -->
> التأكد من أن المحتوى يعطي الأولوية لنهج اللغة العربية أولاً، وتضمن استخدام اللغات الاخرى وفقًا لمعايير هيئة الحكومة الرقمية.
>
> Ensure that content prioritizes the Arabic-first approach, while supporting the use of other languages in accordance with the DGA standards.
<!-- /dga -->

<!-- dga -->
> استخدام اللغة العربية كلغة أساسية في جميع الصفحات والمكونات، مع ضمان جودة الصياغة وسلامة اللغة.
>
> Use Arabic as the primary language across all pages and components, ensuring high-quality wording and language accuracy.
<!-- /dga -->

<!-- dga -->
> دعم اللغات الأخرى (مثل الإنجليزية) بشكل ثانوي بما يتوافق مع توجهات ومعايير هيئة الحكومة الرقمية.
>
> Support other languages (such as English) secondarily, in accordance with the DGA guidelines and standards.
<!-- /dga -->

<!-- dga -->
> عند التبديل بين اللغة العربية والإنجليزية، يجب أن يتم تغيير المحتوى بالكامل بشكل دقيق دون فقدان أو نقص في المعلومات.
>
> When switching between Arabic and English, the entire content must be accurately updated without any loss or omission of information.
<!-- /dga -->

### 40

<!-- dga -->
> التأكد من آليات تقييم المستخدمين لتقديم الملاحظات حول التطبيق/الموقع، وكيفية الاعتراف بهذه التعليقات واستخدامها من قبل المنظمة.
>
> Ensure that mechanisms are in place for users to provide feedback about the application/website, and that this feedback is acknowledged and utilized by the organization.
<!-- /dga -->

<!-- dga -->
> توفر وسيلة واضحة للمستخدمين لتقديم الملاحظات (الاستناد على قالب تقييم).
>
> Provide a clear method for users to submit feedback (based on a standardized evaluation form).
<!-- /dga -->

<!-- dga -->
> تُعرض رسالة تأكيد بعد إرسال الملاحظات توضح أنه تم استلامها بنجاح.
>
> Display a confirmation message after feedback submission to indicate successful receipt.
<!-- /dga -->

### 41

<!-- dga -->
> التأكد من تقييم مدى رؤية ووضوح إشعارات الخصوصية والأمان، والتأكد من أنها مفهومة ويمكن لجميع المستخدمين الوصول إليها.
>
> Ensure that the visibility and clarity of privacy and security notices are evaluated, and that they are understandable and accessible to all users.
<!-- /dga -->

<!-- dga -->
> وضوح إشعارات الخصوصية والأمان للمستخدم دون الحاجة للبحث عنها في أماكن مخفية أو غير متوقعة.
>
> Clear privacy and security notifications should be easily accessible to users without requiring them to search in hidden or unexpected places.
<!-- /dga -->

<!-- dga -->
> توفر روابط أو رسائل واضحة في نقاط التفاعل الأساسية للإقرارات التي تشمل إشعارات الخصوصية والأمان مثل صفحة الدخول، التسجيل، أو عند جمع بيانات المستخدم.
>
> Provide clear links or messages at key interaction points—such as login, registration pages, or when collecting user data—to inform users about privacy and security notices.
<!-- /dga -->

<!-- dga -->
> وضع الإشعارات في مواضع مألوفة مثل التذييل (Footer) أو نافذة منبثقة تظهر عند أول زيارة للموقع.
>
> Place notifications in familiar locations like the footer or as a popup displayed on the user’s first visit to the site.
<!-- /dga -->

### 42

<!-- dga -->
> التأكد من الاتساق في المصطلحات المستخدمة عبر النظام لمنع الارتباك والمساعدة في فهم المستخدم.
>
> Ensure consistency in the terminology used across the system to prevent confusion and support user understanding.
<!-- /dga -->

<!-- dga -->
> استخدام مصطلحات موحدة ومتسقة في جميع الشاشات والعناصر، لتسهيل فهم المستخدم.
>
> Use consistent and unified terminology across all screens and elements to facilitate user understanding.
<!-- /dga -->

<!-- dga -->
> المصطلحات تتبع دليل اللغة المعتمد (إن وجد)، وتعكس وظيفة العنصر أو الإجراء بوضوح ودقة.
>
> Terminology should follow the approved language guide (if available) and clearly reflect the function of the element or action.
<!-- /dga -->

<!-- dga -->
> يجب أن يكون كل مصطلح مستخدَم واضحًا ويعبّر بدقة عن وظيفته للمستخدم.
>
> Every term used must be clear and accurately reflect its function to the user.
<!-- /dga -->

<!-- dga -->
> وجود تكرار أو تعبيرات مختلفة لنفس المعنى وتبسيط المحتوى بأفضل طريقة تناسب الجمهور المستهدف.
>
> Avoid repetition or multiple expressions for the same meaning, and simplify content in the most suitable way for the target audience.
<!-- /dga -->

### 43

<!-- dga -->
> التأكد من الحفاظ على نهج ثابت في كيفية التعامل مع الأخطاء وعرضها عبر التطبيق/الموقع لضمان تجربة مستخدم سلسة.
>
> Ensure a consistent approach to how errors are handled and displayed across the application/website to ensure a smooth user experience.
<!-- /dga -->

<!-- dga -->
> عرض الأخطاء بنفس النمط البصري والمكاني لنفس السياق (مثلا في حال وجود سياق لتعبئة حقول مختلفة يجب ان يظهر الخطأ بنفس النمط لكل حقل).
>
> Display errors using a consistent visual style and placement within the same context (e.g., for multiple input fields, error messages should appear uniformly for each field).
<!-- /dga -->

<!-- dga -->
> تتبع رسائل الخطأ صياغة واضحة ومتسقة تسهّل على المستخدم فهم المشكلة وطريقة حلها.
>
> Error messages should follow a clear and consistent wording that helps users easily understand the issue and how to resolve it.
<!-- /dga -->

<!-- dga -->
> صياغة الرسائل واضحة، موجزة، وتسترشد بأسلوب لغوي موحد يسهل على المستخدم فهم الإجراء أو المشكلة (مثال: “تم حفظ البيانات بنجاح” أو “الرجاء إدخال البريد الإلكتروني”).
>
> Messages must be clear, concise, and use a unified linguistic style that makes it easy for users to comprehend the action or problem (e.g., “Data saved successfully” or “Please enter your email address”).
<!-- /dga -->


## المعايير الثانوية

### 44

<!-- dga -->
> ضمان توافق عنصر قائمة التنقل الجانبية مع نظام التصميم الموحد (كود المنصات)
>
> Follow the Unified Design System (Platforms Code) for the Nav Drawer component
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/ui-shell/navigation-drawer

### 45

<!-- dga -->
> التأكد من استخدام عنصر ترقيم الصفحات بما يتماشى مع نظام التصميم الموحد (كود المنصات)
>
> Follow the Unified Design System (Platforms Code) for the Pagination component
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/navigational/pagination

### 46

<!-- dga -->
> ضمان استخدام عنصر التحميل وفق نظام التصميم الموحد (كود المنصات)
>
> Ensure the Loading component is implemented per the Unified Design System (Platforms Code) guidelines
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/loading-and-status/loading

### 47

<!-- dga -->
> التأكد من توافق عنصر الخطوات مع معايير التصميم الموحد (كود المنصات)
>
> Ensure the Steps component is in line with the Unified Design System (Platforms Code) specifications
<!-- /dga -->

Reference column: https://design.dga.gov.sa/guidelines/components/forms-and-inputs/steps

### 48

<!-- dga -->
> التأكد من أن التصميم ينشئ تسلسلاً مرئيًا واضحًا، يوجه انتباه المستخدم إلى العناصر المهمة أولاً.
>
> Ensure the design establishes a clear visual hierarchy, directing the user's attention to important elements first
<!-- /dga -->

### 49

<!-- dga -->
> التأكد من ما إذا كان التنقل بديهيًا، بما في ذلك التجميع المنطقي ووضع العلامات على الأقسام والروابط.
>
> Ensure the navigation is intuitive, including logical grouping and labeling of sections and links
<!-- /dga -->

### 50

<!-- dga -->
> التأكد من ما إذا كان من الممكن إكمال المهام الشائعة بكفاءة بأقل الخطوات والتفاعلات البديهية
>
> Ensure common tasks can be completed efficiently with minimal steps and intuitive interactions
<!-- /dga -->

### 51

<!-- dga -->
> التأكد من مراجعة موارد المساعدة والوثائق المتوفرة لسهولة الوصول إليها والوضوح والفائدة في مساعدة المستخدمين على استخدام التطبيق/الموقع بشكل فعال
>
> Ensure available help resources and documentation are easily accessible, clear, and useful in assisting users to effectively use the application/website
<!-- /dga -->

### 52

<!-- dga -->
> التأكد من أن اللغة المستخدمة في الواجهة واضحة وموجزة ومناسبة للجمهور المستهدف، وتقييم الترجمة لتدعم اللغات المتعددة
>
> Ensure the language used in the interface is clear, concise, and appropriate for the intended audience, and assess localization efforts for multilingual support
<!-- /dga -->

### 53

<!-- dga -->
> التأكد من ما إذا كانت واجهة المستخدم تتصرف بطريقة يمكن التنبؤ بها، مما يقلل من ارتباك المستخدم وأخطائه
>
> Evaluate whether the user interface behaves in a predictable manner, reducing user confusion and errors
<!-- /dga -->

### 54

<!-- dga -->
> التأكد من أن أنماط التفاعل (مثل الإيماءات والنقرات والتنقل) متسقة، مما يجعل النظام بديهيًا وقابلاً للتعلم
>
> Ensure the interaction patterns (eg, gestures, clicks, navigation) are consistent, making the system intuitive and learnable
<!-- /dga -->

### 55

<!-- dga -->
> التأكد من تقديم المحتوى (النصوص والصور ومقاطع الفيديو) بأسلوب موحد ونبرة مناسبة للجمهور المستهدف
>
> Ensure the content (text, images, videos) is presented in a uniform style and tone appropriate for the target audience
<!-- /dga -->

### 56

<!-- dga -->
> التأكد من أن التغذية الراجعة المقدمة للمستخدمين عن أفعالهم متسقة في الأسلوب والتوقيت عبر التطبيق/الموقع لتجنب الالتباس.
>
> Ensure that feedback provided to users for their actions is consistent in style and timing across the application/website to avoid confusion
<!-- /dga -->
