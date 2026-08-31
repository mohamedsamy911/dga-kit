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
import contextlib
import json
import os
import shutil
import sys
import tempfile
import ssl
import subprocess
from unittest.mock import MagicMock, patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'harvest'))

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except (ValueError, OSError):
        pass

import sources  # noqa: E402
import deep     # noqa: E402


def _forbid_report_write(*_args, **_kwargs):
    raise AssertionError('Offline scenarios must not overwrite the real freshness report')


sources.write_freshness = _forbid_report_write

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

# A page the browser reported from a DIFFERENT route is worse than a blocked one: the text is
# real, so it hashes and diffs cleanly, just under the wrong name. The SPA bounces deep links to
# `/`, so this is the failure most likely to actually happen.
res, pending, blocking = deep.process(
    {'/guidelines/templates/home-page': {'path': '/', 'text': 'plausible looking prose'}},
    {'sources': []})
chk('5. text captured from the wrong route is WRONG_PAGE, not a clean hash',
    res[0]['status'] == 'WRONG_PAGE' and 'sha256' not in res[0], str(res))
chk('5. a wrong-page capture blocks acceptance', len(blocking) == 1, str(blocking))
res, _, _ = deep.process(
    {'/guidelines/templates/home-page':
     {'path': '/guidelines/templates/home-page/', 'text': 'prose'}},
    {'sources': []})
chk('5. a trailing slash is not a wrong page', res[0]['status'] != 'WRONG_PAGE', str(res))

# A group source hashed from SOME of its members reads green forever while the rest go unwatched.
_inv = {'sources': [{'tier': 'B', 'url': '/guidelines/templates/{slug}'}],
        'tierA': {'bundle': {'routes': {'templates': ['/guidelines/templates/home-page',
                                                      '/guidelines/templates/hajj-template']}}}}
_seen = [{'route': '/guidelines/templates/home-page', 'sha256': 'a' * 64}]
# _record WRITES the inventory. Point it at a scratch file: a fixture that overwrote
# source-inventory.json is a mistake this repo has already made once.
_real_inv, deep.INV = deep.INV, os.path.join(tempfile.mkdtemp(), 'inv.json')
_skipped = deep._record(_inv, _seen, '2026-08-28')
chk('5. a partly-captured group is skipped, not hashed',
    'contentHash' not in _inv['sources'][0] and len(_skipped) == 1, str(_inv['sources'][0]))
_seen.append({'route': '/guidelines/templates/hajj-template', 'sha256': 'b' * 64})
_skipped = deep._record(_inv, _seen, '2026-08-28')
chk('5. a complete group is hashed with every member counted',
    _inv['sources'][0].get('memberCount') == 2 and not _skipped, str(_inv['sources'][0]))
deep.INV = _real_inv
chk('5. the real inventory was never touched by the fixture',
    io.open(deep.INV, encoding='utf-8').read().count('"tier"') > 1, 'INV redirect leaked')

_SRC = io.open(os.path.join(ROOT, 'harvest', 'sources.py'), encoding='utf-8').read()

# A capture file is untrusted input - hand-written, or from a driver on a machine this repo does
# not control - and its keys become paths. A '/'-only replacement is a POSIX assumption: on
# Windows the backslash separates too, so these walked out of harvest/snapshots/.
for _evil in (r'/x\..\..\evil', '/a/../../../etc/passwd',
              '/C:/Windows/system32/x', r'/x\\server\share'):
    _slug = deep.slug_for(_evil)
    chk('5. ' + repr(_evil) + ' cannot escape the snapshot directory',
        '/' not in _slug and '\\' not in _slug and os.sep not in _slug
        and os.path.dirname(deep.snapshot_path(_evil)) == os.path.abspath(deep.SNAPS),
        _slug)
chk('5. an ordinary route still gets a readable slug',
    deep.slug_for('/guidelines/templates/home-page') == 'guidelines__templates__home-page',
    deep.slug_for('/guidelines/templates/home-page'))

