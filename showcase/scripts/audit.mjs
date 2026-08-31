import { mkdir, writeFile } from 'node:fs/promises';
import { chromium } from '@playwright/test';
import pa11y from 'pa11y';
import lighthouse from 'lighthouse';
import { launch } from 'chrome-launcher';
import assert from 'node:assert/strict';

// Programmatic APIs: github.com/pa11y/pa11y and github.com/GoogleChrome/lighthouse.
// Audits launch isolated test browsers; they do not attach to a user's browser.
const baseURL = new URL(process.argv[2] || 'http://127.0.0.1:4173/dga-kit/');
if (!['localhost', '127.0.0.1', '[::1]'].includes(baseURL.hostname)) {
  throw new Error('This demonstration audit only targets a local showcase server.');
}
if (!baseURL.pathname.endsWith('/')) baseURL.pathname += '/';
baseURL.search = '';
baseURL.hash = '';
const origin = baseURL.href;
function auditURL(locale, route) {
  const url = new URL(baseURL);
  url.searchParams.set('lang', locale);
  url.hash = route;
  return url.href;
}
const chromePath = chromium.executablePath();
await mkdir('docs/audits', { recursive: true });
const summary = { date: new Date().toISOString(), origin, pa11y: [], lighthouse: [] };
// HTML_CodeSniffer treats SPA #/routes as document IDs. Review only our known
// routes; never suppress missing real anchors or unknown destinations.
const serviceIds = ['home-permit', 'municipal-appointment', 'business-license', 'community-event', 'volunteer', 'participation-certificate'];
const appRoutes = new Set(['/', '/services', '/about', '/track', '/privacy', '/accessibility', ...serviceIds.flatMap(id => [`/services/${id}`, `/apply/${id}`])]);
function isReviewedRouteAnchor(issue) {
  const href = issue.context.match(/href="([^"]+)"/)?.[1];
  return issue.code === 'WCAG2AA.Principle2.Guideline2_4.2_4_1.G1,G123,G124.NoSuchID'
    && Boolean(href?.startsWith('#/') && appRoutes.has(href.slice(1).split('?')[0]));
}
const anchorIssue = { code: 'WCAG2AA.Principle2.Guideline2_4.2_4_1.G1,G123,G124.NoSuchID', context: '<a href="#/services">Services</a>' };
assert.equal(isReviewedRouteAnchor(anchorIssue), true);
assert.equal(isReviewedRouteAnchor({ ...anchorIssue, context: '<a href="#missing">Broken anchor</a>' }), false);
assert.equal(isReviewedRouteAnchor({ ...anchorIssue, context: '<a href="#/missing-route">Broken route</a>' }), false);
assert.equal(isReviewedRouteAnchor({ ...anchorIssue, code: 'some-other-failure' }), false);
let findings = false;
for (const locale of ['ar', 'en']) {
  for (const route of ['/', '/apply/home-permit']) {
    const url = auditURL(locale, route);
    const result = await pa11y(url, {
      chromeLaunchConfig: { executablePath: chromePath, headless: true },
      standard: 'WCAG2AA',
      wait: 800,
      timeout: 30000,
      viewport: { width: 1440, height: 1000 },
    });
    const actionable = result.issues.filter(issue => !isReviewedRouteAnchor(issue));
    const reviewedRouteAnchors = result.issues.length - actionable.length;
    summary.pa11y.push({ locale, route, issues: result.issues, reviewedRouteAnchors, actionable });
    if (actionable.some(issue => issue.type === 'error')) findings = true;
    console.log(`pa11y ${locale} ${route}: ${actionable.length} actionable findings; ${reviewedRouteAnchors} reviewed SPA route anchors (raw results retained)`);
  }
  const chrome = await launch({ chromePath, chromeFlags: ['--headless', '--disable-gpu'] });
  try {
    const result = await lighthouse(auditURL(locale, '/'), {
      port: chrome.port,
      output: 'json',
      onlyCategories: ['accessibility'],
      logLevel: 'error',
    });
    if (!result || result.lhr.runtimeError) throw new Error(result?.lhr.runtimeError?.message || 'No Lighthouse result');
    await writeFile(`docs/audits/lighthouse-${locale}.json`, result.report);
    const score = result.lhr.categories.accessibility.score;
    summary.lighthouse.push({ locale, score });
    if (score !== 1) findings = true;
    console.log(`Lighthouse accessibility ${locale}: ${score === null ? 'unavailable' : Math.round(score * 100)}`);
  } finally {
    await chrome.kill();
  }
}
await writeFile('docs/audits/summary.json', `${JSON.stringify(summary, null, 2)}\n`);
if (findings) process.exitCode = 1;
