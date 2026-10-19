# Raw capture — the CODE tab of every component page, 2026-10-19

Every DGA component page has a Live Demo with a **Visual** and a **Code** tab. The Code tab
had never been read by this kit. Each sample below is byte-exact from the `code:` template
literal in DGA's live lazy chunk (named per section), and each was confirmed **displayed** on
the rendered English Code tab in a browser on 2026-10-19 (50 of 50). A 51st literal, in
`FeedbackDetails-*.js` for the Feedback Section template, is **not** displayed on any page and
is not evidence.

Under every sample, every component page displays the same note:

<!-- dga -->
> This component is designed to utilize React for its functionality. The structure of the code provided will seamlessly integrate with the React framework, especially when paired with the bundled library of National Design System. While the use of the bundled React library is recommended for optimal compatibility and performance, it's not mandatory.You have the flexibility to leverage your preferred framework if you choose to do so. However, it's crucial to ensure that the component is styled according to the provided examples, maintaining consistency in the user interface regardless of the library used.
<!-- /dga -->

These are **illustrative samples**, not a DGA requirement or a complete API contract. Two are
not samples of their component at all: **Menu** and **Footer** display an unrelated Mongoose
schema (`import mongoose, { Schema } from 'untitled'`).

---

## `/guidelines/components/actions/buttons`

Chunk `index-Be1pi7AI.js` · imports: `platformscode-react` · elements: `Btn`, `Tick02Icon`

````jsx
import { Button as Btn } from "platformscode-react";
<Btn
  label={Translation("Button.label")}
  size="lg"
  style="primary-brand"
  leadIcon
  leadIconType={<Tick02Icon />}
/>
````

---

## `/guidelines/components/actions/chip`

Chunk `index-ClZrXBGu.js` · imports: none shown · elements: `DgaChip`

````jsx
<DgaChip
  label={i18n.language === "ar" ? "اختيار" : "item"}
  size="lg"
/>
````

---

## `/guidelines/components/actions/dropdown`

Chunk `index-C9ZCcwa1.js` · imports: none shown · elements: `Dropdown`

````jsx
<Dropdown
  id="dropdown"
  getSelectedOptions={() => {}}
  options={[
    {
      name: "Option 1",
      selected: false,
      value: "option1",
    },
    {
      name: "Option 2",
      selected: true,
      value: "option2",
    },
    {
      name: "Option 3",
      selected: false,
      value: "option3",
    },
  ]}
  placeholder="Option"
  size="lg"
  style="default"
/>
````

---

## `/guidelines/components/actions/floating-Button`

Chunk `index-HzI1na33.js` · imports: `platformscode-new-react` · elements: `FloatingButton`

````jsx
import { FloatingButton } from "platformscode-new-react";;
  <FloatingButton
    icon="plus-sign"
    iconOnly
    label="Button"
    size="small"
    variant="primary-brand"
            />
````

---

## `/guidelines/components/actions/link`

Chunk `index-D2zAKDLV.js` · imports: none shown · elements: `Link`

````jsx
<Link
  url="#"
  external
  label="Link"
  size="lg"
  style="brand"
  target="_blank"
/>
````

---

## `/guidelines/components/content-display/accordion`

Chunk `index-BLN97gdx.js` · imports: none shown · elements: `DgaAccordion`

````jsx
  <DgaAccordion
  content="This is the default accordion state with standard configuration."
  iconAlignment="trailing"
  size="lg"
  title="Default Accordion"
/>
````

---

## `/guidelines/components/content-display/card`

Chunk `index-D9V1uBuB.js` · imports: none shown · elements: `DgaCard`

````jsx
  <DgaCard
    description={Translation("card.demo.description")}
    image=""
    primaryActionLabel={Translation("card.demo.action")}
    secondaryActionLabel={Translation("card.demo.action")}
    showDescription
    showFeaturedIcon
    showTitle
    title={Translation("card.demo.title")}
    type="default"
  />
````

---

## `/guidelines/components/content-display/carousel`

Chunk `index-C4e5bB2B.js` · imports: none shown · elements: `DgaCarousel`, `DgaCarouselItem`

````jsx
<DgaCarousel variant="arrows">
    <DgaCarouselItem></DgaCarouselItem>
    <DgaCarouselItem></DgaCarouselItem>
    <DgaCarouselItem></DgaCarouselItem>
  </DgaCarousel>
````

---

## `/guidelines/components/content-display/code-snippet`

Chunk `index-B1yWIVti.js` · imports: none shown · elements: `DgaCodesnippet`

````jsx
   <DgaCodesnippet
    showButton
    showSidebar
    showTabList
    snippets={}
    type="multi-line"
  />


 
````

---

## `/guidelines/components/content-display/digital-stamp`

Chunk `index-CAGv0o34.js` · imports: `platformscode-new-react` · elements: `DgaDigitalSignature`

````jsx
import { DgaDigitalSignature, } from "platformscode-new-react";
  <DgaDigitalSignature
  extension=".gov.sa"
  language="en"
  linkProps={{
    inline: true,
    label: '20230103200',
    size: 'md',
    target: '_self',
    url: '#',
    variant: 'primary'
  }}
/>
````

---

## `/guidelines/components/content-display/divider`

Chunk `index-CGOOAbmr.js` · imports: none shown · elements: `DgaDivider`

````jsx
  <DgaDivider color="primary" />
````

---

## `/guidelines/components/content-display/list`

Chunk `index-Cr6-LA70.js` · imports: none shown · elements: `DgaListItem`, `DgaListV2`

````jsx
    <DgaListV2 type='ordered' color='neutral'>
    <DgaListItem type="ordered" level='one' itemNumber='1-' itemText={Translation("list.list_item")}></DgaListItem>
    <DgaListItem type="ordered" level='two' itemLetter='a-'  itemText={Translation("list.list_item")}></DgaListItem>
    <DgaListItem type="ordered" level='two' itemLetter='b-'  itemText={Translation("list.list_item")}></DgaListItem>
    <DgaListItem type="ordered" level='two' itemLetter='c-'  itemText={Translation("list.list_item")}></DgaListItem>
   
  </DgaListV2>
  <DgaListV2 type='unordered' color='neutral'>
    <DgaListItem type="unordered" level='one' itemNumber='-' itemText={Translation("list.list_item")}></DgaListItem>
    <DgaListItem type="unordered" level='two' itemLetter='a-'  itemText={Translation("list.list_item")}></DgaListItem>
    <DgaListItem type="unordered" level='two' itemLetter='b-'  itemText={Translation("list.list_item")}></DgaListItem>
    <DgaListItem type="unordered" level='two' itemLetter='c-'  itemText={Translation("list.list_item")}></DgaListItem>
   
  </DgaListV2>
  <DgaListV2 type='with-icon' color='neutral'>
    <DgaListItem type="with-icon" level='one' icon='<i  class="hgi-stroke hgi-checkmark-circle-02"></i>' itemText={Translation("list.list_item")}></DgaListItem>
    <DgaListItem type="with-icon" level='two' icon='<i  class="hgi-stroke hgi-checkmark-circle-02"></i>'  itemText={Translation("list.list_item")}></DgaListItem>
    <DgaListItem type="with-icon" level='two' icon='<i  class="hgi-stroke hgi-checkmark-circle-02"></i>'  itemText={Translation("list.list_item")}></DgaListItem>
    <DgaListItem type="with-icon" level='two' icon='<i  class="hgi-stroke hgi-checkmark-circle-02"></i>'  itemText={Translation("list.list_item")}></DgaListItem>
    
   
  </DgaListV2>
````

---

## `/guidelines/components/content-display/quote`

Chunk `index-UZx9Rl7T.js` · imports: none shown · elements: `DgaQuote`

````jsx
 <DgaQuote
    authorDescription={
      i18n.language == "ar"
        ? "نبذة أو وصف"
        : "brief or description."
    }
    authorName={
      i18n.language == "ar" ? "اسم المؤلف" : "Author's name"
    }
    quoteDescription={
      i18n.language == "ar"
        ? "تُوضع هنا عبارة الاقتباس لتسليط الضوء على مقولة معينة أو تقديم اقتباس مختصر يعبر عن فكرة أو مفهوم مهم."
        : "The quote is placed here to highlight a specific saying or to present a brief quote that expresses an important idea or concept."
    }
    quoteTitle={
      i18n.language == "ar" ? "عنوان الاقتباس" : "Title of quote"
    }
    showAvatar={true}
  />
````

---

## `/guidelines/components/data-display/avatar`

Chunk `index-Bs_NMhSp.js` · imports: none shown · elements: `DgaAvatar`

````jsx
   <DgaAvatar
    imgUrl="/avatar/avatar-img.png"
    size={68}
    type="image"
  />
````

---

## `/guidelines/components/data-display/charts`

Chunk `index-B9VGVVFJ.js` · imports: `platformscode-react` · elements: `DgaChart`

````jsx
  // Imports
  import {DgaChart} from "platformscode-react"
  
  function BasicExample() {
  
    return (
      <>
      <DgaChart
        colors={["#1B8354", "#079455", "#B8EACB", "#54C08A"]}
        height="400px"
        labels={["Team A", "Team B", "Team C", "Team D"]}
        series={[44, 55, 41, 17]}
        type="donut"
        width="100%"
      />

      <DgaChart
        colors={["#1B8354", "#079455"]}
        height="400px"
        series={[
          {
            data: [10, 20, 30, 40],
            group: "apexcharts-axis-0",
            name: "Series 1",
          },
          {
            data: [20, 10, 40, 30],
            group: "apexcharts-axis-0",
            name: "Series 2",
          },
        ]}
        type="line"
        width="100%"
        xaxis={{
          categories: ["Jan", "Feb", "Mar", "Apr"],
          convertedCatToNumeric: true,
        }}
      />

      <DgaChart
        colors={["#1B8354", "#54C08A", "#E5E7EB"]}
        height="400px"
        series={[
          {
            data: [10, 20, 30, 40],
            group: "apexcharts-axis-0",
            name: "Series 1",
          },
          {
            data: [20, 10, 40, 30],
            group: "apexcharts-axis-0",
            name: "Series 2",
          },
          {
            data: [30, 15, 30, 20],
            group: "apexcharts-axis-0",
            name: "Series 3",
          },
        ]}
        type="bar"
        width="100%"
        xaxis={{
          categories: ["Q1", "Q2", "Q3", "Q4"],
          convertedCatToNumeric: false,
        }}
      />
      </>
    );
  }
  
  export default BasicExample;
  
````

---

## `/guidelines/components/data-display/content-switcher`

Chunk `index-Bkdv2bYQ.js` · imports: none shown · elements: `DgaContentSwitcher`

````jsx
            <DgaContentSwitcher
    size="md"
    
  />
````

---

## `/guidelines/components/data-display/metric`

