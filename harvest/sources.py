#!/usr/bin/env python3
"""The source contract for design.dga.gov.sa, and the Tier A baselines.

`harvest/source-inventory.json` is the authoritative map: every DGA page this kit depends on,
which reference file owns it, and what a change to it would invalidate. This script writes that
file and refreshes the baselines a `curl` can actually establish.

    python3 harvest/sources.py --baseline    # fetch and rewrite source-inventory.json
    python3 harvest/sources.py --check       # sentinel: diff live vs baseline, write FRESHNESS.md
    python3 harvest/sources.py               # print the inventory summary, fetch nothing

WHAT THE SITE ALLOWS US TO MONITOR - measured, not assumed
----------------------------------------------------------
design.dga.gov.sa is a client-rendered SPA served from a Vite build. Three consequences shape
everything here, and each was verified against the live site on 2026-08-27:

1. EVERY route returns the same 4,417-byte app shell with HTTP 200 - including routes that do
   not exist (`/this-route-does-not-exist-xyz` returns 200). So HTTP status can NEVER detect a
   removed or renamed page, and a per-route content hash is identical for every route in the
   site. Any monitor built on either would be permanently green and prove nothing.

2. The shell links one stylesheet, `/assets/index-<vite-hash>.css`. That filename changes on
   every DGA deploy, which makes it a free and exact "DGA shipped something" tripwire - cheaper
   and more reliable than hashing any page. The file itself carries the entire token surface,
   including the 402 dark-theme declarations.

3. `sitemap.xml` exists and is fetchable, but it is STALE: it lists 34 components and 16
   templates against the real 50 and 19, and its template set is exactly the Sep 2024 release.
   It is a lower-bound signal - if it grows, something happened - and must never be used as the
   route count.

4. The JS bundle is a static asset too, and it CONTAINS THE ROUTE TABLE - all 50 component
   slugs, all 19 template slugs, the 5 foundations, the 6 Thoughts articles, and one route per
   published release (`version-history-1-0-3`). So the route contract and "has DGA released?"
   are answerable by curl after all. Only page PROSE needs a browser.

   That is a better split than the plan assumed, and it is why `--check` can verify the counts.
   Thoughts routes are stored without a leading slash (`"thoughts/atomic-design"`); the
   extractor allows for that, and would silently under-count if it did not.

So monitoring splits in two, and the `tier` field on every source says which applies:

    tier A  - reachable by curl: asset hashes, sitemap, robots, the ROUTE TABLE and the
              release list out of the JS bundle, and the critical token facts out of the CSS.
              Cheap, run often.
    tier B  - needs a headless browser driving client-side navigation: the readable text of a
              page. Expensive, run on a Tier A signal or quarterly.

COST. The bundles are ~19 MB together, too heavy to pull weekly for nothing. `--check` therefore
fetches the 4 KB shell first and reads the Vite build hashes out of it. If they match the
baseline, DGA has not deployed and there is nothing a deep read could find, so it stops. The
bundles are only downloaded when something actually shipped.

A Tier B source therefore has `contentHash: null` until a deep harvest fills it. That is honest
missing data, not a gap to paper over with a hash of the shell.
"""
import hashlib
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date, timezone, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'harvest', 'source-inventory.json')
BASE = 'https://design.dga.gov.sa'
UA = 'dga-kit source inventory (+https://github.com/mohamedsamy911/dga-kit)'

# --- the contract ----------------------------------------------------------
# Counts this kit asserts everywhere. They are here so a re-harvest that finds a different
# number fails loudly instead of quietly changing what the skills claim. Both have been wrong
# before: the template count was published as 19 while the harvest actually held 17.
COMPONENTS = {
    'actions': ['buttons', 'chip', 'dropdown', 'floating-Button', 'link'],
    'content-display': ['accordion', 'card', 'carousel', 'code-snippet', 'digital-stamp',
                        'divider', 'list', 'quote'],
    'data-display': ['avatar', 'charts', 'content-switcher', 'metric', 'structured-list', 'table'],
    'feedback': ['modal', 'notification', 'rating', 'tooltip'],
    'forms-and-inputs': ['checkbox', 'datepicker', 'file-uploader', 'input', 'number-input',
                         'radio', 'slider', 'steps', 'switch', 'textarea'],
    'loading-and-status': ['loading', 'progress-bar', 'radial-stepper', 'skeleton'],
    'navigational': ['breadcrumbs', 'menu', 'pagination', 'slide-out', 'tabs'],
    'search-and-filters': ['filtration', 'search-box', 'tags'],
    'ui-shell': ['footer', 'navigation-drawer', 'navigation-header', 'second-nav-header',
                 'table-of-content'],
}
TEMPLATES = ['about-page', 'chatbot', 'contact-us-page', 'content-page', 'cookies-banner',
             'e-participation-page', 'faqs-page', 'feedback-section', 'form-page', 'founding-day',
             'hajj-template', 'help-page', 'home-page', 'national-day', 'page-not-found',
             'rating-section', 'search-page', 'service-page', 'sitemap-page']
