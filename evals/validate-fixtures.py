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
# Design spec says -2%; CSS letter-spacing does not accept percentages, so the em equivalent is used.
chk('case02: display carries -2% tracking (as DGA publishes it)', t['typography']['scale']['display-2xl'].get('tracking') == '-2%')
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
chk('ui-04: display-lg carries -2% tracking (as DGA publishes it)', t['typography']['scale']['display-lg'].get('tracking') == '-2%')
chk('ui-07: background.body is #f9fafb', body == '#f9fafb', body)
chk('ui-07: an 8px radius step exists', '8px' in radius.values())
chk('ui-11: text.default is #161616', t['role']['text']['default'] == '#161616', t['role']['text']['default'])
# case 12 asserts $-prefixed annotation keys exist and must be stripped by consumers.
chk('ui-12: tokens.json carries $-prefixed annotation keys',
    any(k.startswith('$') for k in t['radius']) and any(k.startswith('$') for k in t['role']))

docd = ['0px','2px','4px','6px','8px','12px','16px','20px','24px','32px','40px','48px','64px','80px','96px','128px','160px']
chk('documented 17-step scale representable', all(d in space for d in docd),
    str([d for d in docd if d not in space]))

# --- installed-layout integrity ----------------------------------------------
# skills/ is installed on its own; harvest/, evals/ and COVERAGE.md are NOT. A reference that
# escapes the skills/ tree resolves in this repo and dangles once installed. Caught here so it
# never reaches a user.
import re as _re
_esc = []
for _dirpath, _dirnames, _files in os.walk(os.path.join(ROOT, 'skills')):
    for _f in _files:
        if not _f.endswith(('.md', '.mjs', '.ts', '.js')):
            continue
        _fp = os.path.join(_dirpath, _f)
        _rel = os.path.relpath(_fp, os.path.join(ROOT, 'skills'))
        _depth = _rel.count(os.sep)
        for _m in _re.findall(r'\.\./[A-Za-z0-9_./-]+\.(?:md|json|css|mjs|js|ts)', open(_fp, encoding='utf-8').read()):
            # how many levels does this climb, and does it leave skills/ ?
            if _m.count('../') > _depth:
                _esc.append(f'{_rel} -> {_m}')
chk('installed layout: no skill reference escapes skills/', not _esc, str(_esc))

# --- ui-12: every ratio quoted in the clean-theme case ------------------------
# This case failed twice because it was written from imagination. Every number in it is now
# derived from tokens.json and asserted here, so the fixture cannot drift from the data.
_B = t['color']['brand']
_G8 = t['color']['secondary-gold']['800']
_bg = t['role']['background']

def _near(a, b): return abs(a - b) < 0.01

chk('ui-12: text.secondary repointed to secondary-gold.800 = #945c01', _G8 == '#945c01', _G8)
chk('ui-12: repointed gold clears AA on white (5.54)', _near(cr(_G8, _bg['white']), 5.54), f'{cr(_G8, _bg["white"]):.2f}')
chk('ui-12: repointed gold clears AA on body (5.30)', _near(cr(_G8, _bg['body']), 5.30), f'{cr(_G8, _bg["body"]):.2f}')

# brand colorPalette: fg=700 must clear AA on subtle/muted/emphasized, which fg=600 does not
chk('ui-12: fg brand.700 on subtle brand.50 (6.31)', _near(cr(_B['700'], _B['50']), 6.31), f'{cr(_B["700"], _B["50"]):.2f}')
chk('ui-12: fg brand.700 on muted brand.100 (5.81)', _near(cr(_B['700'], _B['100']), 5.81), f'{cr(_B["700"], _B["100"]):.2f}')
chk('ui-12: fg brand.700 on emphasized brand.200 (4.92)', _near(cr(_B['700'], _B['200']), 4.92), f'{cr(_B["700"], _B["200"]):.2f}')
chk('ui-12: fg brand.600 would FAIL on muted - why 700 is used', cr(_B['600'], _B['100']) < 4.5, f'{cr(_B["600"], _B["100"]):.2f}')
chk('ui-12: contrast white on solid brand.600 (4.75)', _near(cr('#ffffff', _B['600']), 4.75), f'{cr("#ffffff", _B["600"]):.2f}')

