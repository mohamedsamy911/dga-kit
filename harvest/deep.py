#!/usr/bin/env python3
"""Tier B: the deep harvest. Page TEXT, which is the one thing curl cannot reach.

WHAT TIER B IS ACTUALLY FOR
---------------------------
Less than the plan assumed. The SPA bundle turned out to carry the route table and the release
list, so `sources.py --check` already verifies the 50/19/5/6 contract and detects releases by
plain GET. What is left for a browser is the readable PROSE of a page - a wording change that
ships without a rebuild is invisible to Tier A, and prose is what every reference file quotes.

EXTRACTION IS SEPARATE FROM PROCESSING, ON PURPOSE
--------------------------------------------------
This file owns the contract - the JS to run, the normalisation, the hashing, the diff, the
classification. It does NOT own the browser. Two input modes:

    python3 harvest/deep.py --emit-js                 # print the extraction snippet
    python3 harvest/deep.py --capture captured.json   # REPORT ONLY - writes nothing
    python3 harvest/deep.py --capture c.json --accept  # accept, after reviewing the diffs
    python3 harvest/deep.py --playwright              # drive it locally (needs playwright)

THE REVIEW GATE
---------------
Reporting is read-only. `--capture` writes NO snapshot and NO hash; `--accept` is the only thing
that does, and it is the Tier B equivalent of `sources.py --baseline`.

That is not tidiness. If a run wrote the new snapshot while reporting the change, the next run
would compare live against the text it had just stored, say "unchanged", and the diff a
maintainer had not read yet would be gone - the automation would have quietly accepted its own
finding. Same reason the sentinel never rewrites `source-inventory.json`.

A NEW page is unaccepted too, not merely unchanged. A page with no baseline has never been
reviewed, so it is reported and it fails the run until someone accepts it.

A page the driver could not capture is a FAILED HARVEST, not a clean page. Every route the
driver was asked for comes back in the result set - as EMPTY if the browser returned nothing, as
MISSING if it never reported at all. Both block `--accept` entirely: a browser that quietly died
on forty routes would otherwise report "fifty-one unchanged" and be accepted as a clean run.

The split exists because the driver is the least portable part and the most likely to rot, while
the contract is what has to stay identical across drivers. It also means a capture taken by hand
in devtools is processed by exactly the same code as an automated one.

> The `--playwright` path needs `pip install playwright && playwright install chromium`. It is
> NOT exercised by this repo's CI and has not been run here. `--capture` is the tested path.

THREE TRAPS, ALL HIT FOR REAL
-----------------------------
1. Deep-linking bounces to `/`. The router only responds to a real click on an in-page anchor.
2. `document.querySelector('main')` returns the NAVIGATION DRAWER. The content `<main>` is the
   one containing the `<h1>` - walk up from the heading instead.
3. The default locale is Arabic. Switch to English first or half the corpus is in the wrong
   language and every hash churns the first time someone runs it the other way.

WHERE THE TEXT GOES
-------------------
`harvest/snapshots/` - machine-owned, overwritten every run, used only for hashing and diffing.
It is deliberately NOT `harvest/raw/`: those captures are human-curated evidence with `<!-- dga -->`
fences marking which passages are DGA's words, and auto-dumping page text into them would put
unfenced noise into the quote-fidelity corpus. Promote a snapshot into a raw capture by hand,
with fences, when you need to cite it.
"""
import difflib
import hashlib
import io
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(ROOT, 'harvest', 'source-inventory.json')
SNAPS = os.path.join(ROOT, 'harvest', 'snapshots')
BASE = 'https://design.dga.gov.sa'

# The single source of truth for extraction. Both drivers run exactly this, so a hash taken by
# hand and a hash taken by Playwright are comparable.
EXTRACT_JS = r'''
(async (path) => {
  // 1. real click - the address bar bounces every deep link to /
  const a = document.querySelector('a[href="' + path + '"]');
  if (!a) return { error: 'no in-page link to ' + path };
  a.click();
  await new Promise(r => setTimeout(r, 3000));
  // 2. the FIRST <main> is the navigation drawer; the content one holds the <h1>
  let m = document.querySelector('h1');
  while (m && m.tagName !== 'MAIN') m = m.parentElement;
  if (!m) return { error: 'no content <main> for ' + path };
  return { path: location.pathname, text: m.innerText };
})('{{PATH}}')
'''.strip()