FOUNDATIONS = ['color-system', 'elevation', 'iconography', 'layout-and-spacing', 'typography']
THOUGHTS = ['AccessibilityEase', 'atomic-design', 'consistency-and-unified-identity',
            'designToken', 'localAndGlobal', 'responsive-design']

DS = 'skills/dga-design-system/references/'


# A custom property is an ident at the START of a declaration - after `{` or `;`. The first
# version of this pattern anchored on nothing, so `.btn--close[disabled],.btn--sort:hover`
# matched as a property named `--close[disabled],.btn--sort` and 83 BEM class fragments were
# counted as tokens: 1,209 reported against 1,126 real. Excluding the selector characters
# `,[]()` while keeping the class otherwise broad matters - DGA declares `--colors-rose-*`
# with a non-ASCII acute, so an [A-Za-z0-9_-] ident class drops 14 real properties. Verified
# against an independent block parser (harvest/reconcile-tokens.py): both give 1,126 exactly.
CUSTOM_PROP = rb'[{;]\s*(--[^\s:{};,\[\]()]+)\s*:'


def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


class NotTheSite(Exception):
    """The response was served, but it is not the site this sentinel knows how to read."""


def asset_problem(kind, status, body):
    """Why this response is not the asset it claims to be - or None if it is.

    A valid shell says NOTHING about the assets. The shell can be served from a CDN edge or a
    stale cache while a proxy answers the two asset requests with a login page, and every one of
    those responses is a 200. That combination is the dangerous one: the build hash is read out of
    the SHELL markup, so a poisoned baseline records a real-looking hash beside zero tokens and
    zero routes - and from then on every --check compares that emptiness against itself and reports
    a quiet week. Guarding the shell alone, which is what an earlier version of this file did,
    misses it entirely.

    Deliberately structural, not exact: "is this a stylesheet at all", not "does it have 1,209
    properties". A real DGA change to the counts must reach compare() as a reported finding, not
    be swallowed here as a refusal to look.
    """
    if status != 200:
        return f'{kind} returned HTTP {status}'
    head = body[:400].lstrip().lower()
    if head.startswith(b'<!doctype html') or head.startswith(b'<html'):
        return f'{kind} responded with an HTML page - a proxy, login or maintenance response'
    if not body.strip():
        return f'{kind} responded with an empty body'
    if kind == 'stylesheet':
        n = len(set(re.findall(CUSTOM_PROP, body)))
        if n < 100:
            return (f'stylesheet declares {n} custom properties; DGA publishes over a thousand, '
                    f'so this is not the token surface')
    else:
        r = routes_from_js(body)
        empty = [g for g in ('components', 'templates', 'foundations') if not r[g]]
        if empty:
            return 'bundle carries no ' + ', '.join(empty) + ' routes - no route table to read'
    return None


