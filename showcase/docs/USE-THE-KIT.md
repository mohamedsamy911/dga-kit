# Demonstrating the plugin in Codex

Open this project in Codex after installing dga-kit. The site runs independently of the plugin; the plugin supplies the engineering guidance while an agent builds or reviews the site.

Try these prompts against the actual source:

> Use dga-ui-adapter and dga-rtl-i18n to add a fictional service card in Arabic and English. Keep the semantic theme and current data shape.

> Use dga-a11y to review the application form, error summary, focus movement, and footer controls in both locales. Distinguish automated evidence from manual findings.

> Use dga-design-review to inspect the service-details screen. Cite each finding and name any WCAG fallback where the DGA harvest is silent.

> Use dga-launch-gate to explain what would still be needed before turning this fictional demo into a real government platform. Do not describe this showcase as certified or launch-ready.

If the `dga-frontend-dev` agent is available in the agent catalog, use it for implementation. Agent availability and the plugin's skill installation are separate; this plugin manifest installs 11 skills only.

The showcase deliberately does not invoke every skill unnecessarily. `dga-react` targets DGA's own React component package, whereas this app uses native React/CSS and `dga-ui-adapter`. `dga-tokens-sync` is for a deliberate re-harvest, not ordinary UI development. Brand registration, Digital Stamp credentials, real integrations, and legal policy decisions cannot be invented to make a demo look complete.

## Installation verified on the development machine

On 2026-08-31, `codex plugin list --json` reported:

```json
{
  "pluginId": "dga-kit@dga-kit",
  "version": "0.7.2",
  "installed": true,
  "enabled": true
}
```

Codex's bundled `validate_plugin.py` also passed against that installed plugin directory. PyYAML was loaded from an isolated tooling directory for validation; no global Python package was modified. This records the original standalone build; the app was subsequently incorporated into the dga-kit repository under `showcase/` for GitHub Pages publication.