# --- --baseline must not discard accepted Tier-B review state -----------------
# deep.py writes a Tier-B hash only behind --accept, after a human read the diffs. sources()
# rebuilds every entry with contentHash=None, so a --baseline run silently threw that away.
_fresh = [{'url': '/a', 'tier': 'B', 'contentHash': None, 'verified': None},
          {'url': '/gone', 'tier': 'B', 'contentHash': None, 'verified': None},
          {'url': '/t', 'tier': 'A', 'contentHash': None, 'verified': None}]
_prev = {'sources': [
    {'url': '/a', 'tier': 'B', 'contentHash': 'a' * 64, 'hashMethod': 'browser-innertext',
     'capturedAt': '2026-08-28', 'memberCount': 3, 'verified': True},
    {'url': '/t', 'tier': 'A', 'contentHash': 'ffff', 'verified': True}]}
_tmp = os.path.join(tempfile.mkdtemp(), 'inv.json')
json.dump(_prev, io.open(_tmp, 'w', encoding='utf-8'))
_real_out, sources.OUT = sources.OUT, _tmp
_carried = sources._carry_accepted(json.loads(json.dumps(_fresh)))
sources.OUT = _real_out
_by = {s['url']: s for s in _carried}
chk('B. --baseline keeps an accepted tier-B hash',
    _by['/a']['contentHash'] == 'a' * 64 and _by['/a']['memberCount'] == 3
    and _by['/a']['hashMethod'] == 'browser-innertext', str(_by['/a']))
chk('B. a tier-B source with no prior acceptance stays null',
    _by['/gone']['contentHash'] is None, str(_by['/gone']))
chk('B. tier A is refetched, never carried',
    _by['/t']['contentHash'] is None, 'tier A must come from the live fetch, not the old file')
# Testing _carry_accepted() in isolation proves the function works, not that anything calls it -
# and break-testing showed exactly that hole: removing the call from build() failed nothing. Pin
# the call site, which is the part that can be dropped by accident.
chk('B. build() actually routes sources() through _carry_accepted',
    '_carry_accepted(sources())' in _SRC,
    'the carry-forward is unreachable; --baseline would still wipe accepted tier-B hashes')

# --- a 200 maintenance/proxy page must not become a baseline ------------------
# The failure this prevents is the quiet one: with no /assets/index-<hash> links, buildHash is
# None on both sides forever after, so every later --check compares nothing and reports a quiet
# week. The sentinel looks healthy precisely because it was blinded.
_saved = sources.fetch
for _label, _body, _status in (
        ('a maintenance page', b'<html><body>We are back soon</body></html>', 200),
        ('a captive proxy', b'<html><head><title>Sign in</title></head></html>', 200)):
    sources.fetch = lambda url, timeout=45, _b=_body, _s=_status: (_s, _b)
    try:
        sources.tier_a_baselines()
        _refused = False
    except sources.NotTheSite:
        _refused = True
    except Exception:                                  # noqa: BLE001 - any other error is a bug
        _refused = False
    chk('C. ' + _label + ' answering 200 is refused as a baseline', _refused,
        'a baseline with no build-hash tripwire reports a quiet week forever')
sources.fetch = _saved
# The nastier shape: a VALID shell - real markup, real /assets/index-<hash> links, so the build
# hashes read out fine - in front of a proxy that answers the two asset requests with a login
# page. Every response is a 200. Guarding only the shell (which an earlier version did) let this
# write a baseline carrying real-looking build hashes beside zero tokens and zero routes, and
# every later --check then compared that emptiness against itself and reported a quiet week.
_GOOD_SHELL = (b'<!doctype html><html><head>'
               b'<link rel="stylesheet" href="/assets/index-abc123.css">'
               b'<script type="module" src="/assets/index-def456.js"></script>'
               b'</head><body><div id="root"></div></body></html>')
