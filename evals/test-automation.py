#!/usr/bin/env python3
"""Does the monitoring actually detect what it claims to?

The rest of the eval suite checks the kit's CONTENT against DGA. This file checks the
AUTOMATION: given a known change, does the sentinel report it, with the right words, and
without quietly fixing anything.

That distinction matters because a monitor that silently stops working looks exactly like a
monitor with nothing to report. Every scenario below was a real ad-hoc test during development,
mutating the live baseline and restoring it afterwards. Here they are fixtures, so they run every
time instead of once.

Six scenarios, from the plan:

  1. a no-change run
  2. a new DGA version
  3. a changed token
  4. a new or removed template
  5. a blocked source page
  6. a DGA contradiction - which must be REPORTED, never silently resolved

  python3 evals/test-automation.py
  python3 evals/test-automation.py --ci    # exit 1 on any failure (same as default)
"""
import io
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'harvest'))

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except (ValueError, OSError):
        pass

import sources  # noqa: E402
import deep     # noqa: E402

failures = []


def chk(name, cond, detail=''):
    print(('PASS  ' if cond else 'FAIL  ') + name + (f'  {detail}' if not cond and detail else ''))
    if not cond:
        failures.append(name)


def titles(findings):
    return [t for t, _ in findings]


def has(findings, needle):
    return any(needle.lower() in t.lower() for t in titles(findings))


# The shape a healthy run sees. Deliberately small and hand-written rather than a copy of the
# real inventory: a fixture that tracks production stops being able to fail.
BASE = {
    'stylesheet': {'buildHash': 'CSS1', 'facts': {
        'text.secondary.declared': 'var(--colors-secondary-gold-600-primary)',
        'text.secondary.resolved': '#dba102',
        'darkSelectorUnmatchable': True,
        'darkSelectorFixed': False,
        'customProperties': 1209,
    }},
    'bundle': {'buildHash': 'JS1', 'routes': {
        'components': ['/guidelines/components/actions/buttons'],
        'templates': ['/guidelines/templates/home-page', '/guidelines/templates/hajj-template'],
        'foundations': ['/guidelines/foundations/color-system'],
        'thoughts': ['/thoughts/atomic-design'],
        'releases': ['1.0.0', '1.0.3'],
    }},
    'sitemap': {'sha256': 'SM1', 'urls': ['/', '/guidelines']},
    'robots': {'sha256': 'RB1'},
}
CONTRACTS = {'components': 1, 'templates': 2, 'foundations': 1, 'thoughts': 1}


def observed(**over):
    """A live reading identical to the baseline, except where a scenario changes it."""
    obs = {
        'cssHash': 'CSS1', 'jsHash': 'JS1',
        'sitemapSha': 'SM1', 'sitemapUrls': list(BASE['sitemap']['urls']),
        'robotsSha': 'RB1', 'robotsText': '',
        'routes': json.loads(json.dumps(BASE['bundle']['routes'])),
        'facts': dict(BASE['stylesheet']['facts']),
    }
    obs['counts'] = {k: len(v) for k, v in obs['routes'].items()}
    for k, v in over.items():
        obs[k] = v
    return obs


print('Automation scenarios - does the monitoring detect what it claims to?\n')

# --- 1. no change ------------------------------------------------------------
f = sources.compare(BASE, observed(), CONTRACTS)
chk('1. a quiet week reports nothing at all', f == [], str(f))

# --- 2. a new DGA version ----------------------------------------------------
o = observed()
o['routes']['releases'] = ['1.0.0', '1.0.3', '1.0.4']
f = sources.compare(BASE, o, CONTRACTS)
chk('2. a new release is reported', has(f, 'NEW RELEASE'), str(titles(f)))
chk('2. the release is named in the finding',
    any('1.0.4' in d for t, d in f if 'RELEASE' in t), str(f))

# the ordering bug that would misreport the tenth patch
o = observed()
o['routes']['releases'] = ['1.0.0', '1.0.3', '1.0.9', '1.0.10']
f = sources.compare(BASE, o, CONTRACTS)
chk('2. releases past the ninth patch are ordered numerically',
    any(d.startswith('1.0.9, 1.0.10') for t, d in f if 'RELEASE' in t), str(f))

# --- 3. a changed token ------------------------------------------------------
o = observed()
o['facts']['text.secondary.resolved'] = '#945c01'
f = sources.compare(BASE, o, CONTRACTS)
chk('3. a recoloured token is reported', has(f, 'text.secondary.resolved'), str(titles(f)))
chk('3. the finding carries both values',
    any("'#dba102' -> '#945c01'" in d for _, d in f), str(f))