# Chrome that appears on every page and would otherwise dominate the hash.
CHROME = re.compile(
    r'(Contact Us\s*Connect With Us.*$)'
    r'|(Design Language\s*Guidelines\s*Documentations.*$)'
    r'|(on this page\s*$)',
    re.S | re.M)


def normalise(text):
    """Page prose only, stable across runs.

    The footer and the contact block are identical on every page; leaving them in means every
    hash shares ~400 characters of noise and a footer edit churns all 80 at once.
    """
    t = CHROME.sub('', text or '')
    t = t.replace('—', '-').replace('–', '-')
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


def digest(text):
    return hashlib.sha256(normalise(text).encode('utf-8')).hexdigest()


def slug_for(route):
    return route.strip('/').replace('/', '__') or 'root'


def load_inventory():
    return json.load(io.open(INV, encoding='utf-8'))


def tier_b_routes(inv):
    """Concrete routes to visit - group patterns expanded from the bundle's route table."""
    out, bundle = [], (inv['tierA'].get('bundle') or {}).get('routes') or {}
    for s in inv['sources']:
        if s['tier'] != 'B':
            continue
        if '{' not in s['url']:
            out.append(s['url'])
            continue
        for group in ('components', 'templates', 'foundations', 'thoughts'):
            if s['url'].startswith('/guidelines/' + group) or s['url'].startswith('/' + group):
                out += bundle.get(group, [])
                break
    return sorted(set(out))


def process(captures, inv, accept=False, expected=None):
    """captures: {route: innerText} -> (results, pending, blocking).

    `accept` is False by default and nothing is written in that mode - see THE REVIEW GATE.
    `expected` is the route list the driver was ASKED for; anything absent from `captures` comes
    back as MISSING rather than vanishing from the report.
    """
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    results, pending_writes = [], []
    todo = dict(captures)
    for route in (expected or []):
        todo.setdefault(route, None)
    for route, text in sorted(todo.items()):
        if text is None and route not in captures:
            results.append({'route': route, 'status': 'MISSING',
                            'note': 'the driver never reported this route'})
            continue
        if not isinstance(text, str) or not text.strip():
            results.append({'route': route, 'status': 'EMPTY', 'note': 'driver returned no text'})
            continue
        norm = normalise(text)
        h = hashlib.sha256(norm.encode('utf-8')).hexdigest()
        path = os.path.join(SNAPS, slug_for(route) + '.txt')
        was = io.open(path, encoding='utf-8').read() if os.path.exists(path) else None
        if was is None:
            status, diff = 'NEW', ''
        elif hashlib.sha256(was.encode('utf-8')).hexdigest() == h:
            status, diff = 'unchanged', ''
        else:
            status = 'CHANGED'
            diff = '\n'.join(list(difflib.unified_diff(
                was.splitlines(), norm.splitlines(),
                fromfile='baseline', tofile='live', lineterm=''))[:40])
        pending_writes.append((path, norm))
        results.append({'route': route, 'status': status, 'sha256': h,
                        'chars': len(norm), 'capturedAt': now, 'diff': diff})

    # NEW counts as pending: a page with no baseline has never been reviewed, so accepting it
    # silently at exit 0 would let a whole first harvest through unread.
    pending = [r for r in results if r['status'] in ('CHANGED', 'NEW', 'EMPTY', 'MISSING')]
    # A harvest with holes in it cannot be accepted at all - accepting the pages that DID come
    # back would record a partial run as the new baseline, and the missing ones would then look
    # unchanged forever. All or nothing.
    blocking = [r for r in results if r['status'] in ('EMPTY', 'MISSING')]

    if accept and not blocking:
        os.makedirs(SNAPS, exist_ok=True)
        for path, norm in pending_writes:
            io.open(path, 'w', encoding='utf-8').write(norm)
        _record(inv, results, now)
    return results, pending, blocking