Chunk `index-eXvBbZpX.js` · imports: none shown · elements: `DgaMetric`

````jsx
  <DgaMetric
    Style="large-chart"
    changeProps={{
      trend: 'positive',
      type: '01'
    }}
    chartProps={{
      data: [
        10,
        20,
        30,
        40,
        50
      ],
      showMarker: false,
      trend: 'positive',
      type: 'realistic'
    }}
    onExpandAction={function Qa(){}}
    onPrimaryAction={function Qa(){}}
    onSecondaryAction={function Qa(){}}
    percentage="50%"
    showActions
    showChart
    showFeaturedIcon
    showInfo
    showMoreButton
    showSecondaryAction
    trend={{
      description: 'Increasing trend',
      slope: 'positive',
      value: '+25%'
    }}
  />
````

---

## `/guidelines/components/data-display/structured-list`

Chunk `index-DTsoOumn.js` · imports: none shown · elements: `DgaStructuredList`

````jsx
        <DgaStructuredList
   cells={[
     {
       propertyName: 'row1',
       title: 'Row',
       type: 'element'
     },
     {
       propertyName: 'name',
       title: 'Row',
       type: 'element'
     },
     {
       propertyName: 'row3',
       title: 'Row',
       type: 'element'
     }
   ]}
   data={[
     {
       row1: "Row",
       name: 'Row',
       row3: 'Row',
     },
     {
       row1: "Row",
       name: 'Row',
       row3: 'Row',
 
     },
     {
       row1: "Row",
       name: 'Row',
       row3: 'Row',
 
     },
     
   ]}
   rowDivider
   selectable={false}
   alternate={false}
 />
````

---

## `/guidelines/components/data-display/table`

Chunk `index-C2lBZyrH.js` · imports: none shown · elements: `DgaDataTable`

````jsx
       <DgaDataTable
    cells={[
      {
        colSpan: 1,
        isFilter: false,
        isSort: false,
        propertyName: 'header1',
        title: 'Header',
        type: 'propertyName'
      },
      {
        colSpan: 1,
        isFilter: false,
        isSort: true,
        propertyName: 'header2',
        sort: 'up',
        title: 'Header',
        type: 'propertyName'
      },
      {
        colSpan: 1,
        isFilter: true,
        isSort: false,
        propertyName: 'header3',
        title: 'Header',
        type: 'propertyName'
      },
      {
        colSpan: 1,
        isFilter: false,
        isSort: false,
        propertyName: 'header4',
        title: 'Header',
        type: 'element',
        El: 'dga-tag',
        elProperties: ['label'],
        staticProps: { variant: 'neutral', outlined: true, size: 'sm' }
      }
    ]}
    contained
    data={[
      { header1: 'Link', header2: 'Cell', header3: 'Cell', label: 'Tag', selected: false },
      { header1: 'Link', header2: 'Cell', header3: 'Cell', label: 'Tag', selected: false },
      { header1: 'Link', header2: 'Cell', header3: 'Cell', label: 'Tag', selected: false },
      { header1: 'Link', header2: 'Cell', header3: 'Cell', label: 'Tag', selected: false }
    ]}
    getSelectedRows={function vu(){}}
    pressOnFilter={function vu(){}}
    rowDivider
    showSelectCheckBox
  />
````

---

## `/guidelines/components/feedback/modal`

Chunk `index-BVAvG-sK.js` · imports: none shown · elements: `DgaModal`

````jsx
    <DgaModal
  buttonsList={[
    { extraClass: '', label: 'Button 1', onClick: () => {}, title: 'Button' },
    { extraClass: '', label: 'Button 2', onClick: () => {}, title: 'Button' },
  ]}
  closeButton
  featuredIconProps={{
    size: 'md',
    color: 'gray',
    variant: 'light',
    circle: false,
    icon: {
      name: 'InformationCircle',
      variant: 'stroke',
      type: 'sharp',
      size: 20,
    }
  }}
  modalTitle={
    i18n.language == "ar" ? "العنوان يذهب هنا" : "Title goes here"
  }
  name="testModal"
  onClose={() => {setShowModal(false)}}
  open={showModal}
  secondBtnPosition="left"
  staticModal
>
<p className="text-[14px] leading-[20px] font-[400] text-[var(--colors-gray-neutral-700)]">
                {i18n.language == "ar"
                  ? "عندما يحتاج المشروط إلى شرح تفصيلي إضافي، فإنه يذهب هنا."
                  : "When a Modal needs a further detailed explanation, it goes here."}
              </p>
</DgaModal>
````

---

## `/guidelines/components/feedback/notification`

Chunk `index-B3tDTnqA.js` · imports: none shown · elements: `DgaNotificationToast`

````jsx
<DgaNotificationToast
vPostion="top"
  action
  buttonsList={[
    {
      extraClasses: "",
      id: "1",
      label: i18next.language == "en" ? "Button" : "زر",
      onClick: () => {},
      title: "Button",
    },
    {
      extraClasses: "",
      id: "2",
      label: i18next.language == "en" ? "Button" : "زر",
      onClick: () => {},
      title: "Button",
    },
  ]}
  closeButton
  hasHelperText
  helperText={
    i18next.language == "en"
      ? "When a Notification/Alert needs a further detailed explanation, it goes here."
      : "عندما يحتاج الإشعار/التنبيه إلى شرح تفصيلي إضافي، يتم وضعه هنا."
  }
  leadText={
    i18next.language == "en"
      ? "Notification/Alert message title"
      : "عنوان رسالة الإخطار/التنبيه"
  }
  onClose={() => {setShow(false)}}
  type="info"
  open={Show}
/>
````

---

## `/guidelines/components/feedback/rating`

Chunk `index-CcsRAiTh.js` · imports: none shown · elements: `DgaRating`

````jsx
  <DgaRating
    value={rating}
    max={5}
    onChange={(val) => handleRatingChange(val)}
    size="md"
    readOnly={false}
  />
````

---

## `/guidelines/components/feedback/tooltip`

Chunk `index-Bocbw4AM.js` · imports: none shown · elements: `DgaTooltip`

````jsx
   <DgaTooltip
    title="Tooltip title"
    helperText="Max width of tooltips is 240px - text will wrap automatically"
    icon
    feedbackIcon={{
      size: 24,
      style: 'container',
      type: 'neutral-?'
    }}
    beakPlacement="bottom"
    beakAlignment="center"
  >
    <span className="text-md-semibold">Hover Here</span>
  </DgaTooltip>
````

---

## `/guidelines/components/forms-and-inputs/checkbox`

Chunk `index-DLa7nJX5.js` · imports: none shown · elements: `DgaCheckbox`

````jsx
 <DgaCheckbox
               alertText="Error/Warning message"
               showBorderOnFocusAndFocusOute
               color="brand"
               helperText="When a selection needs a further detailed explanation, it goes here."
               label="Checkbox label"
               alertMessage={true}
             />
````

---

## `/guidelines/components/forms-and-inputs/datepicker`

Chunk `index-T6dedKiu.js` · imports: none shown · elements: `DgaDatepicker`

````jsx
<DgaDatepicker
  initialDate={new Date()}
  onChange={handleSelectDate}
  value={selectedDate}
/>
````

---

## `/guidelines/components/forms-and-inputs/file-uploader`

Chunk `index-CBj654Ob.js` · imports: none shown · elements: `DgaFileUpload`

````jsx
  <DgaFileUpload multiple={false} />
````

---

## `/guidelines/components/forms-and-inputs/input`

Chunk `index-uiMOltMU.js` · imports: none shown · elements: `DgaTextInput`

````jsx
  <DgaTextInput
    feedbackIconType="error"
    onBlur={() => {}}
    onChange={() => {
    }}
    onInput={() => {}}
    placeholder={Translation("textinput_placeholder")}
    size="lg"
    variant="default"
    value={textValue}
  />
````

---

## `/guidelines/components/forms-and-inputs/number-input`

Chunk `index-CL745SP7.js` · imports: `platformscode-react` · elements: `DgaNumberInput`

````jsx
// Imports
import { DgaNumberInput } from "platformscode-react";

function BasicExample() {

  return (
    <>
    <DgaNumberInput
    feedbackIconType="error"
    icon
    inputPrefix={null}
    inputSuffix={null}
    label={"Label"}
    name="numberInput"
    onBlur={function Qa(){}}
    onChange={function Qa(){}}
    onInput={function Qa(){}}
    placeholder="0000"
    size="lg"
    variant="default"
  />
    </>
  );
}

export default BasicExample;
````

---

## `/guidelines/components/forms-and-inputs/radio`

Chunk `index-B6MI7Xhd.js` · imports: none shown · elements: `DgaRadioButton`

````jsx
<DgaRadioButton
  name="radio-button"
  color="brand"
  label="Radio Button label"
/>
````

---

## `/guidelines/components/forms-and-inputs/slider`

Chunk `index-C4l_aw50.js` · imports: `platformscode-new-react` · elements: `DgaSlider`

````jsx
// Imports
import {DgaSlider} from "platformscode-new-react"

<DgaSlider
  helperText="Helper Text"
  label="Range Slider"
  max={100}
  min={0}
  showHelperText
  showLabel
  size="small"
  step={1}
/>
````

---

## `/guidelines/components/forms-and-inputs/steps`

Chunk `index-CURDqx2t.js` · imports: none shown · elements: `DgaProgressIndicator`, `DgaProgressIndicatorStep`

````jsx
  <DgaProgressIndicator activeStep={2} alignment="horizontal">
    <DgaProgressIndicatorStep
      description="this is step description"
      title="Step One"
    />
    <DgaProgressIndicatorStep
      description="this is step description"
      title="Step Two"
    />
    <DgaProgressIndicatorStep
      description="this is step description"
      title="Step Three"
      nextStep={false}
    />
  </DgaProgressIndicator>
````

---

## `/guidelines/components/forms-and-inputs/switch`

Chunk `index-fnOi2Tef.js` · imports: `platformscode-react` · elements: `Switch`

````jsx
  // Imports
  import { Switch  } from "platformscode-react";
  
  function BasicExample() {

    return (
      <>
         <Switch
              color="brand"
              label="Switch label"
              onChange={() => {}}
              onInput={() => {}}
            />
      </>
    );
  }
  
  export default BasicExample;
````

---

## `/guidelines/components/forms-and-inputs/textarea`

Chunk `index-BtTCW6Cb.js` · imports: `platformscode-react` · elements: `Textarea`

````jsx
  // Imports
  import { Textarea } from "platformscode-react";
  
  function BasicExample() {
   const [enteredText, setEnteredText] = useState("");

   const handleInputChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
     setEnteredText(e.target.value);
   };
    return (
      <>
          <Textarea
              placeholder="Enter Text"
              value={enteredText}
              onChange={handleInputChange}
            />
      </>
    );
  }
  
  export default BasicExample;
````

---

