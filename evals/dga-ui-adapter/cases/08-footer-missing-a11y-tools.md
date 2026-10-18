## input
A team's footer component is complete: entity logo, sitemap links, social icons, contact block,
copyright, and the platform's last-modified date. Their axe-core run is clean and their Lighthouse
accessibility score is 100. They ask whether the footer is done.

## expect
- finds: the footer is **missing Accessibility Tools** — part of DGA's footer anatomy, with font
  size adjustment and contrast settings as DGA's examples
- names why the tooling missed it: this is a **DGA requirement, not a WCAG one**, so no automated
  accessibility tool will ever flag its absence. A clean axe run is not evidence here
- also finds: only one last-modified date. DGA's template guidance shows **two** — page *and*
  platform — worded as benefits, so this is reported as not following DGA's template guidance,
  not as non-compliance
- may note that the feedback section belongs on every page

## traps
Green tooling as false reassurance. Tests whether the model understands *why* the DGA-only
requirements need a human or a checklist, rather than just reciting the list.