_GOOD_CSS = b':root{' + b''.join(b'--tok-%d:#000;' % i for i in range(300)) + b'}'
_GOOD_JS = (b'"/guidelines/components/actions/buttons","/guidelines/templates/home-page",'
            b'"/guidelines/foundations/color-system","/thoughts/atomic-design"')
_PROXY = b'<!DOCTYPE html><html><head><title>Sign in</title></head><body>SSO</body></html>'


def _serve(css_body, css_status, js_body, js_status):
    def _f(url, timeout=45):
        if url.endswith('.css'):
            return css_status, css_body
        if url.endswith('.js'):
            return js_status, js_body
        if url.endswith('.xml'):
            return 200, b'<urlset><loc>https://design.dga.gov.sa/</loc></urlset>'
        if url.endswith('robots.txt'):
            return 200, b'Allow: /'
        return 200, _GOOD_SHELL
    return _f


_saved = sources.fetch
for _label, _args in (
        ('a proxy login page for the stylesheet', (_PROXY, 200, _GOOD_JS, 200)),
        ('a proxy login page for the JS bundle', (_GOOD_CSS, 200, _PROXY, 200)),
        ('a 503 on the stylesheet', (b'nope', 503, _GOOD_JS, 200)),
        ('a 503 on the JS bundle', (_GOOD_CSS, 200, b'nope', 503)),
        # The status check is only load-bearing when the BODY would otherwise pass: a CDN serving
        # stale-but-valid content under a 5xx. With a junk body the content check catches it first,
        # so deleting the status check failed nothing - which is what break-testing showed.
        ('a 503 carrying an otherwise-valid stylesheet', (_GOOD_CSS, 503, _GOOD_JS, 200)),
        ('a 503 carrying an otherwise-valid JS bundle', (_GOOD_CSS, 200, _GOOD_JS, 503)),
        ('a 403 carrying an otherwise-valid stylesheet', (_GOOD_CSS, 403, _GOOD_JS, 200)),
        ('an empty stylesheet', (b'   ', 200, _GOOD_JS, 200)),
        ('a stylesheet with almost no custom properties',
         (b':root{--only-one:#fff;}', 200, _GOOD_JS, 200)),
        ('a JS bundle with no route table', (_GOOD_CSS, 200, b'console.log(1)', 200))):
    sources.fetch = _serve(*_args)
    try:
        sources.tier_a_baselines()
        _refused = False
    except sources.NotTheSite:
        _refused = True
    except Exception:                                  # noqa: BLE001 - anything else is a bug
        _refused = False
    chk('C. a valid shell with ' + _label + ' is refused as a baseline', _refused,
        'the build hash would be recorded beside empty facts, and read as a quiet week forever')

# ...and the same fixture with HEALTHY assets must still be accepted, or the guard is just a
# refusal to work.
sources.fetch = _serve(_GOOD_CSS, 200, _GOOD_JS, 200)
try:
    _ok = sources.tier_a_baselines()
    _built = bool(_ok.get('stylesheet') and _ok.get('bundle'))
except Exception as _exc:                              # noqa: BLE001
    _built, _ok = False, str(_exc)
chk('C. a valid shell with healthy assets still builds a baseline', _built, str(_ok)[:200])

sources.fetch = lambda url, timeout=45: (503, b'<html>maintenance</html>')
try:
    sources.tier_a_baselines()
    _refused = False
except sources.NotTheSite:
    _refused = True
sources.fetch = _saved
chk('C. a non-200 shell is refused as a baseline', _refused)

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

# --- a BROKEN monitor must not look like a finding ---------------------------
# The distinction the weekly workflow runs on: exit 1 means "DGA moved, review it" and keeps the
# job green while opening an issue; exit 2 means "the sentinel could not complete". Python exits
# 1 on ANY unhandled exception, so before check_main() a DNS failure, a read timeout, a 500 or
# malformed JSON all surfaced as exit 1 - a broken monitor filing a normal review issue, weekly,
# looking healthy. Mocked here because the real failure only happens when the network is down.
import urllib.error  # noqa: E402

