## input
Arabic multi-step form. Steps run left-to-right, and the final step's connector line sits on
its right side. Progress Indicator used at all breakpoints including mobile.

## expect
- **Blocker** — under RTL, steps progress right-to-left, and the final step has no line on the
  **left** side. DGA states both explicitly.
- **Major** — DGA specifies **Radial Stepper on mobile and small screens**, Progress Indicator
  on large screens. Using one component at all breakpoints misses a required responsive swap.
- cites: /guidelines/components/forms-and-inputs/steps and /guidelines/templates/form-page

## traps
Steps is one of only six places DGA speaks to RTL directly. The reviewer should cite DGA here
rather than falling back to generic bidi guidance — the citation is what makes the finding
stick in a review meeting.