# the single highest-impact change DGA could make
o = observed()
o['facts']['darkSelectorUnmatchable'] = False
o['facts']['darkSelectorFixed'] = True
f = sources.compare(BASE, o, CONTRACTS)
chk('3. DGA fixing the dark selector is reported', has(f, 'darkSelector'), str(titles(f)))
chk('3. both halves of the dark-selector change are reported', len(f) == 2, str(titles(f)))

# --- 4. a new or removed template --------------------------------------------
o = observed()
o['routes']['templates'] = ['/guidelines/templates/home-page',
                            '/guidelines/templates/hajj-template',
                            '/guidelines/templates/new-thing']
f = sources.compare(BASE, o, CONTRACTS)
chk('4. an added template breaks the contract', has(f, 'templates count'), str(titles(f)))
chk('4. the added route is named', any('new-thing' in d for _, d in f), str(f))

o = observed()
o['routes']['templates'] = ['/guidelines/templates/home-page']
f = sources.compare(BASE, o, CONTRACTS)
chk('4. a removed template is reported', has(f, 'templates'), str(titles(f)))
chk('4. the removed route is named', any('hajj-template' in d for _, d in f), str(f))

# A rename is an add AND a remove, and must not net out to silence.
o = observed()
o['routes']['templates'] = ['/guidelines/templates/home-page',
                            '/guidelines/templates/hajj-2027']
f = sources.compare(BASE, o, CONTRACTS)
chk('4. a rename is reported even though the count is unchanged',
    has(f, 'templates routes changed'), str(titles(f)))

# --- 5. a blocked source page -------------------------------------------------
# Tier A: the shell markup moved, so the assets cannot be located. check() turns that into a
# finding before any deref; here we assert the safe half - nothing is claimed as observed.
o = observed(cssHash=None, jsHash=None, routes=None, facts=None, counts=None)
f = sources.compare(BASE, o, CONTRACTS)
chk('5. an unreadable bundle claims no route or token findings',
    not has(f, 'count') and not has(f, 'critical fact'), str(titles(f)))

# Tier B: a page the driver could not take must not read as clean.
res, pending, blocking = deep.process({'/x/page': None}, {'sources': []})
chk('5. a blocked page is EMPTY, not clean',
    res[0]['status'] == 'EMPTY' and len(blocking) == 1, str(res))
res, pending, blocking = deep.process({}, {'sources': []}, expected=['/x/a', '/x/b'])
chk('5. a page the driver never reported is MISSING',
    sorted(r['status'] for r in res) == ['MISSING', 'MISSING'], str(res))
chk('5. a failed harvest cannot be accepted', len(blocking) == 2, str(blocking))

# --- 6. a contradiction is reported, never resolved ---------------------------
# (a) live vs contract. The sentinel must report the disagreement and NOT adopt the live number:
#     a monitor that rewrites its own contract has stopped being a contract.
snapshot = json.loads(json.dumps(CONTRACTS))
o = observed()
o['routes']['components'] = ['/guidelines/components/actions/buttons',
                             '/guidelines/components/actions/chip']
f = sources.compare(BASE, o, CONTRACTS)
chk('6. a live count contradicting the contract is reported',
    has(f, 'components count broke the contract'), str(titles(f)))
chk('6. the contract is NOT rewritten to match', CONTRACTS == snapshot,
    'compare() must never adopt the live value')

# (b) contradictions DGA publishes about itself stay recorded with both sides, rather than being
#     quietly settled in favour of whichever number the kit prefers.
_cov = io.open(os.path.join(ROOT, 'COVERAGE.md'), encoding='utf-8').read()
chk('6. the 33+ vs 50 component contradiction is still recorded with both numbers',
    '33+' in _cov and '50' in _cov and 'reconcile' in _cov.lower(), '')
chk('6. the roadmap vs change-log date contradiction is still recorded',
    'roadmap' in _cov.lower() and 'change-log' in _cov.lower()
    and 'Feb 2024' in _cov and '2025' in _cov, '')

# --- the review gate holds across all of it ----------------------------------
_src = io.open(os.path.join(ROOT, 'harvest', 'sources.py'), encoding='utf-8').read()
chk('gate: compare() writes nothing',
    'def compare(' in _src
    and 'json.dump' not in _src.split('def compare(')[1].split('def check(')[0],
    'the comparison must not be able to accept its own finding')

print()
if failures:
    print(f'{len(failures)} FAILING - the automation would miss a real change')
    sys.exit(1)
print('All automation scenarios detected correctly')