## `/guidelines/components/loading-and-status/loading`

Chunk `index-B-E5vnEA.js` · imports: `platformscode-react` · elements: `Spinner`

````jsx
  // Imports
  import { Spinner } from "platformscode-react";
  
  function BasicExample() {

    return (
      <>
        <Spinner size="md" style="brand" />
      </>
    );
  }
  
  export default BasicExample;
````

---

## `/guidelines/components/loading-and-status/progress-bar`

Chunk `index-B6fHujGZ.js` · imports: `platformscode-react` · elements: `Tag`

````jsx
  // Imports
  import { Tag } from "platformscode-react";
  
  function BasicExample() {

    return (
      <>
         <Tag
              color="gray"
              label="Tag"
              leadIcon
              leadIconType={
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 18 18"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M8.46101 2.59041C8.63388 2.24021 8.72031 2.06511 8.83764 2.00916C8.93973 1.96049 9.05834 1.96049 9.16043 2.00916C9.27776 2.06511 9.3642 2.24021 9.53706 2.59041L11.1771 5.91289C11.2281 6.01628 11.2536 6.06797 11.2909 6.10811C11.3239 6.14365 11.3635 6.17244 11.4075 6.19289C11.4572 6.21599 11.5142 6.22433 11.6283 6.24101L15.2968 6.77721C15.6831 6.83367 15.8762 6.8619 15.9656 6.95625C16.0434 7.03835 16.08 7.15115 16.0652 7.26326C16.0481 7.39211 15.9083 7.52831 15.6286 7.80071L12.9751 10.3852C12.8924 10.4658 12.851 10.5061 12.8243 10.554C12.8007 10.5965 12.7856 10.6431 12.7797 10.6913C12.7731 10.7458 12.7829 10.8027 12.8024 10.9165L13.4285 14.567C13.4945 14.952 13.5275 15.1446 13.4655 15.2588C13.4115 15.3582 13.3155 15.4279 13.2043 15.4485C13.0765 15.4722 12.9036 15.3813 12.5579 15.1995L9.27831 13.4748C9.17612 13.4211 9.12503 13.3942 9.0712 13.3836C9.02355 13.3743 8.97453 13.3743 8.92687 13.3836C8.87304 13.3942 8.82195 13.4211 8.71977 13.4748L5.44022 15.1995C5.09446 15.3813 4.92158 15.4722 4.79375 15.4485C4.68253 15.4279 4.58657 15.3582 4.53258 15.2588C4.47052 15.1446 4.50354 14.952 4.56958 14.567L5.19569 10.9165C5.21521 10.8027 5.22497 10.7458 5.21836 10.6913C5.21252 10.6431 5.19736 10.5965 5.17373 10.554C5.14704 10.5061 5.10568 10.4658 5.02296 10.3852L2.36944 7.80071C2.08977 7.52831 1.94993 7.39211 1.93292 7.26326C1.91811 7.15115 1.95469 7.03835 2.03246 6.95625C2.12185 6.8619 2.315 6.83367 2.70131 6.77721L6.36976 6.24101C6.48384 6.22433 6.54088 6.21599 6.59056 6.19289C6.63455 6.17244 6.67414 6.14365 6.70716 6.10811C6.74445 6.06797 6.76997 6.01628 6.821 5.91289L8.46101 2.59041Z"
                    stroke="#161616"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              }
              size="lg"
            />
      </>
    );
  }
  
  export default BasicExample;
````

---

## `/guidelines/components/loading-and-status/radial-stepper`

Chunk `index-Coi1p3SS.js` · imports: none shown · elements: `DgaRadialSteppe`

````jsx
<div
  style={{
    backgroundColor: 'transparent',
    borderRadius: '10px',
    padding: '20px'
  }}
>
  <DgaRadialSteppe
    activeStep={1}
    showStepDescription
    showStepName
    showText
    size="120px"
    steps={[
      {
        showNextStep: true,
        showPreStep: false,
        stepDescription: 'This is the first step of the process.',
        stepName: 'Introduction',
        text: 'Step 1'
      },
      {
        showNextStep: true,
        showPreStep: true,
        stepDescription: 'Here are some additional details.',
        stepName: 'Details',
        text: 'Step 2'
      },
      {
        showNextStep: true,
        showPreStep: true,
        stepDescription: 'This is the review and confirmation step.',
        stepName: 'Confirmation',
        text: 'Step 3'
      },
      {
        showNextStep: false,
        showPreStep: true,
        stepDescription: 'This is the final step to complete the process.',
        stepName: 'Completion',
        text: 'Step 4'
      }
    ]}
    variant="primary"
  />
</div>
````

---

## `/guidelines/components/loading-and-status/skeleton`

Chunk `index-B6L4nKdH.js` · imports: none shown · elements: `DgaLineSkeleton`, `DgaSquareSkeleton`

````jsx
  <div className="flex gap-[10px]" style={{
        background: "white",
        padding: "1rem",
        borderRadius: "8px"
      }}>
          <DgaSquareSkeleton type={"1"} width="64px" />
          <div >
            {[1, 2, 3, 4, 5].map(item => <DgaLineSkeleton key={item} type={item % 2 === 0 ? "1" : "2"} size="sm" style={{
            marginBottom: "0.5rem"
          }} />)}
          </div>
        </div>
````

---

## `/guidelines/components/navigational/breadcrumbs`

Chunk `index-C_NdDELm.js` · imports: none shown · elements: `DgaBreadcrumbs`

````jsx
  <DgaBreadcrumbs
key={Translation("breadcrumb.link")}
items={[
  {
    label: Translation("breadcrumb.link"),
    path: "/link",
  },
  {
    label: Translation("breadcrumb.link"),
    path: "/link",
    disabled: true,
  },
]}
max={5}
/>
````

---

## `/guidelines/components/navigational/menu`

Chunk `index-DPsAGqYE.js` · imports: `untitled` · elements: none · **placeholder, not a sample of this component**

````jsx
// Imports
import mongoose, { Schema } from 'untitled'

// Collection name
export const collection = 'Design'|

// Schema
const schema = new Schema({
  name: {
    type: String,
    required: true
  },

  description: {
    type: String
  }
}, {timestamps: true})

// Model
export default untitled.model(collection, schema, collection)
````

---

## `/guidelines/components/navigational/pagination`

Chunk `index-DVIlfg0R.js` · imports: none shown · elements: `DgaPagination`

````jsx
  <DgaPagination
   currentPage={1}
   onChange={function vu(){}}
   siblingCount={1}
   size="large"
   totalPageCount={999}
 />
````

---

## `/guidelines/components/navigational/slide-out`

Chunk `index-DenlEOeZ.js` · imports: none shown · elements: `DgaButton`, `DgaDivider`, `DgaMenuGroup`, `DgaMenuItem`, `DgaSlideoutMenu`, `DgaSlideoutMenuActions`, `DgaSlideoutMenuHeader`, `DgaSlideoutMenuItems`

````jsx
<DgaSlideoutMenu backgroundColor="gray" scrollbar={false} open>
<DgaSlideoutMenuHeader
title="Title"
description="Description gose here."
/>

<DgaSlideoutMenuItems>
<DgaMenuGroup groupLabel="GROUP LABEL">
<DgaMenuItem label="Item Label" hasTrailElement hasLeadIcon>
<svg
slot="lead-icon"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M7.75 2C7.75 1.58579 7.41421 1.25 7 1.25C6.58579 1.25 6.25 1.58579 6.25 2V5.25H3C2.58579 5.25 2.25 5.58579 2.25 6C2.25 6.41421 2.58579 6.75 3 6.75H6.25V10C6.25 10.4142 6.58579 10.75 7 10.75C7.41421 10.75 7.75 10.4142 7.75 10V6.75H11C11.4142 6.75 11.75 6.41421 11.75 6C11.75 5.58579 11.4142 5.25 11 5.25H7.75V2Z"
fill="#161616"
/>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M10.1809 22.749C8.29902 22.749 7.35404 22.749 6.51505 22.454C5.15405 21.976 4.08106 20.963 3.56906 19.673C3.24806 18.864 3.24805 17.967 3.24805 16.181V11.999C3.24805 11.585 3.58405 11.249 3.99805 11.249C4.41205 11.249 4.74805 11.585 4.74805 11.999V16.181C4.74805 17.777 4.74805 18.578 4.96305 19.121C5.31405 20.007 6.06105 20.706 7.01105 21.04C7.60904 21.25 8.46804 21.25 10.18 21.25C10.4543 21.25 10.7164 21.25 10.967 21.2497C10.9779 21.2492 10.9889 21.249 11 21.249C12.424 21.249 13.583 20.09 13.583 18.666C13.583 18.5059 13.575 18.3334 13.5666 18.151L13.5647 18.1111C13.5398 17.5665 13.5116 16.9499 13.665 16.374C13.888 15.542 14.543 14.887 15.375 14.665C15.952 14.51 16.571 14.539 17.117 14.565L17.1474 14.5664C17.3312 14.5749 17.5059 14.583 17.667 14.583C19.057 14.583 20.1945 13.4787 20.248 12.1015L20.248 9.273C20.248 6.38201 20.248 4.93099 19.563 4.07C19.364 3.82 19.129 3.599 18.862 3.411C17.9251 2.75 16.3691 2.75 13.2701 2.75H12.997C12.583 2.75 12.247 2.414 12.247 2C12.247 1.586 12.583 1.25 12.997 1.25H13.2701C16.685 1.25 18.4001 1.25 19.726 2.185C20.1091 2.455 20.449 2.775 20.736 3.136C21.747 4.407 21.747 6.03299 21.747 9.27298L21.747 11.933C21.749 11.9551 21.75 11.9774 21.75 12C21.75 12.0526 21.749 12.105 21.747 12.1571C21.7463 14.9883 21.7274 16.4556 21.225 17.722C20.39 19.828 18.6341 21.484 16.4071 22.266C15.1592 22.704 13.714 22.7456 11.0577 22.7496C11.0382 22.7499 11.0186 22.75 10.999 22.75C10.7376 22.7503 10.4648 22.75 10.1791 22.75L10.1809 22.749ZM15.912 20.851C15.443 21.0155 14.9065 21.1121 14.2237 21.169C14.7614 20.4775 15.082 19.6091 15.082 18.667C15.082 18.4764 15.0734 18.2815 15.0649 18.0911L15.063 18.048L15.0628 18.0447C15.0419 17.5877 15.0202 17.1152 15.114 16.763C15.199 16.448 15.447 16.199 15.763 16.115C16.1111 16.0211 16.5785 16.0425 17.0317 16.0633L17.047 16.064L17.0872 16.0658C17.2786 16.0743 17.4754 16.083 17.667 16.083C18.6203 16.083 19.4985 15.7546 20.1941 15.2049C20.1415 16.038 20.0375 16.6513 19.8321 17.17C19.1581 18.871 17.729 20.213 15.912 20.851Z"
fill="#161616"
/>
</svg>

