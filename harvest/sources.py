#!/usr/bin/env python3
"""The source contract for design.dga.gov.sa, and the Tier A baselines.

`harvest/source-inventory.json` is the authoritative map: every DGA page this kit depends on,
which reference file owns it, and what a change to it would invalidate. This script writes that
file and refreshes the baselines a `curl` can actually establish.

    python3 harvest/sources.py --baseline    # fetch and rewrite source-inventory.json
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

So monitoring splits in two, and the `tier` field on every source says which applies:

    tier A  - reachable by curl. Asset hash, sitemap, robots. Cheap, run often.
    tier B  - needs a headless browser driving client-side navigation. Page text, the nav route
              enumeration, the 50/19 counts. Expensive, run on a Tier A signal or quarterly.

A Tier B source therefore has `contentHash: null` until a deep harvest fills it. That is honest
missing data, not a gap to paper over with a hash of the shell.
"""
import hashlib
import io
import json
import os
import re
import sys
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


def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tier_a_baselines():
    """Everything a plain HTTP GET can establish. Nothing here needs a browser."""
    out = {}

    status, shell = fetch(BASE + '/')
    out['shell'] = {
        'url': BASE + '/', 'status': status, 'bytes': len(shell), 'sha256': sha(shell),
        'note': 'The SPA shell. Served for EVERY route, valid or not - see the module docstring. '
                'Its hash changes when DGA rebuilds, which is the same signal as the asset '
                'filename below, one request earlier.',
    }

    m = re.search(rb'href="(/assets/[^"]+\.css)"', shell)
    if m:
        css_path = m.group(1).decode()
        status, css = fetch(BASE + css_path)
        out['stylesheet'] = {
            'url': BASE + css_path, 'status': status, 'bytes': len(css), 'sha256': sha(css),
            'buildHash': css_path.split('index-')[-1].split('.css')[0],
            'customProperties': len(set(re.findall(rb'(--[^\s:{};]+)\s*:', css))),
            'note': 'THE tripwire. The filename carries Vite\'s build hash, so it changes on '
                    'every DGA deploy. This file also holds the whole token surface, including '
                    'the 402 dark-theme declarations under the unmatchable [data-theme=dark] '
                    ':root selector.',
        }

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
        'sources': sources(),
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


if __name__ == '__main__':
    if '--baseline' in sys.argv:
        summarise(build())
        print(f'\nwrote {os.path.relpath(OUT, ROOT)}')
    elif os.path.exists(OUT):
        summarise(json.load(io.open(OUT, encoding='utf-8')))
    else:
        print('No inventory yet. Run: python3 harvest/sources.py --baseline')
        sys.exit(1)
