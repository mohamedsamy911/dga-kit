## input
A designer submits a services landing page. Section subheadings use `--text-secondary`
(#dba102) at 18px on `--background-white`. Everything else is on-token.

## expect
- severity: **Blocker**
- finds: #dba102 on #ffffff measures **2.30:1**, below DGA's 4.5:1 for text under 24px —
  and below even the 3:1 large-text threshold, so no size makes it compliant
- cites: /guidelines/foundations/color-system, and CONTRAST-AUDIT.md
- fix names: `secondary-gold-800` (#945c01) at 5.54:1 as the first compliant step
- must NOT: treat "it's an official DGA token" as making it acceptable

## traps
The token is genuinely DGA's and is *named* `text-secondary`. A weak reviewer defers to the
token set. The correct behaviour is to flag DGA's own token as unusable here.