<p
slot="trail-element"
className="text-[var(--text-secondary-paragraph,#6C737F)] text-[16px] leading-[24px] font-[400]"
>
+99
</p>
</DgaMenuItem>

<DgaMenuItem label="Item Label" hasTrailElement hasLeadIcon>
<svg
slot="lead-icon"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M7.75 2C7.75 1.58579 7.41421 1.25 7 1.25C6.58579 1.25 6.25 1.58579 6.25 2V5.25H3C2.58579 5.25 2.25 5.58579 2.25 6C2.25 6.41421 2.58579 6.75 3 6.75H6.25V10C6.25 10.4142 6.58579 10.75 7 10.75C7.41421 10.75 7.75 10.4142 7.75 10V6.75H11C11.4142 6.75 11.75 6.41421 11.75 6C11.75 5.58579 11.4142 5.25 11 5.25H7.75V2Z"
fill="#161616"
/>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M10.1809 22.749C8.29902 22.749 7.35404 22.749 6.51505 22.454C5.15405 21.976 4.08106 20.963 3.56906 19.673C3.24806 18.864 3.24805 17.967 3.24805 16.181V11.999C3.24805 11.585 3.58405 11.249 3.99805 11.249C4.41205 11.249 4.74805 11.585 4.74805 11.999V16.181C4.74805 17.777 4.74805 18.578 4.96305 19.121C5.31405 20.007 6.06105 20.706 7.01105 21.04C7.60904 21.25 8.46804 21.25 10.18 21.25C10.4543 21.25 10.7164 21.25 10.967 21.2497C10.9779 21.2492 10.9889 21.249 11 21.249C12.424 21.249 13.583 20.09 13.583 18.666C13.583 18.5059 13.575 18.3334 13.5666 18.151L13.5647 18.1111C13.5398 17.5665 13.5116 16.9499 13.665 16.374C13.888 15.542 14.543 14.887 15.375 14.665C15.952 14.51 16.571 14.539 17.117 14.565L17.1474 14.5664C17.3312 14.5749 17.5059 14.583 17.667 14.583C19.057 14.583 20.1945 13.4787 20.248 12.1015L20.248 9.273C20.248 6.38201 20.248 4.93099 19.563 4.07C19.364 3.82 19.129 3.599 18.862 3.411C17.9251 2.75 16.3691 2.75 13.2701 2.75H12.997C12.583 2.75 12.247 2.414 12.247 2C12.247 1.586 12.583 1.25 12.997 1.25H13.2701C16.685 1.25 18.4001 1.25 19.726 2.185C20.1091 2.455 20.449 2.775 20.736 3.136C21.747 4.407 21.747 6.03299 21.747 9.27298L21.747 11.933C21.749 11.9551 21.75 11.9774 21.75 12C21.75 12.0526 21.749 12.105 21.747 12.1571C21.7463 14.9883 21.7274 16.4556 21.225 17.722C20.39 19.828 18.6341 21.484 16.4071 22.266C15.1592 22.704 13.714 22.7456 11.0577 22.7496C11.0382 22.7499 11.0186 22.75 10.999 22.75C10.7376 22.7503 10.4648 22.75 10.1791 22.75L10.1809 22.749ZM15.912 20.851C15.443 21.0155 14.9065 21.1121 14.2237 21.169C14.7614 20.4775 15.082 19.6091 15.082 18.667C15.082 18.4764 15.0734 18.2815 15.0649 18.0911L15.063 18.048L15.0628 18.0447C15.0419 17.5877 15.0202 17.1152 15.114 16.763C15.199 16.448 15.447 16.199 15.763 16.115C16.1111 16.0211 16.5785 16.0425 17.0317 16.0633L17.047 16.064L17.0872 16.0658C17.2786 16.0743 17.4754 16.083 17.667 16.083C18.6203 16.083 19.4985 15.7546 20.1941 15.2049C20.1415 16.038 20.0375 16.6513 19.8321 17.17C19.1581 18.871 17.729 20.213 15.912 20.851Z"
fill="#161616"
/>
</svg>

<p
slot="trail-element"
className="text-[var(--text-secondary-paragraph,#6C737F)] text-[16px] leading-[24px] font-[400]"
>
+99
</p>
</DgaMenuItem>
<DgaMenuItem label="Item Label" hasTrailElement hasLeadIcon>
<svg
slot="lead-icon"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M7.75 2C7.75 1.58579 7.41421 1.25 7 1.25C6.58579 1.25 6.25 1.58579 6.25 2V5.25H3C2.58579 5.25 2.25 5.58579 2.25 6C2.25 6.41421 2.58579 6.75 3 6.75H6.25V10C6.25 10.4142 6.58579 10.75 7 10.75C7.41421 10.75 7.75 10.4142 7.75 10V6.75H11C11.4142 6.75 11.75 6.41421 11.75 6C11.75 5.58579 11.4142 5.25 11 5.25H7.75V2Z"
fill="#161616"
/>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M10.1809 22.749C8.29902 22.749 7.35404 22.749 6.51505 22.454C5.15405 21.976 4.08106 20.963 3.56906 19.673C3.24806 18.864 3.24805 17.967 3.24805 16.181V11.999C3.24805 11.585 3.58405 11.249 3.99805 11.249C4.41205 11.249 4.74805 11.585 4.74805 11.999V16.181C4.74805 17.777 4.74805 18.578 4.96305 19.121C5.31405 20.007 6.06105 20.706 7.01105 21.04C7.60904 21.25 8.46804 21.25 10.18 21.25C10.4543 21.25 10.7164 21.25 10.967 21.2497C10.9779 21.2492 10.9889 21.249 11 21.249C12.424 21.249 13.583 20.09 13.583 18.666C13.583 18.5059 13.575 18.3334 13.5666 18.151L13.5647 18.1111C13.5398 17.5665 13.5116 16.9499 13.665 16.374C13.888 15.542 14.543 14.887 15.375 14.665C15.952 14.51 16.571 14.539 17.117 14.565L17.1474 14.5664C17.3312 14.5749 17.5059 14.583 17.667 14.583C19.057 14.583 20.1945 13.4787 20.248 12.1015L20.248 9.273C20.248 6.38201 20.248 4.93099 19.563 4.07C19.364 3.82 19.129 3.599 18.862 3.411C17.9251 2.75 16.3691 2.75 13.2701 2.75H12.997C12.583 2.75 12.247 2.414 12.247 2C12.247 1.586 12.583 1.25 12.997 1.25H13.2701C16.685 1.25 18.4001 1.25 19.726 2.185C20.1091 2.455 20.449 2.775 20.736 3.136C21.747 4.407 21.747 6.03299 21.747 9.27298L21.747 11.933C21.749 11.9551 21.75 11.9774 21.75 12C21.75 12.0526 21.749 12.105 21.747 12.1571C21.7463 14.9883 21.7274 16.4556 21.225 17.722C20.39 19.828 18.6341 21.484 16.4071 22.266C15.1592 22.704 13.714 22.7456 11.0577 22.7496C11.0382 22.7499 11.0186 22.75 10.999 22.75C10.7376 22.7503 10.4648 22.75 10.1791 22.75L10.1809 22.749ZM15.912 20.851C15.443 21.0155 14.9065 21.1121 14.2237 21.169C14.7614 20.4775 15.082 19.6091 15.082 18.667C15.082 18.4764 15.0734 18.2815 15.0649 18.0911L15.063 18.048L15.0628 18.0447C15.0419 17.5877 15.0202 17.1152 15.114 16.763C15.199 16.448 15.447 16.199 15.763 16.115C16.1111 16.0211 16.5785 16.0425 17.0317 16.0633L17.047 16.064L17.0872 16.0658C17.2786 16.0743 17.4754 16.083 17.667 16.083C18.6203 16.083 19.4985 15.7546 20.1941 15.2049C20.1415 16.038 20.0375 16.6513 19.8321 17.17C19.1581 18.871 17.729 20.213 15.912 20.851Z"
fill="#161616"
/>
</svg>

<p
slot="trail-element"
className="text-[var(--text-secondary-paragraph,#6C737F)] text-[16px] leading-[24px] font-[400]"
>
+99
</p>
</DgaMenuItem>
</DgaMenuGroup>

<DgaDivider />