def _record(inv, results, now):
    """Write hashes back onto the matching tier-B source entries.

    hashMethod is what makes a tier-B hash meaningful: the SPA shell is byte-identical for every
    route, so a hash without browser provenance can only be the shell and would go green forever.
    evals/validate-fixtures.py enforces that.
    """
    by_route = {r['route']: r for r in results if r.get('sha256')}
    for s in inv['sources']:
        if s['tier'] != 'B':
            continue
        if s['url'] in by_route:
            hit = [by_route[s['url']]]
        else:
            prefix = s['url'].split('{', 1)[0].rstrip('/') if '{' in s['url'] else None
            hit = [r for rt, r in by_route.items()
                   if prefix and rt.startswith(prefix + '/')] if prefix else []
        if not hit:
            continue
        if len(hit) == 1 and hit[0]['route'] == s['url']:
            s['contentHash'] = hit[0]['sha256']
        else:
            # A group entry hashes the set, so any member changing moves it.
            joined = ''.join(h['sha256'] for h in sorted(hit, key=lambda x: x['route']))
            s['contentHash'] = hashlib.sha256(joined.encode()).hexdigest()
            s['memberCount'] = len(hit)
        s['hashMethod'] = 'browser-innertext'
        s['capturedAt'] = now
    json.dump(inv, io.open(INV, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)


def report(results, pending, blocking, accepted):
    print(f'Tier B deep harvest  {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")}')
    counts = {}
    for r in results:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    print('  ' + ' · '.join(f'{v} {k}' for k, v in sorted(counts.items())))
    for r in results:
        if r['status'] in ('CHANGED', 'EMPTY', 'NEW', 'MISSING'):
            print(f'\n  {r["status"]}  {r["route"]}')
            if r.get('diff'):
                for line in r['diff'].splitlines()[:20]:
                    print('    ' + line)
    if blocking:
        print(f'\n  {len(blocking)} route(s) did not come back. This is a FAILED HARVEST, not a')
        print('  clean run - the pages that did return are not trustworthy as a baseline while')
        print('  others are missing, so acceptance is refused outright.')
        if accepted:
            print('\n  --accept REFUSED. Nothing was written. Fix the driver and re-run.')
        return 2
    if accepted:
        print(f'\n  ACCEPTED {len(pending)} page(s): snapshots written to harvest/snapshots/ and')
        print('  hashes recorded in source-inventory.json. Do this only after reading the diffs.')
        return 0
    if pending:
        print(f'\n  {len(pending)} page(s) pending review. NOTHING WAS WRITTEN - no snapshot, no')
        print('  hash, no change in skills/. The diffs above stay reproducible until you accept.')
        print('  Update the guidance first, then:')
        print('      python3 harvest/deep.py --capture <file> --accept')
        return 1
    return 0


def drive_playwright(routes):
    """Local driver. Needs `pip install playwright && playwright install chromium`.

    NOT exercised by this repo's CI, and not run when this file was written - `--capture` is the
    tested path. Treat this as a convenience wrapper over the contract above, not as the contract.
    """
    from playwright.sync_api import sync_playwright
    # Seeded with every requested route. A route the browser fails on must come back as an empty
    # capture, not disappear - otherwise a driver that died halfway reports the pages it managed
    # as the whole harvest, and they look clean.
    out = {r: None for r in routes}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(BASE + '/', wait_until='networkidle')
        for el in page.query_selector_all('a, button'):
            if (el.inner_text() or '').strip() == 'English':
                el.click()
                page.wait_for_timeout(2500)
                break
        for route in routes:
            try:
                res = page.evaluate(EXTRACT_JS.replace('{{PATH}}', route))
                if res and res.get('text'):
                    out[route] = res['text']
                else:
                    print(f'  FAILED {route}: {res.get("error") if res else "no result"}',
                          file=sys.stderr)
            except Exception as exc:                      # noqa: BLE001 - record, keep going
                print(f'  FAILED {route}: {exc}', file=sys.stderr)
        browser.close()
    return out


def main():
    inv = load_inventory()
    if '--emit-js' in sys.argv:
        print(EXTRACT_JS)
        return 0
    if '--routes' in sys.argv:
        print('\n'.join(tier_b_routes(inv)))
        return 0
    expected = None
    if '--capture' in sys.argv:
        src = sys.argv[sys.argv.index('--capture') + 1]
        captures = json.load(io.open(src, encoding='utf-8'))
        # A hand-made capture file is allowed to be a deliberate subset, so `expected` is what
        # the file claims. `--all` asserts it covers every tier-B route instead.
        if '--all' in sys.argv:
            expected = tier_b_routes(inv)
    elif '--playwright' in sys.argv:
        expected = tier_b_routes(inv)
        captures = drive_playwright(expected)
    else:
        print(__doc__.strip().splitlines()[0])
        print('\n  --emit-js | --routes | --capture <file.json> | --playwright')
        return 0
    accept = '--accept' in sys.argv
    results, pending, blocking = process(captures, inv, accept=accept, expected=expected)
    return report(results, pending, blocking, accept)


if __name__ == '__main__':
    sys.exit(main())
