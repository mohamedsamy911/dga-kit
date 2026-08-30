# Eval suite — dga-design-review

A compliance reviewer that is confidently wrong is worse than no reviewer. This suite tests
both directions:

- **Detection** — does it find real DGA violations?
- **Restraint** — does it stay quiet where DGA is silent, instead of inventing a rule?

Restraint cases outnumber detection cases deliberately. Every DGA-silent case is a trap: the
question sounds like it has a DGA answer, and it does not.

## Running

```bash
claude plugin eval --skill dga-design-review
```

The cases here are the source; `skills/dga-design-review/evals/evals.json` is generated from them and is
what the runner reads. **Never edit the JSON** — add or change a case in `cases/`, then:

```bash
python3 evals/build-evals-json.py
```

CI runs `--check` and fails if the two have diverged, so a case added in markdown and not
regenerated is caught rather than silently never run.

Each case maps across as: `## input` → the prompt (prefixed with the skill invocation),
`## expect` bullets → `expectations`, and `## grader` (falling back to `## traps`) →
`expected_output`, because on these cases the trap *is* the expected behaviour — a grader that
never sees it scores a confident fabrication as a pass. Every case also carries the kit's own
bar as a final expectation: **a rule attributed to DGA that DGA does not publish fails the case**,
whatever else the answer gets right.

To run one by hand instead: give the model the case `input`, let it invoke `dga-design-review`, and score
against `expect`.

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
