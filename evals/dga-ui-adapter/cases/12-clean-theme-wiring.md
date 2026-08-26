## input
A Chakra v3 theme for a `.gov.sa` platform: primitives from `tokens.json` under `tokens.colors`,
roles under `semanticTokens.colors`, breakpoints 600/960/1280, IBM Plex Sans on heading and body
with Saudi Font exposed only as `fonts.occasion`, display letter-spacing scoped to Latin, controls
floored at 44px, `$`-prefixed annotation keys stripped before wrapping. Components reference
semantic roles only; `check-contrast.mjs` passes in CI.

## expect
- verdict: **compliant wiring**
- 0 findings against the theme itself
- may raise Notes only: the empty dark slot is expected and correct given DGA's Figma-only dark
  values; responsive radius and spacing remain unresolved for the same reason
- may remind that theme wiring is step 1 of 4 — the **build list** (Digital Stamp, footer with
  Accessibility Tools, feedback section, nav header, ToC, skip link) is still outstanding, since
  no theme can satisfy those
- FALSE POSITIVE if any finding is raised against the theme

## traps
A model that always finds something. Everything checkable here is correct, and the honest answer
is that the remaining work is components, not tokens.