<DgaMenuGroup groupLabel="GROUP LABEL">
<DgaMenuItem label="Item Label" hasTrailElement hasLeadIcon>
<svg
slot="lead-icon"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M7.75 2C7.75 1.58579 7.41421 1.25 7 1.25C6.58579 1.25 6.25 1.58579 6.25 2V5.25H3C2.58579 5.25 2.25 5.58579 2.25 6C2.25 6.41421 2.58579 6.75 3 6.75H6.25V10C6.25 10.4142 6.58579 10.75 7 10.75C7.41421 10.75 7.75 10.4142 7.75 10V6.75H11C11.4142 6.75 11.75 6.41421 11.75 6C11.75 5.58579 11.4142 5.25 11 5.25H7.75V2Z"
fill="#161616"
/>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M10.1809 22.749C8.29902 22.749 7.35404 22.749 6.51505 22.454C5.15405 21.976 4.08106 20.963 3.56906 19.673C3.24806 18.864 3.24805 17.967 3.24805 16.181V11.999C3.24805 11.585 3.58405 11.249 3.99805 11.249C4.41205 11.249 4.74805 11.585 4.74805 11.999V16.181C4.74805 17.777 4.74805 18.578 4.96305 19.121C5.31405 20.007 6.06105 20.706 7.01105 21.04C7.60904 21.25 8.46804 21.25 10.18 21.25C10.4543 21.25 10.7164 21.25 10.967 21.2497C10.9779 21.2492 10.9889 21.249 11 21.249C12.424 21.249 13.583 20.09 13.583 18.666C13.583 18.5059 13.575 18.3334 13.5666 18.151L13.5647 18.1111C13.5398 17.5665 13.5116 16.9499 13.665 16.374C13.888 15.542 14.543 14.887 15.375 14.665C15.952 14.51 16.571 14.539 17.117 14.565L17.1474 14.5664C17.3312 14.5749 17.5059 14.583 17.667 14.583C19.057 14.583 20.1945 13.4787 20.248 12.1015L20.248 9.273C20.248 6.38201 20.248 4.93099 19.563 4.07C19.364 3.82 19.129 3.599 18.862 3.411C17.9251 2.75 16.3691 2.75 13.2701 2.75H12.997C12.583 2.75 12.247 2.414 12.247 2C12.247 1.586 12.583 1.25 12.997 1.25H13.2701C16.685 1.25 18.4001 1.25 19.726 2.185C20.1091 2.455 20.449 2.775 20.736 3.136C21.747 4.407 21.747 6.03299 21.747 9.27298L21.747 11.933C21.749 11.9551 21.75 11.9774 21.75 12C21.75 12.0526 21.749 12.105 21.747 12.1571C21.7463 14.9883 21.7274 16.4556 21.225 17.722C20.39 19.828 18.6341 21.484 16.4071 22.266C15.1592 22.704 13.714 22.7456 11.0577 22.7496C11.0382 22.7499 11.0186 22.75 10.999 22.75C10.7376 22.7503 10.4648 22.75 10.1791 22.75L10.1809 22.749ZM15.912 20.851C15.443 21.0155 14.9065 21.1121 14.2237 21.169C14.7614 20.4775 15.082 19.6091 15.082 18.667C15.082 18.4764 15.0734 18.2815 15.0649 18.0911L15.063 18.048L15.0628 18.0447C15.0419 17.5877 15.0202 17.1152 15.114 16.763C15.199 16.448 15.447 16.199 15.763 16.115C16.1111 16.0211 16.5785 16.0425 17.0317 16.0633L17.047 16.064L17.0872 16.0658C17.2786 16.0743 17.4754 16.083 17.667 16.083C18.6203 16.083 19.4985 15.7546 20.1941 15.2049C20.1415 16.038 20.0375 16.6513 19.8321 17.17C19.1581 18.871 17.729 20.213 15.912 20.851Z"
fill="#161616"
/>
</svg>
<svg
slot="trail-element"
width="12"
height="9"
viewBox="0 0 12 9"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M11.8307 4.50161C11.8307 4.25257 11.7203 4.02153 11.6157 3.84804C11.5029 3.66083 11.3511 3.46755 11.1846 3.2791C10.8506 2.90105 10.4148 2.49506 9.99192 2.12782C9.56652 1.75841 9.14259 1.41827 8.82591 1.17109C8.6673 1.04729 8.53498 0.946335 8.44205 0.876128C8.39557 0.841015 8.3589 0.813567 8.33369 0.79477L8.30464 0.773181L8.29693 0.767478L8.29426 0.765505C8.07193 0.60173 7.75864 0.648991 7.59486 0.871325C7.43109 1.09365 7.47855 1.40664 7.70086 1.57042L7.70935 1.57669L7.73605 1.59654C7.75966 1.61414 7.79461 1.6403 7.83927 1.67404C7.92863 1.74154 8.05672 1.83927 8.21061 1.95939C8.51892 2.20003 8.92832 2.52863 9.33625 2.88287C9.74667 3.23926 10.1442 3.61181 10.4352 3.94119C10.4536 3.96203 10.4714 3.9825 10.4886 4.0026L0.664062 4.00261C0.38792 4.00261 0.164062 4.22646 0.164062 4.5026C0.164063 4.77875 0.38792 5.00261 0.664063 5.00261L10.4869 5.0026C10.4703 5.02207 10.453 5.04189 10.4352 5.06204C10.1442 5.39142 9.74667 5.76397 9.33625 6.12037C8.92832 6.4746 8.51893 6.8032 8.21062 7.04385C8.05672 7.16396 7.92863 7.26169 7.83927 7.3292C7.79461 7.36294 7.75966 7.3891 7.73605 7.4067L7.70935 7.42655L7.70086 7.43282C7.47856 7.5966 7.4311 7.90959 7.59486 8.13191C7.75864 8.35425 8.07193 8.40151 8.29426 8.23773L8.29693 8.23576L8.30464 8.23005L8.33369 8.20847C8.3589 8.18967 8.39557 8.16222 8.44205 8.12711C8.53498 8.0569 8.6673 7.95594 8.82591 7.83215C9.14259 7.58496 9.56652 7.24482 9.99192 6.87542C10.4148 6.50817 10.8506 6.10219 11.1846 5.72414C11.3511 5.53569 11.5029 5.3424 11.6157 5.15519C11.7197 4.98275 11.8294 4.75343 11.8307 4.5061"
fill="#161616"
/>
</svg>
</DgaMenuItem>

<DgaMenuItem label="Item Label" hasTrailElement hasLeadIcon>
<svg
slot="lead-icon"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M7.75 2C7.75 1.58579 7.41421 1.25 7 1.25C6.58579 1.25 6.25 1.58579 6.25 2V5.25H3C2.58579 5.25 2.25 5.58579 2.25 6C2.25 6.41421 2.58579 6.75 3 6.75H6.25V10C6.25 10.4142 6.58579 10.75 7 10.75C7.41421 10.75 7.75 10.4142 7.75 10V6.75H11C11.4142 6.75 11.75 6.41421 11.75 6C11.75 5.58579 11.4142 5.25 11 5.25H7.75V2Z"
fill="#161616"
/>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M10.1809 22.749C8.29902 22.749 7.35404 22.749 6.51505 22.454C5.15405 21.976 4.08106 20.963 3.56906 19.673C3.24806 18.864 3.24805 17.967 3.24805 16.181V11.999C3.24805 11.585 3.58405 11.249 3.99805 11.249C4.41205 11.249 4.74805 11.585 4.74805 11.999V16.181C4.74805 17.777 4.74805 18.578 4.96305 19.121C5.31405 20.007 6.06105 20.706 7.01105 21.04C7.60904 21.25 8.46804 21.25 10.18 21.25C10.4543 21.25 10.7164 21.25 10.967 21.2497C10.9779 21.2492 10.9889 21.249 11 21.249C12.424 21.249 13.583 20.09 13.583 18.666C13.583 18.5059 13.575 18.3334 13.5666 18.151L13.5647 18.1111C13.5398 17.5665 13.5116 16.9499 13.665 16.374C13.888 15.542 14.543 14.887 15.375 14.665C15.952 14.51 16.571 14.539 17.117 14.565L17.1474 14.5664C17.3312 14.5749 17.5059 14.583 17.667 14.583C19.057 14.583 20.1945 13.4787 20.248 12.1015L20.248 9.273C20.248 6.38201 20.248 4.93099 19.563 4.07C19.364 3.82 19.129 3.599 18.862 3.411C17.9251 2.75 16.3691 2.75 13.2701 2.75H12.997C12.583 2.75 12.247 2.414 12.247 2C12.247 1.586 12.583 1.25 12.997 1.25H13.2701C16.685 1.25 18.4001 1.25 19.726 2.185C20.1091 2.455 20.449 2.775 20.736 3.136C21.747 4.407 21.747 6.03299 21.747 9.27298L21.747 11.933C21.749 11.9551 21.75 11.9774 21.75 12C21.75 12.0526 21.749 12.105 21.747 12.1571C21.7463 14.9883 21.7274 16.4556 21.225 17.722C20.39 19.828 18.6341 21.484 16.4071 22.266C15.1592 22.704 13.714 22.7456 11.0577 22.7496C11.0382 22.7499 11.0186 22.75 10.999 22.75C10.7376 22.7503 10.4648 22.75 10.1791 22.75L10.1809 22.749ZM15.912 20.851C15.443 21.0155 14.9065 21.1121 14.2237 21.169C14.7614 20.4775 15.082 19.6091 15.082 18.667C15.082 18.4764 15.0734 18.2815 15.0649 18.0911L15.063 18.048L15.0628 18.0447C15.0419 17.5877 15.0202 17.1152 15.114 16.763C15.199 16.448 15.447 16.199 15.763 16.115C16.1111 16.0211 16.5785 16.0425 17.0317 16.0633L17.047 16.064L17.0872 16.0658C17.2786 16.0743 17.4754 16.083 17.667 16.083C18.6203 16.083 19.4985 15.7546 20.1941 15.2049C20.1415 16.038 20.0375 16.6513 19.8321 17.17C19.1581 18.871 17.729 20.213 15.912 20.851Z"
fill="#161616"
/>
</svg>
<svg
slot="trail-element"
width="12"
height="9"
viewBox="0 0 12 9"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M11.8307 4.50161C11.8307 4.25257 11.7203 4.02153 11.6157 3.84804C11.5029 3.66083 11.3511 3.46755 11.1846 3.2791C10.8506 2.90105 10.4148 2.49506 9.99192 2.12782C9.56652 1.75841 9.14259 1.41827 8.82591 1.17109C8.6673 1.04729 8.53498 0.946335 8.44205 0.876128C8.39557 0.841015 8.3589 0.813567 8.33369 0.79477L8.30464 0.773181L8.29693 0.767478L8.29426 0.765505C8.07193 0.60173 7.75864 0.648991 7.59486 0.871325C7.43109 1.09365 7.47855 1.40664 7.70086 1.57042L7.70935 1.57669L7.73605 1.59654C7.75966 1.61414 7.79461 1.6403 7.83927 1.67404C7.92863 1.74154 8.05672 1.83927 8.21061 1.95939C8.51892 2.20003 8.92832 2.52863 9.33625 2.88287C9.74667 3.23926 10.1442 3.61181 10.4352 3.94119C10.4536 3.96203 10.4714 3.9825 10.4886 4.0026L0.664062 4.00261C0.38792 4.00261 0.164062 4.22646 0.164062 4.5026C0.164063 4.77875 0.38792 5.00261 0.664063 5.00261L10.4869 5.0026C10.4703 5.02207 10.453 5.04189 10.4352 5.06204C10.1442 5.39142 9.74667 5.76397 9.33625 6.12037C8.92832 6.4746 8.51893 6.8032 8.21062 7.04385C8.05672 7.16396 7.92863 7.26169 7.83927 7.3292C7.79461 7.36294 7.75966 7.3891 7.73605 7.4067L7.70935 7.42655L7.70086 7.43282C7.47856 7.5966 7.4311 7.90959 7.59486 8.13191C7.75864 8.35425 8.07193 8.40151 8.29426 8.23773L8.29693 8.23576L8.30464 8.23005L8.33369 8.20847C8.3589 8.18967 8.39557 8.16222 8.44205 8.12711C8.53498 8.0569 8.6673 7.95594 8.82591 7.83215C9.14259 7.58496 9.56652 7.24482 9.99192 6.87542C10.4148 6.50817 10.8506 6.10219 11.1846 5.72414C11.3511 5.53569 11.5029 5.3424 11.6157 5.15519C11.7197 4.98275 11.8294 4.75343 11.8307 4.5061"
fill="#161616"
/>
</svg>
</DgaMenuItem>
<DgaMenuItem label="Item Label" hasTrailElement hasLeadIcon>
<svg
slot="lead-icon"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M7.75 2C7.75 1.58579 7.41421 1.25 7 1.25C6.58579 1.25 6.25 1.58579 6.25 2V5.25H3C2.58579 5.25 2.25 5.58579 2.25 6C2.25 6.41421 2.58579 6.75 3 6.75H6.25V10C6.25 10.4142 6.58579 10.75 7 10.75C7.41421 10.75 7.75 10.4142 7.75 10V6.75H11C11.4142 6.75 11.75 6.41421 11.75 6C11.75 5.58579 11.4142 5.25 11 5.25H7.75V2Z"
fill="#161616"
/>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M10.1809 22.749C8.29902 22.749 7.35404 22.749 6.51505 22.454C5.15405 21.976 4.08106 20.963 3.56906 19.673C3.24806 18.864 3.24805 17.967 3.24805 16.181V11.999C3.24805 11.585 3.58405 11.249 3.99805 11.249C4.41205 11.249 4.74805 11.585 4.74805 11.999V16.181C4.74805 17.777 4.74805 18.578 4.96305 19.121C5.31405 20.007 6.06105 20.706 7.01105 21.04C7.60904 21.25 8.46804 21.25 10.18 21.25C10.4543 21.25 10.7164 21.25 10.967 21.2497C10.9779 21.2492 10.9889 21.249 11 21.249C12.424 21.249 13.583 20.09 13.583 18.666C13.583 18.5059 13.575 18.3334 13.5666 18.151L13.5647 18.1111C13.5398 17.5665 13.5116 16.9499 13.665 16.374C13.888 15.542 14.543 14.887 15.375 14.665C15.952 14.51 16.571 14.539 17.117 14.565L17.1474 14.5664C17.3312 14.5749 17.5059 14.583 17.667 14.583C19.057 14.583 20.1945 13.4787 20.248 12.1015L20.248 9.273C20.248 6.38201 20.248 4.93099 19.563 4.07C19.364 3.82 19.129 3.599 18.862 3.411C17.9251 2.75 16.3691 2.75 13.2701 2.75H12.997C12.583 2.75 12.247 2.414 12.247 2C12.247 1.586 12.583 1.25 12.997 1.25H13.2701C16.685 1.25 18.4001 1.25 19.726 2.185C20.1091 2.455 20.449 2.775 20.736 3.136C21.747 4.407 21.747 6.03299 21.747 9.27298L21.747 11.933C21.749 11.9551 21.75 11.9774 21.75 12C21.75 12.0526 21.749 12.105 21.747 12.1571C21.7463 14.9883 21.7274 16.4556 21.225 17.722C20.39 19.828 18.6341 21.484 16.4071 22.266C15.1592 22.704 13.714 22.7456 11.0577 22.7496C11.0382 22.7499 11.0186 22.75 10.999 22.75C10.7376 22.7503 10.4648 22.75 10.1791 22.75L10.1809 22.749ZM15.912 20.851C15.443 21.0155 14.9065 21.1121 14.2237 21.169C14.7614 20.4775 15.082 19.6091 15.082 18.667C15.082 18.4764 15.0734 18.2815 15.0649 18.0911L15.063 18.048L15.0628 18.0447C15.0419 17.5877 15.0202 17.1152 15.114 16.763C15.199 16.448 15.447 16.199 15.763 16.115C16.1111 16.0211 16.5785 16.0425 17.0317 16.0633L17.047 16.064L17.0872 16.0658C17.2786 16.0743 17.4754 16.083 17.667 16.083C18.6203 16.083 19.4985 15.7546 20.1941 15.2049C20.1415 16.038 20.0375 16.6513 19.8321 17.17C19.1581 18.871 17.729 20.213 15.912 20.851Z"
fill="#161616"
/>
</svg>
<svg
slot="trail-element"
width="12"
height="9"
viewBox="0 0 12 9"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M11.8307 4.50161C11.8307 4.25257 11.7203 4.02153 11.6157 3.84804C11.5029 3.66083 11.3511 3.46755 11.1846 3.2791C10.8506 2.90105 10.4148 2.49506 9.99192 2.12782C9.56652 1.75841 9.14259 1.41827 8.82591 1.17109C8.6673 1.04729 8.53498 0.946335 8.44205 0.876128C8.39557 0.841015 8.3589 0.813567 8.33369 0.79477L8.30464 0.773181L8.29693 0.767478L8.29426 0.765505C8.07193 0.60173 7.75864 0.648991 7.59486 0.871325C7.43109 1.09365 7.47855 1.40664 7.70086 1.57042L7.70935 1.57669L7.73605 1.59654C7.75966 1.61414 7.79461 1.6403 7.83927 1.67404C7.92863 1.74154 8.05672 1.83927 8.21061 1.95939C8.51892 2.20003 8.92832 2.52863 9.33625 2.88287C9.74667 3.23926 10.1442 3.61181 10.4352 3.94119C10.4536 3.96203 10.4714 3.9825 10.4886 4.0026L0.664062 4.00261C0.38792 4.00261 0.164062 4.22646 0.164062 4.5026C0.164063 4.77875 0.38792 5.00261 0.664063 5.00261L10.4869 5.0026C10.4703 5.02207 10.453 5.04189 10.4352 5.06204C10.1442 5.39142 9.74667 5.76397 9.33625 6.12037C8.92832 6.4746 8.51893 6.8032 8.21062 7.04385C8.05672 7.16396 7.92863 7.26169 7.83927 7.3292C7.79461 7.36294 7.75966 7.3891 7.73605 7.4067L7.70935 7.42655L7.70086 7.43282C7.47856 7.5966 7.4311 7.90959 7.59486 8.13191C7.75864 8.35425 8.07193 8.40151 8.29426 8.23773L8.29693 8.23576L8.30464 8.23005L8.33369 8.20847C8.3589 8.18967 8.39557 8.16222 8.44205 8.12711C8.53498 8.0569 8.6673 7.95594 8.82591 7.83215C9.14259 7.58496 9.56652 7.24482 9.99192 6.87542C10.4148 6.50817 10.8506 6.10219 11.1846 5.72414C11.3511 5.53569 11.5029 5.3424 11.6157 5.15519C11.7197 4.98275 11.8294 4.75343 11.8307 4.5061"
fill="#161616"
/>
</svg>
</DgaMenuItem>
</DgaMenuGroup>