def tier_a_baselines():
    """Everything a plain HTTP GET can establish. Nothing here needs a browser.

    REFUSES to record a baseline with no tripwires. A maintenance page, a captive proxy or a
    corporate interstitial answers 200 with real HTML and no /assets/index-<hash> links. Writing
    that as the baseline is the worst possible outcome: buildHash becomes None on both sides, so
    every later --check compares nothing against nothing and reports a quiet week forever. The
    sentinel would look healthy precisely because it had been blinded.
    """
    out = {}

    status, shell = fetch(BASE + '/')
    if status != 200:
        raise NotTheSite(f'shell returned HTTP {status}, not 200')
    out['shell'] = {
        'url': BASE + '/', 'status': status, 'bytes': len(shell), 'sha256': sha(shell),
        'note': 'The SPA shell. Served for EVERY route, valid or not - see the module docstring. '
                'Its hash changes when DGA rebuilds, which is the same signal as the asset '
                'filename below, one request earlier.',
    }

    m = re.search(rb'href="(/assets/[^"]+\.css)"', shell)
    if not m:
        raise NotTheSite(
            f'no /assets/index-<hash>.css link in the shell ({len(shell)} bytes, HTTP {status}). '
            f'Either DGA changed the markup - update the pattern - or this is a maintenance or '
            f'proxy page. Refusing to write a baseline with no build-hash tripwire.')
    css_path = m.group(1).decode()
    status, css = fetch(BASE + css_path)
    bad = asset_problem('stylesheet', status, css)
    if bad:
        raise NotTheSite(
            bad + f' ({BASE + css_path}, {len(css)} bytes). The shell was valid, so this is most '
            f'likely a proxy or maintenance response for the asset alone. Refusing to write a '
            f'baseline whose token facts are empty - it would read as a quiet week forever.')
    out['stylesheet'] = {
        'url': BASE + css_path, 'status': status, 'bytes': len(css), 'sha256': sha(css),
        'buildHash': css_path.split('index-')[-1].split('.css')[0],
        'customProperties': len(set(re.findall(CUSTOM_PROP, css))),
        'facts': facts_from_css(css),
        'note': 'THE tripwire. The filename carries Vite\'s build hash, so it changes on '
                'every DGA deploy. This file also holds the whole token surface, including '
                'the 402 dark-theme declarations under the unmatchable [data-theme=dark] '
                ':root selector.',
    }

    m = re.search(rb'src="(/assets/[^"]+\.js)"', shell)
    if not m:
        raise NotTheSite(
            'no /assets/index-<hash>.js link in the shell. Refusing to write a baseline with no '
            'route table - the 50/19/5/6 contract would be unverifiable.')
    js_path = m.group(1).decode()
    status, js = fetch(BASE + js_path)
    bad = asset_problem('bundle', status, js)
    if bad:
        raise NotTheSite(
            bad + f' ({BASE + js_path}, {len(js)} bytes). The shell was valid, so this is most '
            f'likely a proxy or maintenance response for the asset alone. Refusing to write a '
            f'baseline with no route table - the 50/19/5/6 contract would be unverifiable.')
    r = routes_from_js(js)
    out['bundle'] = {
        'url': BASE + js_path, 'status': status, 'bytes': len(js), 'sha256': sha(js),
        'buildHash': js_path.split('index-')[-1].split('.js')[0],
        'routes': r,
        'counts': {k: len(v) for k, v in r.items()},
        'note': 'The SPA bundle carries the route table and one route per release. This is '
                'what makes the 50/19 contract and "has DGA released?" answerable without a '
                'browser. Only page prose still needs one.',
    }

    if 'stylesheet' in out:
        # re-read the stylesheet we already fetched above for the critical token facts
        pass

    status, sm = fetch(BASE + '/sitemap.xml')
    urls = [u.replace(BASE, '') or '/' for u in re.findall(r'<loc>(.*?)</loc>', sm.decode('utf-8'))]
    out['sitemap'] = {
        'url': BASE + '/sitemap.xml', 'status': status, 'sha256': sha(sm),
        'urlCount': len(urls),
        'componentsListed': len([u for u in urls if u.startswith('/guidelines/components/')]),
        'templatesListed': len([u for u in urls if u.startswith('/guidelines/templates/')
                                and u.count('/') > 2]),
        'urls': sorted(urls),
        'note': 'SIGNAL ONLY - do not derive counts from this. It is stale: it lists far fewer '
                'components and templates than the site publishes, and its template set matches '
                'the Sep 2024 release. Growth in this list means something changed; its size '
                'never means the site is that size.',
    }

    status, rb = fetch(BASE + '/robots.txt')
    out['robots'] = {
        'url': BASE + '/robots.txt', 'status': status, 'sha256': sha(rb),
        'body': rb.decode('utf-8').strip(),
        'note': 'Allow: / - monitoring is permitted. Note the Sitemap: line still points at the '
                'scaffold default yourdomain.com; recorded as a DGA defect, not a typo here.',
    }
    return out


# Routes live in the JS bundle as quoted strings. Thoughts entries omit the leading slash, so
# it is optional here - requiring it silently returned zero Thoughts routes on the first attempt.
ROUTE_IN_JS = re.compile(rb'["\'`](/?(?:guidelines|thoughts|updates)/[A-Za-z0-9_./-]+)["\'`]')
VERSION_ROUTE = re.compile(rb'version-history-([0-9-]+)')


def version_key(v):
    """Order dotted versions numerically.

    A string compare puts '1.0.9' above '1.0.10', so the sentinel would report the wrong latest
    version from DGA's tenth patch onward - and would do it quietly, in the row a reader trusts
    most. At roughly four releases a year that is about two years away, which is exactly long
    enough for nobody to remember why it broke.

    Defensive about non-numeric segments: DGA has only shipped x.y.z, but a '1.1.0-beta' would
    make a bare int() raise and take the whole check down on the run that mattered.
    """
    out = []
    for seg in str(v).split('.'):
        m = re.match(r'(\d+)', seg.strip())
        out.append(int(m.group(1)) if m else 0)
    return tuple(out)


def routes_from_js(js):
    """The published route table, straight out of the SPA bundle."""
    found = {('/' + m.decode().lstrip('/')) for m in ROUTE_IN_JS.findall(js)}
    def group(prefix, depth):
        return sorted(r for r in found if r.startswith(prefix) and r.count('/') >= depth)
    return {
        'components': group('/guidelines/components/', 4),
        'templates': group('/guidelines/templates/', 3),
        'foundations': group('/guidelines/foundations/', 3),
        'thoughts': group('/thoughts/', 2),
        'releases': sorted({m.decode().replace('-', '.') for m in VERSION_ROUTE.findall(js)},
                           key=version_key),
    }


def _declared(css, name):
    m = re.search(rb'--' + name.encode() + rb':\s*([^;}]+)', css)
    return m.group(1).decode().strip() if m else None