# hover/pressed must go darker; brand.500 is excluded as a fill on purpose
chk('ui-12: white on brand.700 hover (6.60)', _near(cr('#ffffff', _B['700']), 6.60), f'{cr("#ffffff", _B["700"]):.2f}')
chk('ui-12: white on brand.800 pressed (8.56)', _near(cr('#ffffff', _B['800']), 8.56), f'{cr("#ffffff", _B["800"]):.2f}')
chk('ui-12: white on brand.500 FAILS - excluded as a fill', cr('#ffffff', _B['500']) < 4.5, f'{cr("#ffffff", _B["500"]):.2f}')

# the -light roles are kept, not deleted - they are usable on DGA's own dark surfaces
for _r, _v in (('primary-light', 10.75), ('secondary-light', 14.79), ('tertiary-light', 9.09)):
    _h = t['role']['text'][_r]
    chk(f'ui-12: text.{_r} on background.black ({_v})', _near(cr(_h, _bg['black']), _v), f'{cr(_h, _bg["black"]):.2f}')

# DGA defines four bands, xl included - the case must not claim otherwise
chk('ui-12: DGA defines an xl band at 1280+', t['breakpoint']['xl']['min'] == 1280)
chk('ui-12: DGA defines exactly four bands',
    sorted(k for k in t['breakpoint'] if not k.startswith('$')) == ['desktop', 'mobile', 'tablet', 'xl'])

# and the case text itself must quote these numbers, not drift from them
_c12 = open(os.path.join(ROOT, 'evals/dga-ui-adapter/cases/12-clean-theme-wiring.md'), encoding='utf-8').read()
_quoted = ['5.54', '5.30', '6.31', '5.81', '4.92', '6.60', '8.56', '3.88', '4.75', '10.75', '14.79', '9.09', '#945c01', '#166a45']
_missing = [q for q in _quoted if q not in _c12]
chk('ui-12: case text quotes the asserted ratios', not _missing, str(_missing))

# --- generated output: the % -> em conversion at the boundary ---------------
# tokens.json keeps DGA's published -2% so a re-harvest diffs clean. CSS letter-spacing does
# not accept percentages, so nothing generated may contain one. This is the check that makes
# keeping the harvested value safe.
_css = open(os.path.join(ROOT, 'skills/dga-design-system/assets/tokens.css'), encoding='utf-8').read()
_tw = open(os.path.join(ROOT, 'skills/dga-design-system/assets/tailwind-preset.js'), encoding='utf-8').read()
_css_tracking = [l.strip() for l in _css.splitlines() if '-tracking:' in l]
chk('generated CSS emits em, never %', _css_tracking and all('-0.02em' in l for l in _css_tracking),
    str([l for l in _css_tracking if '-0.02em' not in l]))
chk('generated CSS has no percentage letter-spacing', not any('%' in l for l in _css_tracking))
chk('tailwind preset emits em, never %', '"letterSpacing": "-0.02em"' in _tw and '"letterSpacing": "-2%"' not in _tw)

# --- fixture must not contradict the guidance it tests -----------------------
# Case 12 shipped three times with a defect a reviewer then correctly reported, and the rubric
# scored them as a false positive. The specific trap: an Arabic-first font stack renders LATIN
# out of the Arabic face's glyphs, so DGA's named face never renders. Assert the case agrees
# with token-wiring.md rather than trusting prose on both sides.
_tw = open(os.path.join(ROOT, 'skills/dga-ui-adapter/references/token-wiring.md'), encoding='utf-8').read()
_LATIN_FIRST = '"IBM Plex Sans", "IBM Plex Sans Arabic"'
_ARABIC_FIRST = '"IBM Plex Sans Arabic", "IBM Plex Sans"'

chk('guidance: token-wiring.md shows the Latin-first stack as correct', _LATIN_FIRST in _tw)
chk('guidance: token-wiring.md shows the Arabic-first stack as the wrong one',
    _ARABIC_FIRST in _tw and 'wrong:' in _tw)
chk('ui-12: case font stack is Latin-first', _LATIN_FIRST in _c12,
    'case still declares an Arabic-first stack, which a reviewer would correctly flag')
# The wrong order may appear in the case only inside the traps commentary, never in the input.
_c12_input = _c12.split('## expect')[0]
chk('ui-12: case INPUT never declares the Arabic-first stack', _ARABIC_FIRST not in _c12_input)

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
