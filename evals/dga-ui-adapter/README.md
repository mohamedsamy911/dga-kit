# Eval suite — dga-ui-adapter

The adapter skill's whole job is to be right about DGA on a library DGA never anticipated. That
gives it two ways to fail, and this suite tests both:

- **Detection** — does it catch a DGA violation expressed in *this* library's idiom?
- **Restraint** — does it stay silent where DGA is silent, instead of inventing a rule to sound
  authoritative?

Restraint cases are deliberately heavy. Every one of them sounds like it has a DGA answer and
does not — and the temptation to fill the gap is stronger here than in the design-review suite,
because the question arrives in a code context where an answer feels obligatory.

There is a third failure mode unique to this skill: **library confusion** — giving MUI advice for
a Chakra codebase, or naming a component the library does not have. Cases 03 and 08 test it.

## Running

Give the model the case `input`, let it invoke `dga-ui-adapter`, and score its output against
`expect`.

## Scoring

| Outcome | Meaning |
|---|---|
| **Hit** | Correct finding, correct rule, cited to the right source |
| **Miss** | Real violation not raised |
| **Fabrication** | 🔴 Asserted a DGA rule that does not exist. **Any fabrication fails the suite.** |
| **Library confusion** | 🔴 Advice for the wrong library, or a component that library does not have |
| **False positive** | Raised a finding on compliant work |

**Pass bar:** ≥90% hits on detection cases · **zero fabrications** · **zero library confusion** ·
<1 false positive per case.

Fabrication is not traded off against detection. One fabrication fails the run regardless of
score, because the kit's entire value rests on its citations being trustworthy — and a fabricated
rule in a code skill gets committed, not just discussed.