# Exercise the real fetch loop, not a replacement for fetch(). No network or actual sleep.
# A single timeout killed the 2026-08-31 scheduled run before it could compare anything.
def _response():
    response = MagicMock()
    response.__enter__.return_value = response
    response.status = 200
    response.read.return_value = b'complete response'
    return response


for _label, _exc in (
        ('a direct timeout', TimeoutError('brief timeout')),
        ('a wrapped timeout', urllib.error.URLError(TimeoutError('brief timeout'))),
        ('a connection reset', ConnectionResetError('brief reset'))):
    _log = io.StringIO()
    with patch.object(sources.urllib.request, 'urlopen', side_effect=[_exc, _response()]) as _get, \
            patch.object(sources.time, 'sleep') as _sleep, contextlib.redirect_stderr(_log):
        try:
            _got = sources.fetch(sources.BASE + '/sitemap.xml', timeout=7)
        except OSError as _error:
            _got = str(_error)
        chk('retry: ' + _label + ' recovers on the next GET',
            _got == (200, b'complete response') and _get.call_count == 2, str(_got))
        chk('retry: ' + _label + ' waits once and preserves the socket timeout',
            _sleep.call_args_list == [((5,), {})]
            and all(c.kwargs.get('timeout') == 7 for c in _get.call_args_list))
        chk('retry: ' + _label + ' names the exact failing URL in diagnostics',
            sources.BASE + '/sitemap.xml' in _log.getvalue() and 'attempt 1/3' in _log.getvalue())

# Recovery must also work after a read timeout, closing the incomplete response first.
_partial = _response()
_partial.read.side_effect = TimeoutError('read stalled')
with patch.object(sources.urllib.request, 'urlopen', side_effect=[_partial, _response()]), \
        patch.object(sources.time, 'sleep'), contextlib.redirect_stderr(io.StringIO()):
    try:
        _got = sources.fetch(sources.BASE + '/')
    except OSError as _error:
        _got = str(_error)
    chk('retry: a partial read is discarded and its response closed',
        _got == (200, b'complete response') and _partial.__exit__.call_count == 1)

# Exhaustion still goes through check_main(), not a successful or review-pending report.
with patch.object(sources.urllib.request, 'urlopen',
                  side_effect=urllib.error.URLError(TimeoutError('persistent timeout'))) as _get, \
        patch.object(sources.time, 'sleep') as _sleep, \
        patch.object(sources, 'write_freshness') as _write, contextlib.redirect_stderr(io.StringIO()):
    chk('retry: persistent timeout exhausts three attempts and exits 2',
        sources.check_main() == 2 and _get.call_count == 3)
    chk('retry: backoff is bounded to 5s then 10s with no final sleep',
        _sleep.call_args_list == [((5,), {}), ((10,), {})])
    chk('retry: exhaustion writes no current report', not _write.called)

for _label, _exc in (
        ('HTTP 403', urllib.error.HTTPError(sources.BASE, 403, 'Forbidden', {}, None)),
        ('HTTP 500', urllib.error.HTTPError(sources.BASE, 500, 'Server Error', {}, None)),
        ('certificate validation', urllib.error.URLError(ssl.SSLCertVerificationError('untrusted'))),
        ('DNS failure', urllib.error.URLError('name resolution failed'))):
    with patch.object(sources.urllib.request, 'urlopen', side_effect=_exc) as _get, \
            patch.object(sources.time, 'sleep') as _sleep, contextlib.redirect_stderr(io.StringIO()):
        chk('retry: ' + _label + ' remains an immediate operational failure',
            sources.check_main() == 2 and _get.call_count == 1 and not _sleep.called)

