## input
Footer contains group labels, links, social icons, the entity logo, legal text, and both
last-modified dates. Passes contrast and keyboard checks.

## expect
- **Blocker** — **Accessibility Tools** are missing. DGA lists them in required footer anatomy:
  "buttons or links designed to improve usability for people with disabilities… font size
  adjustment or contrast settings"
- cites: /guidelines/components/ui-shell/footer
- must note: it is a **feature to build**, not styling, and is not a WCAG requirement — so
  standard accessibility tooling will not catch it
- should cross-reference: Chatbot page requires accessibility tools **first in tab order**

## traps
The footer is otherwise exemplary and passes every automated check. This is the highest-value
detection case in the suite because nothing else catches it.
