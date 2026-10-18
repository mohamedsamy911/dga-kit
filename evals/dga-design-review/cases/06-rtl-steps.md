## input
Arabic multi-step form. Steps run left-to-right, and the final step's connector line sits on
its right side. Progress Indicator used at all breakpoints including mobile.

## expect
- **Blocker** — under RTL, steps progress right-to-left, and the final step has no line on the
  **left** side. DGA states both explicitly.
- **Major** — DGA's form template uses the **Radial Stepper on mobile devices and small
  screens**. Using the full stepper at every breakpoint ignores that guidance.
- cites: /guidelines/components/forms-and-inputs/steps and /guidelines/templates/form-page

## traps
Steps is one of the few pages where DGA speaks to RTL directly (the total is unverified — never
cite a count). The reviewer should cite DGA here
rather than falling back to generic bidi guidance — the citation is what makes the finding
stick in a review meeting.
