# Unofficial cross-reference — `dga-ui-react` v1.11.3

> ## ⛔ NOT A SOURCE OF TRUTH
>
> This is a **community** npm package (MIT, published by an individual, not by DGA) that
> describes itself as "based on the DGA design system". Nothing in this file may be copied
> into `skills/dga-design-system/` or `tokens.json`. It exists for exactly two purposes:
> a scope cross-check for the harvest, and a list of candidate values to *verify* against
> design.dga.gov.sa.
>
> Every value below is **unverified**. Retrieved from npm 2026-08-26.

Package: `dga-ui-react@1.11.3` · MIT · demo at `dgaui.vercel.app` · repo URL in the manifest
returns 404.

---

## What it's actually made of

Read critically, this library is **Untitled UI with a green and gold swapped in**, not a
faithful DGA implementation. The evidence:

- The `error`, `warning`, `success`, `info` and `neutral` scales are verbatim Untitled UI
  values (`#F04438`, `#F79009`, `#17B26A`, `#2E90FA`, `#101828` shadows).
- The type scale — 72/60/48/36/30/24 then 20/18/16/14/12 with matching line-heights — is
  the Untitled UI scale unchanged.
- `fontFamily: "IBM Plex Sans"`, with **no Arabic face at all**.
- `direction: "ltr"` as the default, with RTL offered as an opt-in override.

The last two are the tell. A faithful implementation of an Arabic-first government design
system does not default to LTR and ship without an Arabic typeface. **Treat only the primary
and secondary ramps as plausibly DGA-derived.** Everything else is a generic base.

## Candidate values to verify

Only these two are worth taking to the harvest as hypotheses.

**Primary (green)** — `main #1B8354` · `500 #25935F` · `700 #166A45` · `light #54C08A`
**Secondary (gold)** — `main #DBA102` · `500 #F5BD02` · `800 #945C01` · `light #F7D54D`

### Contrast, measured

| Candidate | on `#FFFFFF` | on `#161616` | Verdict |
|---|---|---|---|
| `#1B8354` primary.main | 4.75 | 3.81 | AA normal text on white |
| `#166A45` primary.700 | 6.60 | 2.74 | AA on white; fails on dark |
| `#25935F` primary.500 | 3.88 | 4.67 | Large text only on white |
| `#54C08A` primary.light | 2.26 | 8.00 | **Never for text on white** |
| `#DBA102` secondary.main | 2.30 | 7.85 | **Never for text on white** |
| `#F5BD02` secondary.500 | 1.73 | 10.48 | **Never for text on white** |
| `#945C01` secondary.800 | 5.54 | 3.27 | AA on white — the usable gold for text |

**The trap:** if DGA's real gold is anywhere near `#DBA102`, gold text or gold icons on a white
background fail AA outright. Expect this to be a recurring **Blocker** in design review, and
confirm during the harvest which gold step DGA designates for text.

## Component inventory — 62 components

The most reusable thing here. Use it to sanity-check the harvest: if DGA's component list is
far shorter than this, this library invented components; if it's longer, the capture missed pages.

Accordion · Autocomplete · Avatar · Breadcrumb · Button · Card · Carousel · Checkbox · Chip ·
CircularProgressBar · CodeSnippet · ContentSwitcher · DatePicker · Divider · DropZone · Dropdown ·
DropdownItem · FileCard · FileUpload · FloatingButton · Grid · HeaderMenuItem · InlineAlert · Link ·
List · Loading · Menu · MenuItem · MenuItemGroup · Modal · NavigationDrawerItem · NormalSlider ·
Notification · NumberInput · Pagination · ProgressBar · ProgressIndicator · Quote · RadialStepper ·
Radio · RadioGroup · RangeSlider · Rating · SearchBox · SecondNavHeader · Skeleton (+Circle/Line/
Rectangle/Square) · SlideoutMenu · StatusTag · Switch · Tab · TabList · Table · Tag · TagInput ·
TextInput · Textarea · ThemeProvider · Tooltip

Note what's **missing** for a government service: no Footer, no SkipLink, no Header/masthead, no
Hijri date support in `DatePicker` (it wraps `react-multi-date-picker`). Those gaps are the ones
`dga-react` will have to fill regardless of which base we start from.

## Other scale values seen

Radii `0 / 2 / 4 / 8 / 16 / 24 / 9999px` · breakpoints `sm 375 / md 768 / lg 1280` ·
seven shadow steps. All unverified, and all consistent with a generic base rather than a
DGA-specific one.

## Recommendation

Do **not** adopt this as the foundation for `dga-react`. It would import a generic design
system wearing DGA colours, and every wrong value would then be very hard to find. It is useful
as a scope cross-check and as a list of two colour ramps to confirm. Revisit only if the
harvest shows the values genuinely match.
