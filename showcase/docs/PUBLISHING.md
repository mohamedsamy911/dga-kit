# Publishing the showcase

Public site: [وصل · Wasl](https://mohamedsamy911.github.io/dga-kit/).
This is a fictional, unofficial demo, not a government service or compliance certificate.

## GitHub Pages setup

In the repository's **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
The root [Showcase Pages workflow](../../.github/workflows/showcase-pages.yml) owns deployment.
It runs on relevant pushes to `master`, pull requests, and manual dispatches.

The build job installs the showcase's lockfile with Node 22, builds the app, checks the theme,
and runs the browser suite against the production preview at `/dga-kit/`. Only a successful
build on this repository's `master` can upload `showcase/dist` and deploy. Pull requests and
forks cannot deploy through this workflow. The deploy job alone receives Pages write and OIDC
permissions. The existing plugin CI remains separate and must also pass before landing changes.

No custom domain, backend, secrets, or external analytics are needed. Do not configure branch
publishing from the repository root: that would publish the wrong content. Do not commit
`node_modules`, `dist`, Playwright reports, or local logs.

## Local production check

From the repository root:

```sh
cd showcase
npm ci
npx playwright install chromium
npm run build
npm run check:theme
npm run test:e2e
```

For an interactive preview, run `npm run preview` and open
[the local demo](http://127.0.0.1:4173/dga-kit/). Browser tests start and stop their own preview;
stop an existing preview on that port before running the suite.

The Vite base is `/dga-kit/`. Hash routes such as `#/services/home-permit` support direct links
and reloads without server rewrite rules. If the repository name or hosting path changes,
update the Vite base, browser test base and prefix expectations, audit URL, documentation links,
and workflow repository guard together. Re-run the production checks before deploying.

The vendored token stylesheet is a pinned dga-kit 0.7.2 snapshot, not an automatic link to the
root harvest. A token upgrade must update the copied generated output, source snapshot, hash
guard, and evidence together after review; never edit a generated token to fix app styling.

## Verification and recovery

After a push, confirm both **CI** and **Showcase Pages** succeeded for that commit. Open the live
Arabic and English entry points and a service hash link; check assets, console errors, and
refresh behavior. An Actions success alone does not prove the public page works.

For a regression, revert the faulty showcase commit through the normal review process and let
the workflow deploy the corrected build. Manual dispatch on `master` can redeploy the current
version; it does not roll back source changes. Never disable tests to force a deployment.

References: [Vite's project-site base guidance](https://vite.dev/guide/static-deploy#github-pages)
and [GitHub's custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