<DgaDivider />

<DgaMenuGroup groupLabel="GROUP LABEL">
<DgaMenuItem label="Item Label" hasTrailElement hasLeadIcon>
<svg
slot="lead-icon"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M7.75 2C7.75 1.58579 7.41421 1.25 7 1.25C6.58579 1.25 6.25 1.58579 6.25 2V5.25H3C2.58579 5.25 2.25 5.58579 2.25 6C2.25 6.41421 2.58579 6.75 3 6.75H6.25V10C6.25 10.4142 6.58579 10.75 7 10.75C7.41421 10.75 7.75 10.4142 7.75 10V6.75H11C11.4142 6.75 11.75 6.41421 11.75 6C11.75 5.58579 11.4142 5.25 11 5.25H7.75V2Z"
fill="#161616"
/>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M10.1809 22.749C8.29902 22.749 7.35404 22.749 6.51505 22.454C5.15405 21.976 4.08106 20.963 3.56906 19.673C3.24806 18.864 3.24805 17.967 3.24805 16.181V11.999C3.24805 11.585 3.58405 11.249 3.99805 11.249C4.41205 11.249 4.74805 11.585 4.74805 11.999V16.181C4.74805 17.777 4.74805 18.578 4.96305 19.121C5.31405 20.007 6.06105 20.706 7.01105 21.04C7.60904 21.25 8.46804 21.25 10.18 21.25C10.4543 21.25 10.7164 21.25 10.967 21.2497C10.9779 21.2492 10.9889 21.249 11 21.249C12.424 21.249 13.583 20.09 13.583 18.666C13.583 18.5059 13.575 18.3334 13.5666 18.151L13.5647 18.1111C13.5398 17.5665 13.5116 16.9499 13.665 16.374C13.888 15.542 14.543 14.887 15.375 14.665C15.952 14.51 16.571 14.539 17.117 14.565L17.1474 14.5664C17.3312 14.5749 17.5059 14.583 17.667 14.583C19.057 14.583 20.1945 13.4787 20.248 12.1015L20.248 9.273C20.248 6.38201 20.248 4.93099 19.563 4.07C19.364 3.82 19.129 3.599 18.862 3.411C17.9251 2.75 16.3691 2.75 13.2701 2.75H12.997C12.583 2.75 12.247 2.414 12.247 2C12.247 1.586 12.583 1.25 12.997 1.25H13.2701C16.685 1.25 18.4001 1.25 19.726 2.185C20.1091 2.455 20.449 2.775 20.736 3.136C21.747 4.407 21.747 6.03299 21.747 9.27298L21.747 11.933C21.749 11.9551 21.75 11.9774 21.75 12C21.75 12.0526 21.749 12.105 21.747 12.1571C21.7463 14.9883 21.7274 16.4556 21.225 17.722C20.39 19.828 18.6341 21.484 16.4071 22.266C15.1592 22.704 13.714 22.7456 11.0577 22.7496C11.0382 22.7499 11.0186 22.75 10.999 22.75C10.7376 22.7503 10.4648 22.75 10.1791 22.75L10.1809 22.749ZM15.912 20.851C15.443 21.0155 14.9065 21.1121 14.2237 21.169C14.7614 20.4775 15.082 19.6091 15.082 18.667C15.082 18.4764 15.0734 18.2815 15.0649 18.0911L15.063 18.048L15.0628 18.0447C15.0419 17.5877 15.0202 17.1152 15.114 16.763C15.199 16.448 15.447 16.199 15.763 16.115C16.1111 16.0211 16.5785 16.0425 17.0317 16.0633L17.047 16.064L17.0872 16.0658C17.2786 16.0743 17.4754 16.083 17.667 16.083C18.6203 16.083 19.4985 15.7546 20.1941 15.2049C20.1415 16.038 20.0375 16.6513 19.8321 17.17C19.1581 18.871 17.729 20.213 15.912 20.851Z"
fill="#161616"
/>
</svg>

<svg
slot="trail-element"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M19.5179 5.95748C19.8175 6.24349 19.8285 6.71823 19.5425 7.01786L9.04252 18.0179C8.90308 18.1639 8.71064 18.2476 8.50872 18.25C8.3068 18.2523 8.11246 18.1731 7.96967 18.0303L4.46967 14.5303C4.17678 14.2374 4.17678 13.7626 4.46967 13.4697C4.76256 13.1768 5.23744 13.1768 5.53033 13.4697L8.48752 16.4269L18.4575 5.98214C18.7435 5.68252 19.2182 5.67148 19.5179 5.95748Z"
fill="#161616"
/>
</svg>
</DgaMenuItem>