_real_fetch = sources.fetch
_FRESH_PATH = os.path.join(ROOT, 'harvest', 'FRESHNESS.md')
_fresh_before = (io.open(_FRESH_PATH, encoding='utf-8').read()
                 if os.path.exists(_FRESH_PATH) else None)

for _label, _exc in (
        ('a read timeout', TimeoutError('simulated timeout')),
        ('a DNS failure', urllib.error.URLError('simulated name resolution failure')),
        ('an HTTP 500', urllib.error.HTTPError('u', 500, 'Server Error', {}, None)),
        ('a dropped connection', ConnectionResetError('simulated reset')),
        ('malformed JSON from DGA', ValueError('Expecting value: line 1 column 1')),
        ('a shape change in the response', KeyError('stylesheet')),
        ('a maintenance page', sources.NotTheSite('shell returned HTTP 503, not 200'))):
    sources.fetch = lambda *_a, _e=_exc, **_k: (_ for _ in ()).throw(_e)
    try:
        _rc = sources.check_main()
    except BaseException as _boom:                      # noqa: BLE001 - escaping IS the bug
        _rc = f'raised {type(_boom).__name__}'
    chk(f'ops: {_label} exits 2, not 1', _rc == 2,
        f'got {_rc!r} - exit 1 tells the workflow a human should review a DGA change, when in '
        f'fact nothing was compared at all')
sources.fetch = _real_fetch

chk('ops: a failed run writes no freshness report',
    (io.open(_FRESH_PATH, encoding='utf-8').read()
     if os.path.exists(_FRESH_PATH) else None) == _fresh_before,
    'a sentinel that could not read DGA must not overwrite the last good report')

# Non-vacuous by construction: the same wrapper must still pass a real finding through as 1 and a
# clean run as 0, or "always return 2" would satisfy every check above.
_saved_check = sources.check
sources.check = lambda: 1
chk('ops: a genuine finding still exits 1', sources.check_main() == 1,
    'findings must stay distinguishable from breakage')
sources.check = lambda: 0
chk('ops: a quiet week still exits 0', sources.check_main() == 0)
sources.check = _saved_check

# And the workflow must actually act on the distinction.
_wf = io.open(os.path.join(ROOT, '.github/workflows/dga-freshness.yml'), encoding='utf-8').read()
chk('ops: the workflow fails the job on exit > 1', '-gt 1' in _wf,
    'the exit codes are meaningless unless the workflow branches on them')


def _workflow_step(name):
    """Read this workflow's named step verbatim; do not duplicate its shell logic in a test."""
    marker = '      - name: ' + name + '\n'
    assert _wf.count(marker) == 1, name
    return _wf.split(marker, 1)[1].split('\n      - ', 1)[0]


def _workflow_script(name):
    return '\n'.join(line[10:] for line in
                     _workflow_step(name).split('        run: |\n', 1)[1].splitlines())


# Bash is already used by the cross-platform installer CI. Use Git Bash on Windows, not WSL.
_bash = (os.path.join(os.environ.get('ProgramFiles', r'C:\Program Files'), 'Git', 'bin', 'bash.exe')
         if os.name == 'nt' else shutil.which('bash'))