def _resolve(css, value, depth=0):
    """Follow one var() reference to the literal behind it.

    DGA declares its semantic roles as references - `--text-secondary:var(--colors-secondary-
    gold-600-primary)` - so matching only a literal hex returns None and the fact silently stops
    being watched. Both levels are recorded: the role can be repointed at a different primitive,
    or the primitive itself can be recoloured, and either is a change worth a human deciding on.
    """
    if not value or depth > 4:
        return value
    m = re.fullmatch(r'var\(\s*--([^,)\s]+)\s*\)', value)
    return _resolve(css, _declared(css, m.group(1)), depth + 1) if m else value


def facts_from_css(css):
    """The critical token facts a plain GET can settle."""
    ts = _declared(css, 'text-secondary')
    return {
        'text.secondary.declared': ts,
        'text.secondary.resolved': _resolve(css, ts),
        'darkSelectorUnmatchable': b'[data-theme=dark] :root' in css,
        'darkSelectorFixed': b':root[data-theme=dark]' in css or b':root[data-theme="dark"]' in css,
        'customProperties': len(set(re.findall(CUSTOM_PROP, css))),
    }


def sources():
    """Every page this kit depends on, with the reference file that owns it."""
    def s(url, category, owns, tier='B', **kw):
        d = {'url': url, 'category': category, 'owns': owns, 'tier': tier,
             'contentHash': None, 'verified': None}
        d.update(kw)
        return d

    why_b = 'SPA: the page text only exists after client-side navigation, so no curl can hash it.'

    # `owns` is derived from the provenance header each reference file declares, not from
    # intuition - an earlier version listed only the obvious owner per route group and missed
    # four real dependants, which defeats the point of a source contract. `routeOwners` carries
    # the per-slug exceptions inside a group.
    out = [
        s('/guidelines/foundations/{slug}', 'foundation',
          [DS + 'foundations.md', DS + 'accessibility.md', DS + 'content.md',
           'skills/dga-design-system/assets/tokens.json'],
          routes=FOUNDATIONS, expectedCount=5, why=why_b,
          routeOwners={
              'color-system': [DS + 'CONTRAST-AUDIT.md',
                               'skills/dga-design-system/assets/check-contrast.mjs'],
              'typography': [DS + 'brand.md'],
              'iconography': [DS + 'brand.md'],
          }),
        s('/guidelines/components/{category}/{slug}', 'component',
          [DS + 'components.md', DS + 'accessibility.md', DS + 'content.md', DS + 'mobile.md'],
          routes=COMPONENTS, expectedCount=50, why=why_b,
          note='accessibility.md is sourced from "the Accessibility section of every component '
               'page", so a change to ANY component page can stale it.'),
        s('/guidelines/templates/{slug}', 'template',
          [DS + 'patterns.md', DS + 'brand.md', DS + 'content.md', DS + 'mobile.md'],
          routes=TEMPLATES, expectedCount=19, why=why_b),

        # The six Thoughts articles have genuinely different dependants, so they are listed
        # individually rather than as one group with a single owner.
        s('/thoughts/AccessibilityEase', 'guidance', [DS + 'accessibility.md'], why=why_b),
        s('/thoughts/atomic-design', 'guidance', [DS + 'foundations.md'], why=why_b),
        s('/thoughts/consistency-and-unified-identity', 'guidance', [DS + 'brand.md'], why=why_b,
          watch='The only page explaining WHY the palette is what it is - the besht gold that '
                'became text.secondary.'),
        s('/thoughts/designToken', 'guidance',
          [DS + 'foundations.md', 'skills/dga-tokens-sync/SKILL.md'], why=why_b),
        s('/thoughts/localAndGlobal', 'guidance',
          [DS + 'foundations.md', 'skills/dga-launch-gate/SKILL.md'], why=why_b),
        s('/thoughts/responsive-design', 'guidance', [DS + 'foundations.md'], why=why_b),
        s('/AssessmentCriteria', 'assessment',
          ['skills/dga-launch-gate/references/assessment-criteria.md',
           'skills/dga-launch-gate/references/checklist.md'],
          why=why_b,
          watch='The four Mandatory criteria, and DGA\'s hedge "typically cannot proceed to '
                'deployment". A change here changes a go/no-go call.'),
        s('/updates/change-log', 'release',
          ['skills/dga-design-system/dga-version.md', 'skills/dga-tokens-sync/SKILL.md'],
          why=why_b,
          watch='A new /updates/change-log/version-history-* route is the definitive "DGA '
                'released" signal. Current published version: 1.0.3 (4 Nov 2025).'),
        s('/updates/roadmap', 'release', ['skills/dga-tokens-sync/references/library-migration.md'],
          why=why_b,
          watch='Dates here disagree with the change log by a year. Cite the change log.'),
        s('/designing', 'guidance', [DS + 'patterns.md'], why=why_b),
        s('/designing-for-mobile', 'guidance', [DS + 'mobile.md'], why=why_b),
        s('/design-installation', 'guidance', [DS + 'brand.md'], why=why_b),
        s('/migration-guide', 'guidance',
          ['skills/dga-tokens-sync/references/library-migration.md'], why=why_b),
        s('/developing', 'guidance', ['skills/dga-react/references/official-packages.md'],
          why=why_b),
        s('/contributing', 'guidance', [DS + 'foundations.md'], why=why_b),
        s('/support', 'guidance', [DS + 'foundations.md'], why=why_b,
          watch='Written for an internal DGA audience; treat as intent, not a citeable rule. '
                'foundations.md declares it as a source alongside /contributing, and quotes its '
                'claims about Storybook and the "beem community" - both of which are not live, '
                'so a change here can turn a documented not-yet into a yes.'),
        s('/about-platforms-code', 'guidance', [], why=why_b,
          watch='Publishes a "33+ components" counter that contradicts the 50 published '
                'component routes. Recorded as a conflict, never reconciled.'),
    ]
    return out


