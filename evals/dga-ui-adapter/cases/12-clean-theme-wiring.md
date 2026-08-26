## input

A Chakra v3 theme for a `.gov.sa` platform, submitted for review.

**Colour roles.** Semantic roles from `tokens.json` under `semanticTokens.colors`. `text.secondary`
is **kept as a defined role but repointed** from DGA's gold `#dba102` (2.30:1, unusable) to
`secondary-gold.800` `#945c01` — 5.54:1 on white, 5.30:1 on body. The three `-light` roles are
**kept as published** and documented as dark-surface only: on `background.black` they measure
10.75:1, 14.79:1 and 9.09:1. Nothing is deleted from the theme, so no token can resolve to a raw
string.

**Brand palette.** Chakra's seven `colorPalette` slots are filled and every composed pairing was
measured: `subtle` brand.50, `muted` brand.100, `emphasized` brand.200, `solid` brand.600 with
`contrast` white at **4.75:1**, `focusRing` brand.600, and **`fg` brand.700 `#166a45`** — 6.31:1 on subtle,
5.81:1 on muted, 4.92:1 on emphasized, 6.60:1 on white. Solid-button hover and pressed resolve to
brand.700 and brand.800 (6.60:1 and 8.56:1 against white); brand.500 is explicitly excluded as a
fill because white on it is 3.88:1.

**Dark mode.** No `_dark` slot is emitted and no colour-mode toggle is exposed. DGA publishes dark
values only in the PC 1.0 Figma collections, so there is nothing legitimate to put in a slot; an
empty-but-present slot filled with the light value would ship a light theme labelled dark. The
gap is recorded in `dga-brand-overlay`.

**Type.** `heading` and `body` are `"IBM Plex Sans", "IBM Plex Sans Arabic", system-ui,
sans-serif` — **Latin first**, so Latin renders in the face DGA actually names and Arabic
falls through per character to the Arabic face. The Arabic face is recorded in
`dga-brand-overlay` as the project's decision pending DS-DGA@dga.gov.sa — not cited as a DGA
rule. Saudi Font is exposed only as `fonts.occasion`.
Display tracking is emitted as `-0.02em` (never `-2%`, which is invalid CSS) and scoped
`:lang(en)`, so an unlabelled document gets **no** tracking rather than tracking on Arabic.

**Breakpoints.** `sm: 600px, md: 960px, lg: 1280px`, with Chakra's inherited `xl`/`2xl` deleted so
an unknown key cannot silently no-op. Documented as **DGA's four bands under three Chakra names** —
mobile 0–599, tablet 600–959, desktop 960–1279, xl 1280+ — with a comment noting that DGA
"desktop" is Chakra `md`.

**Spacing.** Wired in rem rather than DGA's published px, recorded as a deliberate decision: DGA
mandates a footer font-size control, and px spacing would scale the text without scaling the boxes
around it. Computed values match DGA's scale at the default root size.

**Controls.** 44px minimum applied per element type, not blanket: directly on `IconButton`,
`CloseButton`, `Menu.Item` and `Tabs.Trigger`; and on `Checkbox.Root`, `RadioGroup.Item`,
`Switch.Root` and `Tag.Root` via padding and an inset `::before` hit area — so the *target* is
44px without the painted control box, switch track or close glyph being resized. `Link` sets
`textDecoration: 'underline'` in its base.

**CI.** `check-contrast.mjs --json` runs as a committed artefact documenting which upstream DGA
tokens are unusable. The **blocking** checks are separate and run over the project's own source: a
grep for hex literals outside the theme layer, a grep for `#dba102` / `background.secondary` /
`colorPalette="secondary"` (the aliases a developer would actually reach for), and a contrast
assertion over the composed brand pairings listed above.

## expect

This case tests **calibration**, not silence. A reviewer that finds nothing in a real theme is
as broken as one that finds ten things — the question is whether what it raises is true, and
graded honestly.

- **Zero Blockers.** Nothing here is mandated-and-absent.
- **Leads with the verdict and with what is correct**, before any findings.
- **Every finding must be verifiable** — a contrast ratio that reproduces against `tokens.json`,
  a documented Chakra or DGA behaviour, or a named omission in the submission itself. A finding
  that rests on a DGA rule which does not exist is a fabrication and fails the run outright.
- **Severity calibrated.** Nothing mandated-and-absent graded below High; nothing stylistic
  graded above Low. A response that is uniformly severe fails.
- **Notes, not findings**, on limits documented as unavailable upstream: responsive radius and
  spacing being Figma-only; DGA's non-monotonic radius scale.
- The **build list** — Digital Stamp, footer Accessibility Tools, feedback section, skip link,
  table of contents, two last-modified dates, Hijri wrapper — is **scope, not a finding**.

**FAIL if:** a Blocker is raised · any finding cites a DGA rule that does not exist · the
response is uniformly severe · it does not say what the submission got right.

## traps

**Read this before revising the input again.** Three earlier versions of this case were written
as "a perfect theme, expect zero findings." All three failed, and in all three the fixture was
wrong and the reviewer was right — it caught, with exact arithmetic, that only one text role
fails AA rather than four; that deleting a Chakra token makes it fail *silently* rather than
loudly; that `check-contrast.mjs --ci` can never go green; that DGA does define an `xl` band;
that a `fg` of brand.600 fails on `muted`; that `createSystem` deep-merges so "deleted" keys
survive; and that a 44px list omitting `Button` and every text input is not "every interactive
element."

The conclusion is not that the input needs a fourth revision. It is that **a DGA-compliant theme
has too much interacting surface to be specified correctly in prose** — which is the strongest
single argument for this kit existing. Every attempt to describe a flawless one produced a new
real defect.

So the rubric now tests what restraint actually means for a reviewer: no invented rules, no
inflated severity, no Blockers where none exist, and credit where the submission is right.

Two things a padding reviewer will do here and a calibrated one will not: grade the documented
Figma-only gaps as findings rather than Notes, and treat the build list as defects in a theme
that structurally cannot contain them.

**A fourth defect was found after that rewrite, and it is the sharpest.** The input declared an
**Arabic-first** font stack, which *looks* like the Arabic-first principle applied to
typography. It is not. Font fallback resolves **per character**, so an Arabic-first stack
renders **Latin** out of IBM Plex Sans Arabic's Latin glyphs and the face DGA actually names
never renders anything. A reviewer flagging that order is **correct** — and this case would
have scored them as a false positive. Corrected, and `evals/validate-fixtures.py` now asserts
the stack matches `token-wiring.md` rather than trusting prose on both sides.

That is four rounds in which the fixture, not the skill, was wrong.
