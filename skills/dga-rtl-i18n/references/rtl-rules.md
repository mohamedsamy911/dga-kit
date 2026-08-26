# RTL rules

## Mirroring

### Always mirror
Anything whose meaning is "the direction the interface flows."

- Navigation arrows and chevrons — back, forward, next, previous, expand-into
- Breadcrumb separators
- Progress bars, steppers, timelines, slider fill direction
- Sliders and range inputs — the value increases toward the *start* edge
- Pagination controls
- Drawer / sidebar / off-canvas panel position
- Tree and nested-list indentation
- Table column order
- List bullets and numbers
- Speech-bubble tails
- Undo / redo — they are directional metaphors, and undo points toward the start
- Icons depicting aligned text lines

### Never mirror
Anything referring to a physical object or a fixed convention.

- Logos, brand marks, flags, wordmarks
- Checkmarks and cross marks
- Clockwise metaphors — refresh, rotate, timers. Clockwise stays clockwise.
- Physical objects: envelope, phone, camera, printer, pin, lock, calendar
- Musical notation
- Latin text rendered as an image

### Decide once, record the decision
Genuine industry disagreement. Pick one, write it in `dga-design-system/references/brand.md`,
and never revisit it per-screen.

- **Media playback controls** (play, fast-forward, rewind) — some systems mirror them to follow
  the timeline, others keep them fixed as a transport-control convention
- **Magnifying glass** — mirroring is purely cosmetic, but must be consistent across the product
- **Charts with a time axis** — mirroring matches reading direction; not mirroring matches
  conventional data-viz. Whichever you choose, the axis labels must agree with the bars.

If DGA states a rule for any of these, DGA wins — check `references/components.md` first.

## Bidirectional text

The bidi algorithm assigns direction to *neutral* characters — punctuation, brackets, spaces,
symbols — from whatever surrounds them. That is the entire source of "the bracket is on the
wrong side" bugs.

**Isolate embedded runs.** Any LTR content inside Arabic text, or vice versa:

```html
<p>رقم الطلب <bdi>REQ-2026-8841</bdi> قيد المراجعة</p>
```

`<bdi>` is the right tool. `dir="ltr"` alone is not enough — it sets direction but does not
isolate, so neighbouring punctuation still leaks. In CSS, the equivalent is
`unicode-bidi: isolate`.

**Applies to:** phone numbers, national IDs, order and reference numbers, URLs, email
addresses, file paths, code, version strings, English brand names, and user-generated content
of unknown direction.

**Never use `unicode-bidi: bidi-override`.** It forces visual order, breaks copy-paste, and
breaks screen readers. If you reach for it, the real problem is a missing isolate somewhere.

**Never concatenate translated fragments.** `t('sent') + ' ' + count + ' ' + t('messages')`
cannot produce correct Arabic. Use one message with placeholders, and let ICU handle the order.

## CSS that is not automatically logical

These do not respond to `dir` and need an explicit override:

```css
.card { box-shadow: 4px 0 12px rgba(0,0,0,.1); }
.card:dir(rtl) { box-shadow: -4px 0 12px rgba(0,0,0,.1); }
```

- `transform` — `translateX`, `skewX`, `rotate`, and any transform-based slide animation
- `box-shadow` / `text-shadow` offsets
- `background-position`
- Gradient directions (`to right`, angle values)
- `clip-path` and mask coordinates
- Absolute `left` / `right` in JS-computed styles

Prefer `:dir(rtl)` over `[dir="rtl"]` — it works through shadow DOM and doesn't depend on the
attribute being on an ancestor you control.

**Scrolling:** `element.scrollLeft` in RTL is inconsistent across browsers — it may be negative,
or measured from the right. Don't compute scroll positions by hand; use `scrollIntoView()` and
`scrollBy({ left: … })`, which respect direction.

## Arabic typography

- **More line-height.** Arabic ascenders and descenders are taller than Latin. A Latin scale's
  line-heights are usually too tight — expect to add roughly 0.15–0.25 to the ratio. Take the
  actual values from the DGA type scale, not from this note.
- **Slightly larger sizes.** At the same nominal size Arabic reads smaller than Latin. Check the
  DGA scale for whether it specifies different values per script.
- **No letter-spacing, ever.** It breaks the connected script.
- **`text-transform: uppercase` is a no-op on Arabic** but still fires on any embedded Latin,
  producing a mixed-case mess. Scope it.
- **No faux bold, no faux italic.** Arabic has no italic tradition and synthesised slant looks
  broken. Ship real weights; if a weight doesn't exist in the Arabic face, redesign the
  hierarchy rather than synthesising.
- **Cover both scripts in one stack.** If the Arabic face has no Latin glyphs, English words
  mid-sentence fall back to a system font and the line changes texture. Either pick a face that
  covers both, or pair deliberately with `unicode-range`.
- **Justification.** Arabic traditionally justifies by kashida (glyph elongation), which CSS
  can't do reliably. Use `text-align: start` and accept a ragged edge.

## Testing

- Set the browser to Arabic and walk the screen with the keyboard only — focus order is where
  RTL bugs hide after the visual ones are fixed.
- Test with a long Arabic string and a long English string in the same field. Arabic often runs
  longer than English; fixed-width containers designed against English clip.
- Render a screen with `dir="rtl"` but English content, and vice versa. It looks wrong on
  purpose, and it surfaces every hardcoded physical property in one pass.