<DgaMenuItem label="Item Label" hasTrailElement hasLeadIcon>
<svg
slot="lead-icon"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M7.75 2C7.75 1.58579 7.41421 1.25 7 1.25C6.58579 1.25 6.25 1.58579 6.25 2V5.25H3C2.58579 5.25 2.25 5.58579 2.25 6C2.25 6.41421 2.58579 6.75 3 6.75H6.25V10C6.25 10.4142 6.58579 10.75 7 10.75C7.41421 10.75 7.75 10.4142 7.75 10V6.75H11C11.4142 6.75 11.75 6.41421 11.75 6C11.75 5.58579 11.4142 5.25 11 5.25H7.75V2Z"
fill="#161616"
/>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M10.1809 22.749C8.29902 22.749 7.35404 22.749 6.51505 22.454C5.15405 21.976 4.08106 20.963 3.56906 19.673C3.24806 18.864 3.24805 17.967 3.24805 16.181V11.999C3.24805 11.585 3.58405 11.249 3.99805 11.249C4.41205 11.249 4.74805 11.585 4.74805 11.999V16.181C4.74805 17.777 4.74805 18.578 4.96305 19.121C5.31405 20.007 6.06105 20.706 7.01105 21.04C7.60904 21.25 8.46804 21.25 10.18 21.25C10.4543 21.25 10.7164 21.25 10.967 21.2497C10.9779 21.2492 10.9889 21.249 11 21.249C12.424 21.249 13.583 20.09 13.583 18.666C13.583 18.5059 13.575 18.3334 13.5666 18.151L13.5647 18.1111C13.5398 17.5665 13.5116 16.9499 13.665 16.374C13.888 15.542 14.543 14.887 15.375 14.665C15.952 14.51 16.571 14.539 17.117 14.565L17.1474 14.5664C17.3312 14.5749 17.5059 14.583 17.667 14.583C19.057 14.583 20.1945 13.4787 20.248 12.1015L20.248 9.273C20.248 6.38201 20.248 4.93099 19.563 4.07C19.364 3.82 19.129 3.599 18.862 3.411C17.9251 2.75 16.3691 2.75 13.2701 2.75H12.997C12.583 2.75 12.247 2.414 12.247 2C12.247 1.586 12.583 1.25 12.997 1.25H13.2701C16.685 1.25 18.4001 1.25 19.726 2.185C20.1091 2.455 20.449 2.775 20.736 3.136C21.747 4.407 21.747 6.03299 21.747 9.27298L21.747 11.933C21.749 11.9551 21.75 11.9774 21.75 12C21.75 12.0526 21.749 12.105 21.747 12.1571C21.7463 14.9883 21.7274 16.4556 21.225 17.722C20.39 19.828 18.6341 21.484 16.4071 22.266C15.1592 22.704 13.714 22.7456 11.0577 22.7496C11.0382 22.7499 11.0186 22.75 10.999 22.75C10.7376 22.7503 10.4648 22.75 10.1791 22.75L10.1809 22.749ZM15.912 20.851C15.443 21.0155 14.9065 21.1121 14.2237 21.169C14.7614 20.4775 15.082 19.6091 15.082 18.667C15.082 18.4764 15.0734 18.2815 15.0649 18.0911L15.063 18.048L15.0628 18.0447C15.0419 17.5877 15.0202 17.1152 15.114 16.763C15.199 16.448 15.447 16.199 15.763 16.115C16.1111 16.0211 16.5785 16.0425 17.0317 16.0633L17.047 16.064L17.0872 16.0658C17.2786 16.0743 17.4754 16.083 17.667 16.083C18.6203 16.083 19.4985 15.7546 20.1941 15.2049C20.1415 16.038 20.0375 16.6513 19.8321 17.17C19.1581 18.871 17.729 20.213 15.912 20.851Z"
fill="#161616"
/>
</svg>

<svg
slot="trail-element"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M19.5179 5.95748C19.8175 6.24349 19.8285 6.71823 19.5425 7.01786L9.04252 18.0179C8.90308 18.1639 8.71064 18.2476 8.50872 18.25C8.3068 18.2523 8.11246 18.1731 7.96967 18.0303L4.46967 14.5303C4.17678 14.2374 4.17678 13.7626 4.46967 13.4697C4.76256 13.1768 5.23744 13.1768 5.53033 13.4697L8.48752 16.4269L18.4575 5.98214C18.7435 5.68252 19.2182 5.67148 19.5179 5.95748Z"
fill="#161616"
/>
</svg>
</DgaMenuItem>

<DgaMenuItem label="Item Label" hasTrailElement hasLeadIcon>
<svg
slot="lead-icon"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
d="M7.75 2C7.75 1.58579 7.41421 1.25 7 1.25C6.58579 1.25 6.25 1.58579 6.25 2V5.25H3C2.58579 5.25 2.25 5.58579 2.25 6C2.25 6.41421 2.58579 6.75 3 6.75H6.25V10C6.25 10.4142 6.58579 10.75 7 10.75C7.41421 10.75 7.75 10.4142 7.75 10V6.75H11C11.4142 6.75 11.75 6.41421 11.75 6C11.75 5.58579 11.4142 5.25 11 5.25H7.75V2Z"
fill="#161616"
/>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M10.1809 22.749C8.29902 22.749 7.35404 22.749 6.51505 22.454C5.15405 21.976 4.08106 20.963 3.56906 19.673C3.24806 18.864 3.24805 17.967 3.24805 16.181V11.999C3.24805 11.585 3.58405 11.249 3.99805 11.249C4.41205 11.249 4.74805 11.585 4.74805 11.999V16.181C4.74805 17.777 4.74805 18.578 4.96305 19.121C5.31405 20.007 6.06105 20.706 7.01105 21.04C7.60904 21.25 8.46804 21.25 10.18 21.25C10.4543 21.25 10.7164 21.25 10.967 21.2497C10.9779 21.2492 10.9889 21.249 11 21.249C12.424 21.249 13.583 20.09 13.583 18.666C13.583 18.5059 13.575 18.3334 13.5666 18.151L13.5647 18.1111C13.5398 17.5665 13.5116 16.9499 13.665 16.374C13.888 15.542 14.543 14.887 15.375 14.665C15.952 14.51 16.571 14.539 17.117 14.565L17.1474 14.5664C17.3312 14.5749 17.5059 14.583 17.667 14.583C19.057 14.583 20.1945 13.4787 20.248 12.1015L20.248 9.273C20.248 6.38201 20.248 4.93099 19.563 4.07C19.364 3.82 19.129 3.599 18.862 3.411C17.9251 2.75 16.3691 2.75 13.2701 2.75H12.997C12.583 2.75 12.247 2.414 12.247 2C12.247 1.586 12.583 1.25 12.997 1.25H13.2701C16.685 1.25 18.4001 1.25 19.726 2.185C20.1091 2.455 20.449 2.775 20.736 3.136C21.747 4.407 21.747 6.03299 21.747 9.27298L21.747 11.933C21.749 11.9551 21.75 11.9774 21.75 12C21.75 12.0526 21.749 12.105 21.747 12.1571C21.7463 14.9883 21.7274 16.4556 21.225 17.722C20.39 19.828 18.6341 21.484 16.4071 22.266C15.1592 22.704 13.714 22.7456 11.0577 22.7496C11.0382 22.7499 11.0186 22.75 10.999 22.75C10.7376 22.7503 10.4648 22.75 10.1791 22.75L10.1809 22.749ZM15.912 20.851C15.443 21.0155 14.9065 21.1121 14.2237 21.169C14.7614 20.4775 15.082 19.6091 15.082 18.667C15.082 18.4764 15.0734 18.2815 15.0649 18.0911L15.063 18.048L15.0628 18.0447C15.0419 17.5877 15.0202 17.1152 15.114 16.763C15.199 16.448 15.447 16.199 15.763 16.115C16.1111 16.0211 16.5785 16.0425 17.0317 16.0633L17.047 16.064L17.0872 16.0658C17.2786 16.0743 17.4754 16.083 17.667 16.083C18.6203 16.083 19.4985 15.7546 20.1941 15.2049C20.1415 16.038 20.0375 16.6513 19.8321 17.17C19.1581 18.871 17.729 20.213 15.912 20.851Z"
fill="#161616"
/>
</svg>

<svg
slot="trail-element"
width="24"
height="24"
viewBox="0 0 24 24"
fill="none"
xmlns="http://www.w3.org/2000/svg"
>
<path
fill-rule="evenodd"
clip-rule="evenodd"
d="M19.5179 5.95748C19.8175 6.24349 19.8285 6.71823 19.5425 7.01786L9.04252 18.0179C8.90308 18.1639 8.71064 18.2476 8.50872 18.25C8.3068 18.2523 8.11246 18.1731 7.96967 18.0303L4.46967 14.5303C4.17678 14.2374 4.17678 13.7626 4.46967 13.4697C4.76256 13.1768 5.23744 13.1768 5.53033 13.4697L8.48752 16.4269L18.4575 5.98214C18.7435 5.68252 19.2182 5.67148 19.5179 5.95748Z"
fill="#161616"
/>
</svg>
</DgaMenuItem>
</DgaMenuGroup>

<DgaDivider />
</DgaSlideoutMenuItems>

<DgaDivider />

<DgaSlideoutMenuActions>
<DgaButton label="action" />
<DgaButton label="action" />
</DgaSlideoutMenuActions>
</DgaSlideoutMenu>
````

---

## `/guidelines/components/navigational/tabs`

Chunk `index-rIR_KnNA.js` · imports: `platformscode-new-react` · elements: `TabsComponent`

````jsx
import { DgaTabs as TabsComponent } from "platformscode-new-react";

<TabsComponent
divider
external
orientation="horizontal"
size="md"
tabsList={tabsList}
/>
````

---

## `/guidelines/components/search-and-filters/filtration`

Chunk `index-CaJQyrIz.js` · imports: none shown · elements: `DgaFiltration`

