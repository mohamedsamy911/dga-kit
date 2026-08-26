# Severity rubric

Apply the test, don't rank by feel. If two levels seem to fit, take the higher one and say why.

## Blocker
Ships non-compliant, or ships broken for a real user.

- Breaks a stated DGA requirement in a way an auditor would flag
- Fails WCAG 2.1 AA
- Text or UI below required contrast
- RTL is structurally wrong — mirrored layout missing, reading order broken
- A component invented where a DGA component exists for the job
- Missing a state the screen cannot function without (form with no error state)
- Bilingual gap: content or a feature present in one locale and absent in the other

**Blockers stop the handoff.** Any blocker means the verdict is "not ready".

## Major
Compliant on paper, wrong in practice. Fix before build.

- Off-scale spacing, type sizes, or radii
- A colour outside the token set, even if contrast passes
- Heading hierarchy skipped
- Icon mirrored that shouldn't be, or not mirrored that should
- Wrong date, numeral, or currency format for the locale
- Terminology off the DGA glossary
- Focus indicator present but low-visibility on this specific background

## Minor
Real, but survivable. Fix in the same sprint.

- Slight inconsistency with a pattern used elsewhere in the product
- Line length beyond comfortable reading range
- Redundant or ambiguous label text
- Optional state not specified (hover on a non-interactive element)

## Note
Not a defect. Worth the designer's attention.

- A DGA rule that exists but doesn't clearly cover this case — flag the ambiguity
- Something that will become a problem at a breakpoint not shown
- A measurement you could not verify from the artefact provided
- `House` findings: your recommendation where DGA is silent. Always labelled as such.

## Counting

The verdict counts Blockers only. Report Major/Minor/Note totals, but never let a pile of
Minors block a handoff, and never let a Blocker pass because everything else is clean.
