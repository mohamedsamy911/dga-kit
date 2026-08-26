# Cross-reference — an independent second extraction

> ## This one is evidence, not a candidate list
>
> Unlike `UNOFFICIAL-CROSSREF.md` (a derivative npm library), this is an **independent
> extraction of the same official source** by a different person using a different method on a
> different date. Where the two agree, that is real corroboration. Where they disagree, **one of
> us is wrong** and the value needs a re-read before either is trusted.
>
> Still not a source of truth. Nothing here is copied into `tokens.json` without a re-harvest.

**Source:** `Sara-Saraireh/dga-platforms-code-claude-skill` — MIT, a single Claude Code skill for
DGA Platforms Code alignment. Token file `claude/skills/dga-platforms-code/tokens/colors-v1.0.json`,
which states it was read from `/guidelines/foundations/color-system` on **2026-06-21**.

**This kit:** live DOM extraction of CSS custom properties from the same page, **2026-08-26**.

Compared on 2026-08-26.

## Where the two agree — 48 of 51 steps

| Palette | Steps compared | Differences |
|---|---|---|
| Primary / SA green (`brand`) | 12 | **0** |
| `error` | 12 | **0** |
| `warning` | 12 | **0** |
| `success` | 12 | **0** |
| Gold, Lavender | all shared steps | **0** |

Two people, two methods, two months apart, character-identical on every one of those. That is
the strongest evidence either repository has that its numbers are right, and it is worth more
than either repo's own internal consistency.

## Where they disagree — three values

### 1 · `info.50` — almost certainly DGA fixed a typo between the two reads

| | Value |
|---|---|
| Their read, 2026-06-21 | `#ECFDF3` — **green**, character-identical to `success.50` |
| Our read, 2026-08-26 | `#eff8ff` — blue, consistent with the rest of the `info` ramp |

They flagged this themselves as a suspected source typo and told readers to verify before
relying on it. Our later read shows a plausible blue. **Most likely DGA corrected the page
between June and August.**

If that is what happened, it is the clearest possible argument for `dga-tokens-sync`: the source
is edited in place, without a changelog entry, and a value harvested once silently goes stale.
It also means their `VERIFY` note is now resolved — worth telling them.

### 2 · `neutral.500` / their `gray.500`

| | Value | on white |
|---|---|---|
| Ours | `#6c727e` | 4.83:1 |
| Theirs | `#6c737f` | 4.78:1 |

One unit apart in two channels. **`TODO(verify)`.**

Weak evidence for ours: the value appears twice in our extraction, as the `neutral.500`
primitive *and* as the `text.secondary-paragraph` role, from two separate CSS custom properties
that agree. Reading a rendered page cannot cross-check itself that way. Not proof — a systematic
extraction error would produce exactly the same agreement.

**Impact if we are wrong: none material.** Both values clear WCAG AA on white and on
`background.body`, so `text.secondary-paragraph` remains the correct AA-safe replacement for the
gold `text.secondary`. The recommendation does not move; only the fourth significant figure does.

### 3 · `neutral.950` / their `gray.950`

Ours `#0c111b`, theirs `#0d121c`. Same one-unit pattern, same `TODO(verify)`. No contrast
consequence — nothing in DGA pairs text against it.

## Where their read fills a gap in ours

Two "quirks" this kit documented as *missing steps* turn out to be **labelling** on DGA's page,
and their extraction caught the labels where our CSS-variable read could not:

| Value | We had it as | They have it as | What it means |
|---|---|---|---|
| `#dba102` | `role.text.secondary` only; noted "gold has no 600 step" | `gold.primary_600`, page-labelled **"Primary 600"** | The dangerous 2.30:1 gold *is* the gold palette's Primary 600. That explains why it reads as a headline colour and why designers reach for it. |
| `#80519f` | `role.text.tertiary` only; noted "lavender has no 500" | `lavender.primary_500`, page-labelled **"Primary 500"** | Same pattern. |

This strengthens the contrast finding rather than weakening it: the token is not an obscure
mislabelled role, it is the **primary step of a brand palette**, designated for text, at 2.30:1.

## Actions

- [ ] Next harvest: settle `neutral.500` and `neutral.950` by re-reading the CSS variables
- [ ] Next harvest: confirm `info.50` is now blue, and if so tell them their `VERIFY` note is resolved
- [ ] Record `gold 600` and `lavender 500` as **page-labelled palette steps**, not just semantic roles
- [ ] Credit this repository in `README.md`

## Worth borrowing from how they did it

Better practice than ours, independent of scope:

1. **Provenance stamped on every token file**, with the read date in the file itself. Ours puts
   `$meta` on `tokens.json` alone.
2. **Version in the filename** (`colors-v1.0.json`). A DGA version bump becomes a new file rather
   than a mutation of an existing one, so the old values stay readable.
3. **`VERIFY:` notes inside the data**, not only in prose. A suspected source defect travels with
   the value that has it. This is how they caught `info.50`, and it worked.