chk('ops: Bash is available for the actual workflow regression tests', bool(_bash and os.path.isfile(_bash)))
if _bash and os.path.isfile(_bash):
    _sentinel = _workflow_script('Run the sentinel')
    _sentinel = _sentinel.replace("${{ inputs.deep && '--deep' || '' }}", '')
    _stub = ('python -c "import os,sys; print(\'test stdout\'); '
             'print(\'test stderr\',file=sys.stderr); sys.exit(int(os.environ[\'TEST_SENTINEL_EXIT\']))"')
    assert _sentinel.count('python harvest/sources.py --check') == 1
    _sentinel = _sentinel.replace('python harvest/sources.py --check', _stub)
    with tempfile.TemporaryDirectory(prefix='dga-workflow-test-') as _tmp:
        for _code in ('0', '1', '2'):
            _output = os.path.join(_tmp, 'output').replace('\\', '/')
            _summary = os.path.join(_tmp, 'summary').replace('\\', '/')
            _env = dict(os.environ, TEST_SENTINEL_EXIT=_code, SENTINEL_EXIT=_code,
                        GITHUB_OUTPUT=_output, GITHUB_STEP_SUMMARY=_summary)
            _run = subprocess.run([_bash, '-e', '-c', _sentinel], cwd=_tmp, env=_env,
                                  capture_output=True, text=True, timeout=30)
            chk(f'ops: real workflow shell preserves exit {_code}',
                _run.returncode == (2 if _code == '2' else 0), _run.stdout + _run.stderr)
            _outputs = io.open(_output, encoding='utf-8').read().splitlines()
            chk(f'ops: exit {_code} is published for downstream steps',
                bool(_outputs) and _outputs[-1] == f'exit_code={_code}', str(_outputs))
            _logged = io.open(os.path.join(_tmp, 'sentinel.log'), encoding='utf-8').read()
            chk(f'ops: exit {_code} captures stderr as well as stdout',
                'test stdout' in _logged and 'test stderr' in _logged)
            _summary_run = subprocess.run([_bash, '-e', '-c', _workflow_script('Summary')],
                                          cwd=_tmp, env=_env, capture_output=True, text=True, timeout=30)
            _text = io.open(_summary, encoding='utf-8').read()
            _expected = {'0': 'No change against', '1': '**Review pending**', '2': '**Check failed**'}[_code]
            chk(f'ops: exit {_code} has the correct human summary',
                _summary_run.returncode == 0 and _expected in _text
                and (_code != '2' or '**Review pending**' not in _text), _text)
            os.remove(_summary)
        # A setup failure that never reached the sentinel must not claim review pending either.
        _env['SENTINEL_EXIT'] = ''
        _summary_run = subprocess.run([_bash, '-e', '-c', _workflow_script('Summary')],
                                      cwd=_tmp, env=_env, capture_output=True, text=True, timeout=30)
        _text = io.open(_summary, encoding='utf-8').read()
        chk('ops: a missing sentinel result reports an incomplete check',
            _summary_run.returncode == 0 and '**Check failed**' in _text
            and '**Review pending**' not in _text)

_report_step = _workflow_step('Upload the freshness report')
_failure_step = _workflow_step('Upload diagnostics when the check could not complete')
chk('ops: the saved freshness report is uploaded only for completed checks',
    "if: always() && (steps.sentinel.outputs.exit_code == '0' || steps.sentinel.outputs.exit_code == '1')" in _report_step)
chk('ops: an incomplete check uploads only its diagnostic log',
    "if: always() && steps.sentinel.outputs.exit_code != '0' && steps.sentinel.outputs.exit_code != '1'" in _failure_step
    and 'path: sentinel.log' in _failure_step and 'harvest/FRESHNESS.md' not in _failure_step)

# Testing check_main() proves the wrapper works, not that anything calls it. Break-testing found
# exactly that hole: swapping the entry point back to bare check() failed nothing. Pin the call
# site, which is the single line that undoes all of the above.
chk('ops: the --check entry point goes through check_main()',
    'sys.exit(check_main())' in _SRC and 'sys.exit(check())' not in _SRC,
    'the wrapper is bypassed; an unhandled exception would exit 1 again')

# --- the review gate holds across all of it ----------------------------------
chk('gate: compare() writes nothing',
    'def compare(' in _SRC
    and 'json.dump' not in _SRC.split('def compare(')[1].split('def check(')[0],
    'the comparison must not be able to accept its own finding')

print()
if failures:
    print(f'{len(failures)} FAILING - the automation would miss a real change')
    sys.exit(1)
print('All automation scenarios detected correctly')
