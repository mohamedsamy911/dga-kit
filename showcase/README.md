# وصل · Wasl

An Arabic-first React showcase built with **dga-kit 0.7.2** and its **dga-frontend-dev** agent. A fictional digital-services portal that demonstrates the kit through usable screens, not a static component gallery.

**This is an unofficial demo. It is not affiliated with, endorsed by, or certified by the Saudi Digital Government Authority. It is not a government service or evidence of compliance.** All services, fees, processing times, and requests are fictional. Do not enter real personal information.

## Run locally

[Live Arabic demo](https://mohamedsamy911.github.io/dga-kit/) ·
[English demo](https://mohamedsamy911.github.io/dga-kit/?lang=en) ·
[Publishing guide](docs/PUBLISHING.md)

Requires Node.js 22.13+ (tested with 22.17.1).

```sh
cd showcase
npm ci
npm run dev
```

Run these commands from the repository root. Open [the local demo](http://127.0.0.1:5173/dga-kit/). Arabic is the default; the language control switches the whole experience to English.

For an English entry link, use [the English local demo](http://127.0.0.1:5173/dga-kit/?lang=en).

```sh
npm run build
npm run preview
```

Open [the production preview](http://127.0.0.1:4173/dga-kit/). The output is `showcase/dist/` relative to the repository root. Hash routes support static hosting without rewrite rules. No backend, API keys, account, or environment variables are required. Fonts are self-hosted by the build. The app has separate dependencies; installing the plugin does not install or build this demo.

## Demo walkthrough

1. Search and filter the service catalog. Try a query with no matches, then reset it.
2. Open a service and read its requirements, steps, and fictional service information.
3. Start a demo request. Submit empty fields to see linked validation errors, then use fictional details to continue through review and confirmation.
4. Track the demo reference **WASL-2026-1042**, or the reference generated during this session. Try an unknown reference as well.
5. Switch Arabic/English, resize to a phone, navigate using Tab, and activate the skip link.
6. Use the footer's text-size, dark-mode, and high-contrast controls and try page feedback.
7. Open **About the kit** to see which skills inform the experience and where the kit's coverage stops.

Requests and feedback exist only in memory and disappear on refresh. Nothing is sent to a government agency or external service. No analytics or tracking SDK is included.

## What the plugin contributes

| Skill | Concrete use |
| --- | --- |
| `dga-design-system` | Harvested token file, foundation and component reference |
| `dga-ui-adapter` | Native React components, semantic theme ownership, footer tools, feedback and dates |
| `dga-rtl-i18n` | Arabic-first layout, logical CSS, language switching, bidi isolation |
| `dga-a11y` | Keyboard and automated accessibility verification |

The actual `dga-frontend-dev` agent implemented the app. React with native HTML/CSS was chosen deliberately; `dga-react` is for DGA's own `platformscode-new-react` package and is **not** the right skill merely because an app uses React.

See [design decisions and evidence](docs/DESIGN-DECISIONS.md), [verification](docs/VERIFICATION.md), and [the included kit license](docs/dga-kit-LICENSE).

## Install the plugin in Codex

```sh
codex plugin marketplace add mohamedsamy911/dga-kit
codex plugin add dga-kit@dga-kit
```

This installs **11 skills**, not the repository's six agent definitions. On the development machine, the Codex session already exposed `dga-frontend-dev`, and that agent was used for this build. Do not claim that installing the plugin alone registers the agents. See the kit's [installation notes](https://github.com/mohamedsamy911/dga-kit/blob/master/INSTALL.md) for its separate native-agent installer and the runtime discovery check. Newly installed skills become available in a subsequent Codex turn; reopen Codex if its catalog has not refreshed.

The showcase vendors the generated token stylesheet so it runs on machines without the plugin. Codex uses the plugin to guide development; the website does not depend on a Codex runtime.

## Stack and checks

React 19 · TypeScript · Vite 7 · Lucide icons · IBM Plex Sans / IBM Plex Sans Arabic · Playwright / axe-core.

```sh
npm run build
npm run check:theme
npx playwright install chromium
npm run test:e2e
```

With the production preview running on port 4173, `npm run audit` runs the additional pa11y and Lighthouse accessibility checks and writes reports to `docs/audits/`.

Run the checks from `showcase/`. The browser suite starts its own production preview on port 4173 and tests the `/dga-kit/` path, not the Vite development server. Stop an existing preview first. The tests exercise user journeys and accessibility in both locales and at desktop/mobile sizes. See the verification report for the exact checks completed and remaining manual work. Automated passes are not a compliance certification.

## Boundaries

- No real authentication, Nafath integration, payment, document upload, government API, or request persistence.
- No fabricated Digital Stamp, registration number, government emblem, or official identity.
- Dark and high-contrast modes are project-authored settings; they do **not** enable DGA's published, unusable dark theme.
- Production use needs an entity-specific design review, privacy/security review, backend, appropriate registration/integrations, and manual assistive-technology testing.
- Kit coverage is a dated harvest: **50 component specifications, all 19 templates, and 303 consumable token values, as of 2026-08-27**. It is not a claim that this app implements every component or that all live DGA material has been verified today.
