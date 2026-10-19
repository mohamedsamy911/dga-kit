# Raw capture — what DGA's live component demos render, 2026-10-19

Method: each component page's Live Demo (Visual tab, English) on design.dga.gov.sa, inspected in a
browser. The demo is DGA's own `dga-*` web component (`@platformscode/core`; the served version
was not recorded). Inside each host element, light DOM and every shadow root were walked, and every
`role`, `aria-*` attribute, native semantic tag and `tabindex`/`rel`/`target` was listed. **Static**:
before interaction, except the scripted events noted at the end. This records what the demo
rendered; it is not a full accessibility test.

```text

chip [dga-chip, 1] R: | A: | T: | M:tabindex=0
dropdown [dga-dropdown, 1] R:img | A: | T:button,svg,ul,li | M:
accordion [dga-accordion, 3] R:img | A: | T:a,svg | M:
card [dga-card, 1] R:img,button | A:aria-label=Action | T:svg,button | M:tabindex=0
carousel [dga-carousel, 1] R:img | A: | T:a,svg | M:
code-snippet [dga-codesnippet, 1] R:button,img | A:aria-haspopup=true,aria-expanded,aria-label=Button,aria-label=Button with icon,aria-hidden=true,aria-label=Show More | T:ul,li,a,button,svg | M:
digital-stamp [dga-digital-signature, 1] R:img | A: | T:svg,a | M:
divider [dga-divider, 1] R: | A: | T: | M:
list [dga-list-v2, 3] R:img | A: | T:ol,li,ul | M:
quote [dga-quote, 1] R: | A: | T: | M:
avatar [dga-avatar, 1] R: | A: | T:img | M:
charts [dga-chart, 3] R: | A: | T:svg | M:rel=1,rel=2,rel=3,rel=4,rel=0
content-switcher [dga-content-switcher, 1] R: | A: | T:button | M:
metric [dga-metric, 1] R:img,button | A:aria-label=Button with icon,aria-hidden=true,aria-label=View Report | T:svg,button | M:
structured-list [dga-structured-list, 1] R: | A: | T:table,th | M:
table [dga-data-table, 1] R:img | A: | T:table,th,label,input[checkbox],svg,button,td | M:tabindex=0
modal [dga-modal, 1] R:img,button | A:aria-label=Button with icon,aria-hidden=true | T:dialog,svg,button | M:
notification [dga-notification-toast, 1] R:img | A: | T:svg,button | M:
rating [dga-rating, 1] R: | A: | T:label,svg,input[radio] | M:
tooltip [dga-tooltip, 1] R: | A: | T: | M:
checkbox [dga-checkbox, 1] R:img | A: | T:label,input[checkbox],svg | M:tabindex=0
datepicker [dga-datepicker, 1] R:button,img | A:aria-label=Button with icon,aria-hidden=true | T:button,svg | M:
file-uploader [dga-file-upload, 1] R:img,button | A:aria-hidden=true,aria-label=Browse Files | T:input[file],label,svg,button | M:
input [dga-text-input, 1] R: | A: | T:input[text] | M:
number-input [dga-number-input, 1] R:img | A: | T:label,button,svg,input[number] | M:
radio [dga-radio-button, 1] R: | A: | T:label,input[radio] | M:tabindex=0
slider [dga-slider, 1] R:img | A: | T:input[range],svg | M:
steps [dga-progress-indicator, 1] R: | A: | T: | M:
switch [dga-switch, 1] R: | A: | T:label,input[checkbox] | M:
textarea [dga-textarea, 1] R: | A: | T:textarea | M:
loading [dga-loading, 1] R: | A: | T: | M:
progress-bar [dga-linear-progress-bar, 1] R:img | A: | T:svg | M:
radial-stepper [dga-radial-stepper, 1] R: | A:aria-size | T:svg | M:
skeleton [dga-line-skeleton, 5] R: | A: | T: | M:
breadcrumbs [dga-breadcrumbs, 1] R:img | A:aria-label=breadcrumb,aria-disabled,aria-current=page | T:nav,ul,li,a,svg | M:
menu [dga-menu-list, 1] R:img | A: | T:ul,li,label,input[checkbox] | M:tabindex=0
pagination [dga-pagination, 1] R:img | A: | T:ul,li,button,svg | M:
slide-out [dga-slideout-menu, 1] R:img,button | A:aria-label=Button with icon,aria-hidden=true,aria-label=action | T:svg,button,ul,li | M:tabindex=0
tabs [dga-tabs, 1] R:img | A: | T:ul,li,a,svg | M:
filtration [dga-filteration, 1] R:button,img | A:aria-label=Filter,aria-hidden=true | T:button,svg | M:
search-box [dga-search-box, 1] R:img | A: | T:svg,input[text],button | M:
tags [dga-tag, 1] R:img | A: | T:svg | M:
second-nav-header [dga-second-nav-header, 1] R:img,button | A:aria-label=a secondary navigation navbar,aria-label=Button,aria-hidden=true | T:svg,button | M:
table-of-content [dga-table-of-content, 1] R: | A: | T:ul,li,a | M:

Not scanned with a host (demo is not a single dga-* element): buttons, floating button, link,
footer, navigation header; navigation drawer has no inline demo. Link demo (whole demo area): the
new-tab anchor renders target="_blank" rel="noopener noreferrer".

After a scripted interaction (synthetic mouseenter/mouseover/focus on the tooltip; click on the
dropdown button; click on the accordion header): tooltip roles [] aria [] and 0 [role=tooltip] in the
document; dropdown roles [img] aria []; accordion roles [img] aria []. Synthetic events may not
reproduce a real user's interaction.
```
