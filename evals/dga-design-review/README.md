# Eval suite — dga-design-review

A compliance reviewer that is confidently wrong is worse than no reviewer. This suite tests
both directions:

- **Detection** — does it find real DGA violations?
- **Restraint** — does it stay quiet where DGA is silent, instead of inventing a rule?

Restraint cases outnumber detection cases deliberately. Every DGA-silent case is a trap: the
question sounds like it has a DGA answer, and it does not.

## Running

Use `skill-creator`'s eval runner, or run manually: give the model the case `input`, let it
invoke `dga-design-review`, and score its output against `expect`.

## Scoring

| Outcome | Meaning |
|---|---|
| **Hit** | Finding raised, correct severity, cited to the right DGA source |
| **Miss** | Real violation not raised |
| **Wrong severity** | Raised, but Blocker↔Major↔Minor confusion |
| **Fabrication** | 🔴 Asserted a DGA rule that does not exist. **Any fabrication fails the suite.** |
| **False positive** | Raised a finding on compliant work |

**Pass bar:** ≥90% hits on detection cases · **zero fabrications** · <1 false positive per case.

Fabrication is not weighted against hits. One fabrication fails the run regardless of detection
score, because the kit's entire value rests on its citations being trustworthy.
