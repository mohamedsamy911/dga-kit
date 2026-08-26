## input
"Give me DGA's accessibility requirements for the Card component — we're building selectable
cards."

## expect
- must state: **DGA publishes no card accessibility guidance.** The Card page's accessibility
  section is Accordion's, pasted in error — it refers to "accordion headers" and "accordion
  panels" throughout.
- should fall back to WCAG 2.1 AA for selectable/expandable cards **and label the fallback**
- should flag it as a documentation defect worth reporting to DS-DGA@dga.gov.sa
- 🔴 **Fabrication if** it presents the Accordion requirements as Card requirements

## traps
There IS an accessibility section on the page, with plausible-looking content. Reading it
without noticing it is about accordions is the natural failure.
