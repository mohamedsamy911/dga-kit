# Verification record

Verified locally on 2026-08-31, Windows, Node.js 22.17.1 and Playwright Chromium. This is an engineering check of a fictional showcase, not DGA certification or a full WCAG conformance claim.

## Build and theme

- Clean dependency install and production TypeScript/Vite build completed in the delivered project.
- The theme guard checks 12 source files and 78 CSS references. Its deliberately broken examples are detected.
- The vendored DGA token stylesheet is unchanged. Semantic aliases, including the footer color fix, live in the project theme.
- Codex reports dga-kit 0.7.2 installed and enabled; the bundled plugin validator passed. The actual `dga-frontend-dev` agent authored the UI and the footer state fix.

## Browser checks

All **21 Playwright tests passed** against the production build served under `/dga-kit/`
(1.2 minutes on the integration run). They cover:

- Six main routes in Arabic and English at 390px and 1440px, with axe WCAG 2 A/AA and 2.1 A/AA checks and no horizontal overflow.
- Search/filter/reset, invalid fields and linked error summaries, correction, review/edit/confirmation, and session-local request tracking in both languages.
- Empty, unknown-reference, simulated connection-error, and retry tracking states.
- Language switching without losing unfinished input, first-Tab skip navigation, mobile menu, 44px control targets, footer control ordering, and feedback submission.
- High contrast and text resizing; English reflow at 320/600/960/1280px with the app's 120% text setting.
- Real resolved button colors in both languages and contrast modes: resting, hover, pressed, selected, focus-visible, and disabled text-size limits. Disabled primary feedback buttons stay unchanged on hover. JSON measurements are attached to these test results.
- No duplicate header/footer after navigation; no runtime errors in the tested paths; no external requests during the application journey.
- JavaScript, CSS, favicon, and font requests stay under the GitHub Pages project path and
  resolve without HTTP errors; Arabic and English service deep links survive reloads.

Run `npm run build` then `npm run test:e2e` from `showcase/`. The HTML report is generated in `playwright-report/`. Font checks wait for the local fonts to load. The 120% app setting does not replace separate testing at 200% browser zoom.

The new deployment guard was break-tested with a deliberate `vite build --base /`. Its
asset-path test executed and failed because the app could not load under the project prefix.
After restoring the configured build, all three deployment tests passed. Source configuration
and the original standalone project were not modified by the break test.

## Production accessibility tools

From `showcase/`, run `npm run preview`, then `npm run audit` in another terminal. For a custom
port, pass the full project URL, e.g. `node scripts/audit.mjs http://127.0.0.1:4174/dga-kit/`.
Machine-readable evidence is in `docs/audits/`.

- Lighthouse accessibility: **100/100** on Arabic and English home pages.
- pa11y: **0 actionable errors** on Arabic and English home and application pages.
- pa11y HTML_CodeSniffer also reports 29 home-page and 15 application-page hash-route links per locale as missing anchors. These are reviewed SPA route links, not in-page anchors. The script preserves every raw finding and classifies only a finite list of known routes. Unknown routes and missing actual in-page anchors remain failures. Playwright separately follows all unique home-page routes and exercises the application journey.

## Manual evidence and limits

Desktop/mobile Arabic and English layouts were visually inspected during implementation. Keyboard focus, validation transitions, and navigation were exercised. Automated color checks additionally protect the faint disabled button reported by the user.

Not completed: Arabic screen-reader pronunciation and full assistive-technology review, Safari/Firefox, real mobile devices, OS forced-colors, 200% browser zoom, or an independent DGA design/launch audit. Pa11y and Lighthouse do not cover every route/state. Real identity, registration, legal policies, and government integrations are outside this demo's scope. There is no production backend. Public hosting is a static demonstration only; see [publishing and live verification](PUBLISHING.md).