def _carry_accepted(fresh):
    """Preserve Tier-B hashes that a human already accepted.

    sources() rebuilds every entry with contentHash=None. Letting that land discards the one
    thing in this file the automation is not allowed to decide: deep.py writes a Tier-B hash only
    behind --accept, after a maintainer has read the diffs. Regenerating it as null throws that
    review away silently, and every accepted page reads NEW on the next deep harvest - which then
    blocks acceptance, so the damage is loud but the review is gone either way.

    Tier A is deliberately NOT carried: it is refetched on every --baseline by design.
    """
    if not os.path.exists(OUT):
        return fresh
    old = {s['url']: s for s in json.load(io.open(OUT, encoding='utf-8')).get('sources', [])}
    for s in fresh:
        prev = old.get(s['url'])
        if s['tier'] != 'B' or not prev:
            continue
        for k in ('contentHash', 'hashMethod', 'capturedAt', 'memberCount', 'verified'):
            if prev.get(k) is not None:
                s[k] = prev[k]
    return fresh


def build():
    print('fetching Tier A baselines...')
    tier_a = tier_a_baselines()
    doc = {
        '$meta': {
            'purpose': 'Authoritative map of every design.dga.gov.sa page this kit depends on, '
                       'which reference file owns it, and what a change would invalidate.',
            'source': BASE + '/',
            'generated': date.today().isoformat(),
            'generatedBy': 'harvest/sources.py --baseline',
            'publishedVersion': '1.0.3',
            'publishedVersionDate': '2025-11-04',
            'publishedVersionSource': BASE + '/updates/change-log',
        },
        '$ownershipScope':
            'owns[] lists the reference files that declare a DGA page as their SOURCE. Files '
            'derived from those references - dga-ui-adapter/references/component-mapping.md, '
            'token-wiring.md, dga-rtl-i18n/references/rtl-rules.md - are NOT listed: this kit\'s '
            'architecture is that rules live once in dga-design-system/references/, and those '
            'files read from it rather than from DGA. Follow the chain through the owning '
            'reference, not around it. Append-only records are also excluded: '
            'references/capture-log.md logs what was captured and when, so a DGA change does '
            'not make it wrong - it stays true as history. dga-version.md IS listed, because a '
            'release means the pin itself must change.',
        '$constraints': [
            'Every route returns the same SPA shell with HTTP 200, including routes that do not '
            'exist. HTTP status can never detect a removed or renamed page, and a per-route '
            'content hash is identical for every route. Verified 2026-08-27.',
            'Page text requires a headless browser driving client-side navigation - a real '
            'click on a nav anchor. Address-bar deep links bounce to /.',
            'sitemap.xml is stale and is a lower-bound signal only. Never derive counts from it.',
            'The stylesheet filename carries the Vite build hash and is the cheapest exact '
            'signal that DGA deployed.',
        ],
        'contracts': {
            'thoughtsRoutes': THOUGHTS,
            'components': 50,
            'templates': 19,
            'foundations': 5,
            'thoughts': 6,
            'note': 'Asserted by evals/validate-fixtures.py. Both counts have been wrong in this '
                    'repo before - the templates figure was published as 19 while the harvest '
                    'held 17 - so they are machine-checked rather than trusted.',
        },
        'criticalFacts': [
            {'fact': 'published version', 'value': '1.0.3',
             'where': '/updates/change-log',
             'breaks': 'skills/dga-design-system/dga-version.md and every "current version" claim'},
            {'fact': 'mandatory assessment criteria', 'value': 4,
             'where': '/AssessmentCriteria',
             'breaks': 'skills/dga-launch-gate - a go/no-go verdict'},
            {'fact': 'dark theme selector', 'value': '[data-theme=dark] :root',
             'where': 'the stylesheet',
             'breaks': 'If DGA adds the missing space, its dark theme activates everywhere at '
                       'once and tokens.json role.dark stops being audit-only. Highest-impact '
                       'single change on this list.'},
            {'fact': 'text.secondary', 'value': '#dba102',
             'where': 'the stylesheet',
             'breaks': 'The kit\'s headline finding. If DGA darkens it, CONTRAST-AUDIT.md, '
                       'check-contrast.mjs and rule 2 of dga-ui-adapter all change.'},
        ],
        'tierA': tier_a,
        'sources': _carry_accepted(sources()),
    }
    with io.open(OUT, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write('\n')
    return doc


def summarise(doc):
    ta = doc['tierA']
    print(f"\nsource-inventory.json  generated {doc['$meta']['generated']}  "
          f"PC {doc['$meta']['publishedVersion']}")
    print(f"  contracts: {doc['contracts']['components']} components, "
          f"{doc['contracts']['templates']} templates, "
          f"{doc['contracts']['foundations']} foundations, {doc['contracts']['thoughts']} thoughts")
    if 'stylesheet' in ta:
        print(f"  stylesheet build {ta['stylesheet']['buildHash']}  "
              f"{ta['stylesheet']['bytes']:,}b  {ta['stylesheet']['customProperties']} custom props")
    print(f"  sitemap lists {ta['sitemap']['urlCount']} urls "
          f"({ta['sitemap']['componentsListed']} components, "
          f"{ta['sitemap']['templatesListed']} templates) - STALE, signal only")
    b = [s for s in doc['sources'] if s['tier'] == 'B']
    print(f"  page sources: {len(doc['sources'])}, all tier B - {len(b)} need a browser, "
          f"because no page's text is reachable by curl")
    print(f"  tier A is the {len(ta)} assets above, not pages: they are the only things a plain "
          f"GET can meaningfully hash")


def compare(base, obs, contracts):
    """Baseline vs what this run observed. Pure: no network, no files, no clock.

    Split out of check() so every scenario - a release, a token recoloured, a template removed,
    a blocked page - can be exercised offline from a fixture instead of by mutating the real
    baseline and hitting the live site. See evals/test-automation.py.

    It REPORTS. It never edits the contract: a live count that disagrees with the contract is a
    finding for a human, not a number to quietly adopt.
    """
    out = []

    if obs.get('sitemapSha') and obs['sitemapSha'] != base.get('sitemap', {}).get('sha256'):
        live, was = set(obs.get('sitemapUrls') or []), set(base.get('sitemap', {}).get('urls') or [])
        out.append(('sitemap changed', f'+{sorted(live - was)} -{sorted(was - live)}'))
    if obs.get('robotsSha') and obs['robotsSha'] != base.get('robots', {}).get('sha256'):
        out.append(('robots.txt changed', obs.get('robotsText', '')))

    routes = obs.get('routes')
    if routes:
        for group in ('components', 'templates', 'foundations', 'thoughts'):
            got = routes.get(group) or []
            want = contracts.get(group)
            if want is not None and len(got) != want:
                out.append((f'{group} count broke the contract',
                            f'{len(got)} live vs {want} contracted'))
            was = set((base.get('bundle') or {}).get('routes', {}).get(group) or [])
            if was and set(got) != was:
                out.append((f'{group} routes changed',
                            f'+{sorted(set(got) - was)} -{sorted(was - set(got))}'))

        was_rel = set((base.get('bundle') or {}).get('routes', {}).get('releases') or [])
        new_rel = sorted(set(routes.get('releases') or []) - was_rel, key=version_key)
        if new_rel:
            out.append(('NEW RELEASE published', ', '.join(new_rel)))

    for k, was_v in ((base.get('stylesheet') or {}).get('facts') or {}).items():
        if obs.get('facts') is None:
            break                      # not read this run - absence is not a change
        if obs['facts'].get(k) != was_v:
            out.append((f'critical fact changed: {k}', f'{was_v!r} -> {obs["facts"][k]!r}'))
    return out


def check():
    """Tier A sentinel. Diffs the live site against the recorded baseline.

    Never writes the baseline: a detected change stays reported until a human accepts it with
    --baseline. That is the review gate - the automation reports, it does not decide.
    """
    if not os.path.exists(OUT):
        print('No inventory. Run: python3 harvest/sources.py --baseline')
        return 2
    inv = json.load(io.open(OUT, encoding='utf-8'))
    base = inv['tierA']
    findings, notes = [], []
    # Everything this run actually saw. The report renders THIS, not the baseline - a report that
    # prints baseline values under the heading "observed" contradicts its own findings, and does
    # so precisely on the deploy you are reading it for.
    obs = {'checkedAt': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ'),
           'deepRead': False, 'cssHash': None, 'jsHash': None,
           'counts': None, 'releases': None, 'facts': None}

    status, shell = fetch(BASE + '/')
    obs['shellSha256'] = sha(shell)
    obs['shellStatus'] = status
    css_m = re.search(rb'href="(/assets/[^"]+\.css)"', shell)
    js_m = re.search(rb'src="(/assets/[^"]+\.js)"', shell)
    obs['cssHash'] = css_m.group(1).decode().split('index-')[-1].split('.css')[0] if css_m else None
    obs['jsHash'] = js_m.group(1).decode().split('index-')[-1].split('.js')[0] if js_m else None

    old_css = base.get('stylesheet', {}).get('buildHash')
    old_js = base.get('bundle', {}).get('buildHash')
    deployed = (obs['cssHash'] != old_css) or (obs['jsHash'] != old_js)

    # A rebuild that renames the assets, or changes how the shell links them, leaves these
    # unmatched. Dereferencing them here would crash BEFORE the report is written - losing the
    # findings on the one run that mattered. Treat it as review-pending and skip the deep read.
    missing = [n for n, m in (('stylesheet', css_m), ('bundle', js_m)) if m is None]
    if missing:
        findings.append(('SHELL MARKUP CHANGED - could not locate ' + ' and '.join(missing),
                         f'The shell no longer matches the /assets/index-<hash>.(css|js) pattern '
                         f'this sentinel reads. shell HTTP {status}, sha256 '
                         f'{obs["shellSha256"][:16]}..., {len(shell)} bytes. Deep read skipped: '
                         f'update the asset pattern in harvest/sources.py, then re-run.'))

    # Cheap regardless - a few KB.
    _, sm = fetch(BASE + '/sitemap.xml')
    obs['sitemapSha'] = sha(sm)
    obs['sitemapUrls'] = sorted({u.replace(BASE, '') or '/' for u in
                                 re.findall(r'<loc>(.*?)</loc>', sm.decode('utf-8'))})
    _, rb = fetch(BASE + '/robots.txt')
    obs['robotsSha'] = sha(rb)
    obs['robotsText'] = rb.decode('utf-8').strip()

    if missing:
        notes.append('Deep read skipped - the shell asset pattern did not match, so there was '
                     'nothing safe to fetch. Route counts and token facts were NOT observed '
                     'this run; the table below says so rather than reprinting the baseline.')
    elif not deployed and '--deep' not in sys.argv:
        notes.append(f'No deploy: build hashes unchanged (css {old_css}, js {old_js}). '
                     f'The 19 MB bundles were not downloaded - nothing a deep read could find '
                     f'has changed. Use --deep to force.')
    else:
        if deployed:
            findings.append(('DGA DEPLOYED',
                             f'css {old_css} -> {obs["cssHash"]}, '
                             f'js {old_js} -> {obs["jsHash"]}'))
        css_status, css = fetch(BASE + css_m.group(1).decode())
        js_status, js = fetch(BASE + js_m.group(1).decode())
        # Here a bad asset is a FINDING, not an exception. check() must always write its report -
        # raising would lose the findings on the one run that mattered, the same reasoning as the
        # SHELL MARKUP CHANGED branch above. Nothing observed is claimed from an asset that
        # failed: obs keeps its None, and the report says so rather than reprinting the baseline.
        bad = [p for p in (asset_problem('stylesheet', css_status, css),
                           asset_problem('bundle', js_status, js)) if p]
        if bad:
            findings.append(('ASSET RESPONSE NOT USABLE - deep read abandoned',
                             '; '.join(bad) + '. The shell was valid and the build hashes were '
                             'read from it, so this is most likely a proxy or maintenance '
                             'response for the assets alone. Route counts and token facts were '
                             'NOT observed this run.'))
            notes.append('Deep read abandoned - an asset response was not the asset. Nothing '
                         'below is claimed as observed for routes or token facts.')
        else:
            obs['deepRead'] = True
            live_routes = routes_from_js(js)
            obs['routes'] = live_routes
            obs['counts'] = {k: len(v) for k, v in live_routes.items()}
            obs['releases'] = live_routes['releases']
            obs['facts'] = facts_from_css(css)

    findings += compare(base, obs, inv['contracts'])
    write_freshness(inv, obs, findings, notes)
    print('DGA freshness check  ' + obs['checkedAt'])
    for n in notes:
        print('  note   ' + n)
    if findings:
        print(f'\n  {len(findings)} finding(s) - REVIEW PENDING:')
        for title, detail in findings:
            print(f'    {title}\n      {detail}')
        print('\n  Nothing was updated. Read harvest/FRESHNESS.md, decide, then accept with')
        print('  python3 harvest/sources.py --baseline')
        return 1
    print('  no change against the recorded baseline')
    return 0


def write_freshness(inv, obs, findings, notes):
    """Render what THIS RUN observed, with the baseline alongside for comparison.

    Everything labelled "observed" comes from `obs`. Where a run did not look - the cheap path
    skips the bundles - the row says so instead of reprinting the baseline under a live heading.
    """
    ta = inv['tierA']

    def cmp_hash(live, was):
        if live is None:
            return '`—` **not found**'
        return f'`{live}`' if live == was else f'`{live}` ⚠️ **was** `{was}`'

    ver = max(obs['releases'], key=version_key) if obs.get('releases') else None
    ver_row = (f'**{ver}** (observed in the bundle this run)' if ver else
               f'{inv["$meta"]["publishedVersion"]} — *baseline value; releases not read this run*')

    L = [
        '# Freshness',
        '',
        'Generated by `python3 harvest/sources.py --check`. Do not edit by hand.',
        '',
        '| | |', '|---|---|',
        f'| Last sentinel check | **{obs["checkedAt"]}** |',
        f'| Baseline recorded | {inv["$meta"]["generated"]} |',
        f'| DGA version | {ver_row} |',
        f'| CSS build | {cmp_hash(obs["cssHash"], ta.get("stylesheet", {}).get("buildHash"))} |',
        f'| JS build | {cmp_hash(obs["jsHash"], ta.get("bundle", {}).get("buildHash"))} |',
        f'| Deep read this run | {"yes" if obs["deepRead"] else "no"} |',
        f'| Review pending | {"**YES**" if findings else "no"} |',
        '',
        '## Route counts',
        '',
    ]
    if obs['counts']:
        L += ['| Group | Observed | Contract | |', '|---|---|---|---|']
        for g in ('components', 'templates', 'foundations', 'thoughts'):
            live = obs['counts'].get(g, '—')
            want = inv['contracts'].get(g, '—')
            L.append(f'| {g} | **{live}** | {want} | {"✅" if live == want else "🚩"} |')
        L += ['', '> Counts come from the route table inside the SPA bundle, not from '
              '`sitemap.xml`,', '> which is stale and is a lower-bound signal only.', '']
    else:
        L += ['**Not observed this run.** The bundles were not downloaded, so no live count was',
              'taken. Last recorded values, from the baseline of '
              f'{inv["$meta"]["generated"]}:', '',
              '| Group | Baseline | Contract |', '|---|---|---|']
        b = (ta.get('bundle') or {}).get('counts') or {}
        for g in ('components', 'templates', 'foundations', 'thoughts'):
            L.append(f'| {g} | {b.get(g, "—")} | {inv["contracts"].get(g, "—")} |')
        L += ['', '> These are **not** live readings. Run `--deep` to force one.', '']

    if findings:
        L += ['## Findings — a human must decide', '']
        for title, detail in findings:
            L += [f'### {title}', '', f'```', detail, '```', '']
        L += ['Nothing in this repo was changed. Accept the new state with',
              '`python3 harvest/sources.py --baseline` once the guidance has been updated.', '']
    else:
        L += ['## Findings', '', 'None. The live site matches the recorded baseline.', '']

    for n in notes:
        L += [f'> {n}', '']

    L += ['## Known evidence gaps',
          '',
          'Carried from `COVERAGE.md`; the sentinel does not measure these.',
          '',
          '- The Assessment Criteria **checklist file** (the rubric page is captured, the file is not)',
          '- Digital Transformation and Digital Experience Maturity indicators (published off-site)',
          '- PC 1.0 Figma files — responsive radius and spacing resolve per breakpoint there only',
          '- The Arabic-language terminology harvest',
          '',
          '## What this check cannot see',
          '',
          '- **Page prose.** Every route returns the same SPA shell, so readable text needs a',
          '  browser. A wording change with no rebuild is invisible here.',
          '- **A page removed without a rebuild.** Route removal is detected from the bundle, so',
          '  it needs a deploy to surface.',
          '']
    io.open(os.path.join(ROOT, 'harvest', 'FRESHNESS.md'), 'w', encoding='utf-8').write('\n'.join(L))


def check_main():
    """`--check`, with operational failures separated from findings.

    THE DISTINCTION THE WORKFLOW DEPENDS ON:
      0  nothing changed
      1  a finding - DGA moved, a human must review. The job stays green; an issue is opened.
      2  the sentinel itself could not complete.

    Python exits 1 on any unhandled exception, so before this wrapper a DNS failure, a read
    timeout, a 500, or malformed JSON all surfaced as exit 1 - indistinguishable from "DGA
    changed". The weekly job would go green and open an issue claiming a review was pending,
    while the monitor was simply broken. A monitor that cannot report its own failure is the
    thing this repo has spent five rounds guarding against.
    """
    try:
        return check()
    except NotTheSite as exc:
        print(f'\nSENTINEL FAILED: {exc}', file=sys.stderr)
        print('This is an operational failure, NOT a finding. Nothing was compared.',
              file=sys.stderr)
        return 2
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        print(f'\nSENTINEL FAILED: could not reach {BASE} - {type(exc).__name__}: {exc}',
              file=sys.stderr)
        print('Network or transport failure. No comparison was made, so nothing is known about '
              'whether DGA changed.', file=sys.stderr)
        return 2
    except (ValueError, KeyError, TypeError) as exc:
        # Malformed JSON, a missing baseline key, a shape change in what DGA served.
        print(f'\nSENTINEL FAILED: {type(exc).__name__}: {exc}', file=sys.stderr)
        print('The sentinel could not parse what it fetched or read. Not a finding.',
              file=sys.stderr)
        return 2


if __name__ == '__main__':
    if '--check' in sys.argv:
        sys.exit(check_main())
    if '--baseline' in sys.argv:
        summarise(build())
        print(f'\nwrote {os.path.relpath(OUT, ROOT)}')
    elif os.path.exists(OUT):
        summarise(json.load(io.open(OUT, encoding='utf-8')))
    else:
        print('No inventory yet. Run: python3 harvest/sources.py --baseline')
        sys.exit(1)