````jsx
<DgaFiltration
  buttonLabel="Filter Items"
  filterBlocks={[
    {
      id: 'status',
      label: 'Status',
      options: [
        {
          id: 'active',
          label: 'Active',
          value: 'active'
        },
        {
          id: 'inactive',
          label: 'Inactive',
          value: 'inactive'
        },
        {
          id: 'pending',
          label: 'Pending',
          value: 'pending'
        },
        {
          id: 'archived',
          label: 'Archived',
          value: 'archived'
        },
        {
          id: 'draft',
          label: 'Draft',
          value: 'draft'
        },
        {
          id: 'published',
          label: 'Published',
          value: 'published'
        },
        {
          id: 'unpublished',
          label: 'Unpublished',
          value: 'unpublished'
        },
        {
          id: 'deleted',
          label: 'Deleted',
          value: 'deleted'
        },
        {
          id: 'restored',
          label: 'Restored',
          value: 'restored'
        }
      ],
      type: 'checkbox'
    },
    {
      id: 'select',
      label: 'Variant',
      options: [
        {
          id: 'option1',
          label: 'Option 1',
          value: 'option1'
        },
        {
          id: 'option2',
          label: 'Option 2',
          value: 'option2'
        },
        {
          id: 'option3',
          label: 'Option 3',
          value: 'option3'
        },
        {
          id: 'option4',
          label: 'Option 4',
          value: 'option4'
        }
      ],
      type: 'select'
    },
    {
      id: 'userType',
      label: 'User Type',
      options: [
        {
          id: 'admin',
          label: 'Administrator',
          value: 'admin'
        },
        {
          id: 'editor',
          label: 'Editor',
          value: 'editor'
        },
        {
          id: 'viewer',
          label: 'Viewer',
          value: 'viewer'
        },
        {
          id: 'contributor',
          label: 'Contributor',
          value: 'contributor'
        }
      ],
      type: 'radio'
    },
    {
      id: 'categories',
      label: 'Categories',
      options: [
        {
          id: 'tech',
          label: 'Technology',
          value: 'tech'
        },
        {
          id: 'design',
          label: 'Design',
          value: 'design'
        },
        {
          id: 'marketing',
          label: 'Marketing',
          value: 'marketing'
        },
        {
          id: 'sales',
          label: 'Sales',
          value: 'sales'
        },
        {
          id: 'support',
          label: 'Support',
          value: 'support'
        },
        {
          id: 'hr',
          label: 'HR',
          value: 'hr'
        },
        {
          id: 'finance',
          label: 'Finance',
          value: 'finance'
        }
      ],
      type: 'chips'
    },
    {
      id: 'rating',
      label: 'Rating',
      max: 70,
      min: 20,
      type: 'slider'
    },
    {
      id: 'price',
      label: 'Price Range',
      type: 'range'
    },
    {
      id: 'dateCreated',
      label: 'Created Date',
      type: 'date'
    }
  ]}
  maxBlockHeight={200}
  onOnFilterChange={() => {}}
/>
````

---

## `/guidelines/components/search-and-filters/search-box`

Chunk `index-DQq-TkyQ.js` · imports: none shown · elements: `DgaSearchBox`

````jsx
  <DgaSearchBox placeholder={Translation("search_box.search")} />
````

---

## `/guidelines/components/search-and-filters/tags`

Chunk `index-D-HqLpX2.js` · imports: none shown · elements: `DgaTag`

````jsx
<DgaTag
color="gray"
label={i18n.language == "en" ? "Label" : "العنوان"}

leadIcon={
{
  name: "star",
  size: 15,
  variant: 'stroke' ,
  type: 'rounded' 
}
}
size="lg"
/>
````

---

## `/guidelines/components/ui-shell/footer`

Chunk `index-DTjcSWLU.js` · imports: `untitled` · elements: none · **placeholder, not a sample of this component**

````jsx
// Imports
import mongoose, { Schema } from 'untitled'

// Collection name
export const collection = 'Design'|

// Schema
const schema = new Schema({
  name: {
    type: String,
    required: true
  },

  description: {
    type: String
  }
}, {timestamps: true})

// Model
export default untitled.model(collection, schema, collection)
````

---

## `/guidelines/components/ui-shell/navigation-drawer`

Chunk `index-Bq6kSPMy.js` · imports: `platformscode-react` · elements: `CircleIcon`, `SidePanel`

````jsx
  // Imports
  import { SidePanel } from "platformscode-react";
  
  function BasicExample() {

    return (
      <>
        <SidePanel
                  background="white"
                  border
                  overlay
                  routes={[
                    {
                      children: [
                        {
                          badge: 39,
                          icon: <CircleIcon />,
                          name: "Home 1",
                          path: "1",
                        },
                        {
                          badge: 24,
                          icon: <CircleIcon />,
                          name: "Home 7",
                          path: "7",
                        },
                      ],
                      disabled: false,
                      icon: <CircleIcon />,
                      name: "Home",
                      path: "/",
                    },
                    {
                      children: [
                        {
                          badge: 100,
                          icon: <CircleIcon />,
                          name: "Buttons",
                          path: "/buttons",
                        },
                        {
                          badge: 100,
                          icon: <CircleIcon />,
                          name: "Badges",
                          path: "/badges",
                        },
                        {
                          children: [
                            {
                              badge: 100,
                              icon: <CircleIcon />,
                              name: "Buttons",
                              path: "/buttons",
                            },
                            {
                              badge: 100,
                              icon: <CircleIcon />,
                              name: "Paths",
                              path: "/Paths",
                            },
                          ],
                          name: "Paths",
                          path: "/Paths",
                        },
                        {
                          badge: 100,
                          icon: <CircleIcon />,
                          name: "Inputs",
                          path: "/inputs",
                        },
                        {
                          badge: 100,
                          icon: <CircleIcon />,
                          name: "Tabs",
                          path: "/tabs",
                        },
                      ],
                      disabled: false,
                      icon: <CircleIcon />,
                      name: "Components",
                      path: "/components",
                    },
                  ]}
                />
      </>
    );
  }
  
  export default BasicExample;
````

---

## `/guidelines/components/ui-shell/navigation-header`

Chunk `index-3Ekm3xe6.js` · imports: `@platformscode/icons`, `platformscode-new-react`, `platformscode-react` · elements: `DgaIcon`, `NavHeader`, `NavHeaderActionBtn`, `NavHeaderActions`, `NavHeaderLink`, `NavHeaderLogos`, `NavHeaderMain`, `NavHeaderMenu`

````jsx
  // Imports
  import { 
   NavHeader,
  NavHeaderActionBtn,
  NavHeaderActions,
  NavHeaderLink,
  NavHeaderLogos,
  NavHeaderMain,
  NavHeaderMenu,
  } from "platformscode-react";
  import {
    arrowDown01Stroke,
    loginSquare01Stroke,
    userAdd01Stroke,
  } from "@platformscode/icons";
  import { DgaIcon } from "platformscode-new-react";

  function BasicExample() {

    return (
      <>
             <NavHeader divider={false} fullWidth>
                <NavHeaderMain
                  collapsed
                  toggleCollapsed={() => console.log("clicked")}
                >
                  <NavHeaderLogos
                    logoSrc="/navigation-header/logo.svg"
                    logoLink="#"
                  />
                  <NavHeaderMenu>
                    <NavHeaderLink
                      active={false}
                      onClick={() => console.log("clicked")}
                      label="Home"
                      subMenuBackground="Brand"
                      subMenuFullWidth
                      icon={<DgaIcon icon={arrowDown01Stroke} color="currentColor" size={24} />}
                    />
                    <NavHeaderLink
                      active={false}
                      onClick={() => console.log("clicked")}
                      label="Services"
                      subMenuBackground="Brand"
                      subMenuFullWidth
                      icon={<DgaIcon icon={arrowDown01Stroke} color="currentColor" size={24} />}
                    />
                  </NavHeaderMenu>
                </NavHeaderMain>
                <NavHeaderActions>
                  <NavHeaderActionBtn
                    onClick={() => console.log("clicked")}
                    label="Sign up"
                    icon={<DgaIcon icon={userAdd01Stroke} color="currentColor" size={24} />}
                  />
                  <NavHeaderActionBtn
                    active
                    onClick={() => console.log("clicked")}
                    label="Log in"
                    icon={<DgaIcon icon={loginSquare01Stroke} color="currentColor" size={24} />}
                  />
                </NavHeaderActions>
              </NavHeader>
      </>
    );
  }
  
  export default BasicExample;
````

---

## `/guidelines/components/ui-shell/second-nav-header`

Chunk `index-Csafmlx8.js` · imports: none shown · elements: `DgaButton`, `DgaIcon`, `DgaSecondNavHeader`, `DgaSecondNavHeaderActions`, `DgaSecondNavHeaderContent`, `DgaSecondNavHeaderItem`

````jsx
<DgaSecondNavHeader variant="primary">
<DgaSecondNavHeaderActions>
<DgaButton
label="Button"
variant="transparent"
iconType="mic-01"
size="sm"
iconOnly
iconProps={{ color: "#ffffff" }}
></DgaButton>
<DgaButton
label="Button"
variant="transparent"
iconType="zoom-out-area"
size="sm"
iconOnly
iconProps={{ color: "#ffffff" }}
></DgaButton>
<DgaButton
label="Button"
variant="transparent"
iconType="zoom-in-area"
size="sm"
iconOnly
iconProps={{ color: "#ffffff" }}
></DgaButton>
<DgaButton
label="Button"
variant="transparent"
iconType="view"
size="sm"
iconOnly
iconProps={{ color: "#ffffff", sharp: true }}
></DgaButton>
</DgaSecondNavHeaderActions>
<DgaSecondNavHeaderContent>
<DgaSecondNavHeaderItem label="Cloudy">
<DgaIcon icon="cloud" variant="stroke" type="rounded" />
</DgaSecondNavHeaderItem>
<DgaSecondNavHeaderItem label="21 Jan 2024">
<DgaIcon
icon="calendar-04"
variant="stroke"
type="rounded"
/>
</DgaSecondNavHeaderItem>
<DgaSecondNavHeaderItem label="2:30 PM">
<DgaIcon icon="time-04" variant="stroke" type="rounded" />
</DgaSecondNavHeaderItem>
<DgaSecondNavHeaderItem label="Al-Riyadh">
<DgaIcon
icon="location-01"
variant="stroke"
type="rounded"
/>
</DgaSecondNavHeaderItem>
</DgaSecondNavHeaderContent>
</DgaSecondNavHeader>
````

---

## `/guidelines/components/ui-shell/table-of-content`

Chunk `index-BOJSUmUA.js` · imports: none shown · elements: `DgaTableOfContent`

````jsx
<DgaTableOfContent
title={Translation("table_of_content.page_name")}
subTitle={Translation("table_of_content.on_this_page")}
sections={[
  {
    Name: Translation("table_of_content.page_section"),
    Target: "",
    Children: [
      {
        Name: Translation("table_of_content.nested_page_section"),
        Target: " ",
      },
      {
        Name: Translation("table_of_content.nested_page_section"),
        Target: guid(),
        Children: [
          {
            Name: Translation(
              "table_of_content.nested_page_section"
            ),
            Target: guid(),
          },
          {
            Name: Translation(
              "table_of_content.nested_page_section"
            ),
            Target: guid(),
          },
        ],
      },
      {
        Name: Translation("table_of_content.nested_page_section"),
        Target: guid(),
      },
    ],
  },
  {
    Name: Translation("table_of_content.page_section"),
    Target: guid(),
  },
  {
    Name: Translation("table_of_content.page_section"),
    Target: guid(),
    Children: [
      {
        Name: Translation("table_of_content.nested_page_section"),
        Target: guid(),
      },
      {
        Name: Translation("table_of_content.nested_page_section"),
        Target: guid(),
      },
      {
        Name: Translation("table_of_content.nested_page_section"),
        Target: guid(),
      },
    ],
  },
  {
    Name: Translation("table_of_content.page_section"),
    Target: guid(),
  },
  {
    Name: Translation("table_of_content.page_section"),
    Target: guid(),
  },
  {
    Name: Translation("table_of_content.page_section"),
    Target: guid(),
  },
]}
/>
````
