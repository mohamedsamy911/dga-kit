#!/usr/bin/env python3
"""Validates that eval fixtures match the actual harvested tokens.

Covers both suites: evals/dga-design-review/ and evals/dga-ui-adapter/.

An eval asserting a wrong value is worse than no eval — it teaches the skill a false rule.
Run after every token re-harvest:  python3 evals/validate-fixtures.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t = json.load(open(os.path.join(ROOT, 'skills/dga-design-system/assets/tokens.json'), encoding='utf-8'))

def lum(h):
    h = h.lstrip('#')[:6]
    c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def cr(a, b):
    l1, l2 = sorted([lum(a), lum(b)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

failures = []
def chk(name, cond, detail=''):
    print(('PASS  ' if cond else 'FAIL  ') + name + ('' if cond else '  ' + detail))
    if not cond:
        failures.append(name)

space = set(t['space']['named'].values()) | set(t['space']['numeric'].values())
white = t['role']['background']['white']
gold = t['role']['text']['secondary']

chk('case03: 20px is on the DGA scale', '20px' in space)
chk('case03: 34px is not on the scale', '34px' not in space)
chk('case03: 32px/40px are the neighbours', {'32px', '40px'} <= space)
chk('case03: paragraph max-width is 720px', t['container']['paragraph-max-width'] == '720px')
chk('case01: text-secondary on white = 2.30', abs(cr(gold, white) - 2.30) < 0.01, f'{cr(gold, white):.2f}')
chk('case01: fails 3:1 large-text threshold too', cr(gold, white) < 3.0)
chk('case01: secondary-gold-800 clears AA', cr(t['color']['secondary-gold']['800'], white) >= 4.5)
chk('case02: display carries -2% tracking', t['typography']['scale']['display-2xl'].get('tracking') == '-2%')
chk('typography: 12 steps', len(t['typography']['scale']) == 12, str(len(t['typography']['scale'])))
chk('breakpoints: 600/960/1280', [t['breakpoint'][k]['token'] for k in ('mobile', 'tablet', 'desktop')] == [600, 960, 1280])
chk('icons: 24px standard', t['iconography']['$standard'] == 24)
chk('touch target: 44px', t['iconography']['$minTouchTarget'] == '44px')

# --- dga-ui-adapter suite ---------------------------------------------------
# Every value an eval case asserts must be true here, or the case teaches a false rule.
para = t['role']['text']['secondary-paragraph']
body = t['role']['background']['body']
radius = t['radius']

chk('ui-01: text.secondary is #dba102', gold == '#dba102', gold)
chk('ui-01: secondary-paragraph is #6c727e', para == '#6c727e', para)
chk('ui-01: secondary-paragraph clears AA on white', cr(para, white) >= 4.5, f'{cr(para, white):.2f}')
chk('ui-02: radius.md exists', 'md' in radius)
chk('ui-02: radius is NOT monotonic (2xl < xl)', int(radius['2xl'][:-2]) < int(radius['xl'][:-2]),
    f"2xl={radius['2xl']} xl={radius['xl']}")
chk('ui-02: radius is NOT monotonic (3xl < xl)', int(radius['3xl'][:-2]) < int(radius['xl'][:-2]),
    f"3xl={radius['3xl']} xl={radius['xl']}")
chk('ui-04: display-lg carries -2% tracking', t['typography']['scale']['display-lg'].get('tracking') == '-2%')
chk('ui-07: background.body is #f9fafb', body == '#f9fafb', body)
chk('ui-07: an 8px radius step exists', '8px' in radius.values())
chk('ui-11: text.default is #161616', t['role']['text']['default'] == '#161616', t['role']['text']['default'])
# case 12 asserts $-prefixed annotation keys exist and must be stripped by consumers.
chk('ui-12: tokens.json carries $-prefixed annotation keys',
    any(k.startswith('$') for k in t['radius']) and any(k.startswith('$') for k in t['role']))

docd = ['0px','2px','4px','6px','8px','12px','16px','20px','24px','32px','40px','48px','64px','80px','96px','128px','160px']
chk('documented 17-step scale representable', all(d in space for d in docd),
    str([d for d in docd if d not in space]))

# --- provenance + $verify convention -----------------------------------------
# A convention nothing checks is a comment style. These are the rules that make
# $source and $verify load-bearing.
STATUSES = {
    'disputed', 'confirmed-defect-in-source', 'confirmed-naming-hazard', 'confirmed-hazard',
    'likely-corrected-upstream', 'unavailable-upstream', 'dga-silent',
    'gap-in-extraction-method', 'faithful-to-source',
}
sections = [k for k, v in t.items() if k != '$meta' and isinstance(v, dict)]
missing_src = [k for k in sections if '$source' not in t[k]]
chk('provenance: every section carries $source', not missing_src, str(missing_src))

no_date = [k for k in sections
           if '$source' in t[k] and not t[k]['$source'].get('retrieved')]
chk('provenance: every $source carries a read date', not no_date, str(no_date))

bad_entries, bad_status = [], []
for k in sections:
    for e in t[k].get('$verify', []):
        if not all(f in e for f in ('key', 'issue', 'status', 'action')):
            bad_entries.append(f'{k}:{e.get("key", "?")}')
        if e.get('status') not in STATUSES:
            bad_status.append(f'{k}:{e.get("key", "?")}={e.get("status")}')
chk('$verify: every entry has key/issue/status/action', not bad_entries, str(bad_entries))
chk('$verify: every status is in the declared vocabulary', not bad_status, str(bad_status))

declared = t['$meta'].get('$conventions', {}).get('$verify', '')
chk('$verify: vocabulary is documented in $meta.$conventions',
    all(st in declared for st in STATUSES),
    str([st for st in STATUSES if st not in declared]))

# Anything recorded as disputed must also appear in the harvest cross-reference, or the
# conflict lives in one place and gets lost.
import os
xref = os.path.join(ROOT, 'harvest', 'CROSSREF-SECOND-EXTRACTION.md')
xtext = open(xref, encoding='utf-8').read() if os.path.exists(xref) else ''
orphan = [e['key'] for k in sections for e in t[k].get('$verify', [])
          if e['status'] == 'disputed' and e['key'].split('.')[-1] not in xtext]
chk('$verify: every disputed value is written up in the cross-reference', not orphan, str(orphan))

print()
if failures:
    print(f'{len(failures)} FAILING — fixtures disagree with tokens.json')
    sys.exit(1)
print('All fixtures valid against tokens.json')
