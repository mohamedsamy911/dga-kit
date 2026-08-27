#!/usr/bin/env python3
"""Validates that eval fixtures match the actual harvested tokens.

Covers both suites: evals/dga-design-review/ and evals/dga-ui-adapter/.

An eval asserting a wrong value is worse than no eval — it teaches the skill a false rule.
Run after every token re-harvest:  python3 evals/validate-fixtures.py
"""
import json, os, re, sys

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

# --- dark theme -------------------------------------------------------------
# DGA ships 402 dark declarations under `[data-theme=dark] :root` - a selector that can never
# match, because :root is <html> and a descendant combinator needs an ancestor it does not have.
# The values are real and correct; only the selector is broken. These assertions keep three
# things from quietly regressing: that we carry the dark roles at all, that we emit NO live dark
# rule (the guard is with the generated-output checks below), and that the dark defects stay
# visible - text.error, text.primary, and the five un-remapped *-light surfaces.
_d = t['role'].get('dark')
chk('dark: tokens.json carries role.dark', bool(_d and _d.get('text') and _d.get('background')))

if _d:
    chk('dark: every light text role has a dark counterpart',
        {k for k in t['role']['text'] if not k.startswith('$')} ==
        {k for k in _d['text'] if not k.startswith('$')})
    chk('dark: every light background role has a dark counterpart',
        {k for k in t['role']['background'] if not k.startswith('$')} ==
        {k for k in _d['background'] if not k.startswith('$')})

    # The five *-light status surfaces are NOT remapped by DGA's dark block, so they keep their
    # near-white light values while text.default flips to #ffffff. This is the worst pairing in
    # either theme. Asserting equality pins it as a recorded defect, not an oversight of ours.
    _carried = ['brand-light', 'error-light', 'info-light', 'success-light', 'warning-light']
    for _k in _carried:
        chk(f'dark: background.{_k} is carried at its LIGHT value (DGA does not remap it)',
            _d['background'][_k] == t['role']['background'][_k],
            'if this ever differs, DGA fixed it upstream - re-run the spike and update $verify')
    chk('dark: white text on the un-remapped brand-light surface is ~1.05:1',
        round(cr(_d['text']['default'], _d['background']['brand-light']), 2) == 1.05)

    chk('dark: text.error fails AA at every size on the dark body',
        round(cr(_d['text']['error'], _d['background']['body']), 2) == 2.68)
    chk('dark: text.primary is large-text-only on the dark body',
        3 <= cr(_d['text']['primary'], _d['background']['body']) < 4.5)
    # The light-theme headline finding is NOT absolute - record why.
    chk('dark: text.secondary PASSES on dark, so the 2.30:1 finding is light-theme only',
        round(cr(_d['text']['secondary'], _d['background']['body']), 2) == 7.64)

    chk('dark: $verify records the unmatchable selector as a source defect',
        any('[data-theme=dark] :root' in v.get('value', '') for v in _d.get('$verify', [])))

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

# A nested object reaching a token emit point stringifies to "[object Object]" and passes every
# other check silently. This happened when role.dark was added and the light :root loop swallowed
# it. Cheap guard, real bug.
_tw = open(os.path.join(ROOT, 'skills/dga-design-system/assets/tailwind-preset.js'), encoding='utf-8').read()
chk('generated CSS has no stringified objects', '[object Object]' not in _css)
chk('generated preset has no stringified objects', '[object Object]' not in _tw)

# The shipped stylesheet must contain NO live dark rule. DGA's dark theme is inert upstream
# because its selector cannot match, and inert is safe: emitting a corrected selector would
# activate 1.05:1 pairings for any consumer already using data-theme="dark" (Chakra v3 does).
# The values stay in tokens.json for audit. See generate-tokens.mjs for the full reasoning.
_css_rules = [l for l in _css.splitlines() if l and not l.startswith((' ', '\t')) and '{' in l]
chk('generated CSS ships no live dark rule',
    not any('data-theme' in l for l in _css_rules),
    str([l for l in _css_rules if 'data-theme' in l]))
chk('generated CSS still explains why dark is withheld',
    'Dark theme is NOT emitted here' in _css)
chk('generated preset sets no darkMode strategy', 'darkMode:' not in _tw,
    'shipping no dark colours but flipping the dark: variant is a behaviour change for nothing')
# P2: light and dark were read on different dates. One date on the banner is wrong for half of it.
chk('generated CSS banner carries both retrieval dates',
    'Light values retrieved: ' + t['$meta']['retrieved'] in _css
    and 'Dark values retrieved:  ' + t['role']['dark']['$source']['retrieved'] in _css)
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

# --- the source contract ------------------------------------------------------
# harvest/source-inventory.json is the map the monitoring is built on. If it drifts from the
# kit it describes, every later check inherits the drift, so it is pinned here rather than
# trusted. Both counts below have been wrong in this repo before.
_inv_path = os.path.join(ROOT, 'harvest/source-inventory.json')
chk('inventory: harvest/source-inventory.json exists', os.path.exists(_inv_path),
    'run: python3 harvest/sources.py --baseline')

if os.path.exists(_inv_path):
    _inv = json.load(open(_inv_path, encoding='utf-8'))
    _by_cat = {s2['category']: s2 for s2 in _inv['sources'] if 'routes' in s2}

    _n_comp = sum(len(v) for v in _by_cat['component']['routes'].values())
    chk('inventory: component routes match the declared contract',
        _n_comp == _inv['contracts']['components'] == 50,
        f"{_n_comp} routes vs contract {_inv['contracts']['components']}")
    chk('inventory: template routes match the declared contract',
        len(_by_cat['template']['routes']) == _inv['contracts']['templates'] == 19)
    chk('inventory: foundation routes match the declared contract',
        len(_by_cat['foundation']['routes']) == _inv['contracts']['foundations'] == 5)
    # Thoughts are listed one source per article, not as a group: the six have genuinely
    # different dependants (AccessibilityEase -> accessibility.md, consistency -> brand.md), and
    # a single group owner hid four real dependencies in the first version of this file.
    _thoughts = sorted(s2['url'] for s2 in _inv['sources'] if s2['url'].startswith('/thoughts/'))
    chk('inventory: thoughts routes match the declared contract',
        len(_thoughts) == _inv['contracts']['thoughts'] == 6,
        str(_thoughts))
    chk('inventory: every thoughts article is listed as its own source',
        _thoughts == sorted('/thoughts/' + x for x in _inv['contracts']['thoughtsRoutes']))

    _orphan = [o for s2 in _inv['sources'] for o in s2['owns']
               if not os.path.exists(os.path.join(ROOT, o))]
    chk('inventory: every owning reference file exists', not _orphan, str(_orphan))

    # A Tier B hash is only meaningful if a browser produced it: the SPA shell is byte-identical
    # for every route, including ones that do not exist, so a curl-derived hash proves nothing and
    # would go green forever. The deep harvest WILL fill these in, so the rule is not "no hash" -
    # it is "no hash without provenance saying a browser rendered the page".
    _BROWSER_METHODS = {'browser-innertext', 'browser-dom'}
    _fake = [f"{s2['url']} (hashMethod={s2.get('hashMethod')!r})"
             for s2 in _inv['sources']
             if s2['tier'] == 'B' and s2.get('contentHash')
             and s2.get('hashMethod') not in _BROWSER_METHODS]
    chk('inventory: every tier-B hash records a browser method', not _fake,
        'a tier-B hash without hashMethod in ' + str(sorted(_BROWSER_METHODS))
        + ' can only be the SPA shell: ' + str(_fake))

    # The sitemap is recorded as a stale lower bound. If it ever catches up, that note is wrong
    # and the sentinel design changes - so assert the staleness rather than assuming it holds.
    _sm = _inv['tierA']['sitemap']
    chk('inventory: sitemap is still stale (signal only, never a count)',
        _sm['componentsListed'] < _inv['contracts']['components']
        and _sm['templatesListed'] < _inv['contracts']['templates'],
        f"sitemap now lists {_sm['componentsListed']} components / {_sm['templatesListed']} "
        f"templates - if it caught up, update the note in harvest/sources.py")

    chk('inventory: the stylesheet tripwire has a build hash',
        bool(_inv['tierA'].get('stylesheet', {}).get('buildHash')))

    # Critical facts must still be the facts. A stale watch-list is worse than none: it points
    # the sentinel at a value nothing depends on any more.
    _facts = {f['fact']: f['value'] for f in _inv['criticalFacts']}
    chk('inventory: text.secondary critical fact matches tokens.json',
        _facts['text.secondary'] == t['role']['text']['secondary'])
    chk('inventory: dark selector critical fact matches tokens.json',
        _facts['dark theme selector'] in t['role']['dark']['$activation'])
    _ver = open(os.path.join(ROOT, 'skills/dga-design-system/dga-version.md'),
                encoding='utf-8').read()
    # --- ownership completeness, derived rather than trusted -------------------
    # The map was built by hand twice and was wrong both times: the first pass read only each
    # file's opening lines and missed four dependants, the second still missed /support because
    # foundations.md declares it in a per-SECTION provenance line far down the file. So derive
    # it: every route a reference file declares as its source must resolve to an inventory
    # source that lists that file as an owner.
    _DECL = re.compile(
        r'(?:\*\*Sources?:\*\*|\*\*Also:\*\*)(?P<a>[^\n]*(?:\n(?![\n#])[^\n]*){0,2})'
        r'|^`?(?P<b>/[A-Za-z0-9_./-]+)`?\s*\u00b7\s*retrieved',
        re.M)
    _ROUTE = re.compile(r'(?:https?://design\.dga\.gov\.sa)(/[A-Za-z0-9_./*-]*)|(?<![\w/])(/[A-Za-z0-9_./*-]+)')
    # Append-only records: a DGA change does not make a capture log wrong, it stays true as
    # history. dga-version.md is NOT here - a release means the pin itself must change.
    _NOT_OWNERS = ('references/capture-log.md',)
    # Declared routes deliberately absent from the inventory, each mapped to WHY. A set would
    # let a future exemption be added with no justification, which is precisely how a real
    # dependency stops being monitored - so the rationale is structural, not a comment asking
    # nicely, and an empty one fails below.
    #
    # Empty on purpose today: the route pattern is tight enough that prose which merely looks
    # like a path ("header/footer rules", "and/or") no longer reaches here.
    _UNTRACKED_OK = {
        # '/some/route': 'why nothing needs to watch this',
    }

    def _covers(src, route):
        u = src['url']
        if u == route:
            return True
        if '{' not in u:
            return False
        prefix = u.split('{', 1)[0].rstrip('/')
        return route.rstrip('/*') == prefix or route.startswith(prefix + '/')

    _decls, _unknown, _gaps = set(), set(), []
    for _d, _, _fs in os.walk(os.path.join(ROOT, 'skills')):
        for _f in _fs:
            if not _f.endswith('.md'):
                continue
            _p = os.path.join(_d, _f)
            _rel = os.path.relpath(_p, ROOT).replace('\\', '/')
            if _rel.endswith(_NOT_OWNERS):
                continue
            for _m in _DECL.finditer(open(_p, encoding='utf-8').read()):
                for _g in _ROUTE.findall(_m.group('a') or _m.group('b') or ''):
                    _r = (_g[0] or _g[1]).rstrip('.,\u00b7-')
                    if _r in ('/', '') or _r.startswith('/skills') or 'github' in _r:
                        continue
                    _decls.add((_r, _rel))

    for _r, _rel in sorted(_decls):
        _hit = [s2 for s2 in _inv['sources'] if _covers(s2, _r)]
        if not _hit:
            # A reference declaring a DGA page the inventory does not know about is exactly the
            # gap this contract exists to close - the page is cited but nothing watches it. This
            # used to be collected and dropped, which made the completeness claim untrue.
            if _r not in _UNTRACKED_OK:
                _unknown.add(f'{_r} (declared by {_rel})')
            continue
        _own = set()
        for s2 in _hit:
            _own |= set(s2['owns'])
            _slug = _r.rstrip('/*').rsplit('/', 1)[-1]
            _own |= set((s2.get('routeOwners') or {}).get(_slug, []))
        if _rel not in _own:
            _gaps.append(f'{_r} is declared by {_rel}, which is not in its owns[]')

    chk('inventory: every declared source route lists its dependant as an owner', not _gaps,
        str(_gaps))
    chk('inventory: every declared source route is tracked by a source entry', not _unknown,
        'a reference cites a DGA page nothing in the inventory watches - add it to '
        'harvest/sources.py, or to _UNTRACKED_OK with a reason: ' + str(sorted(_unknown)))
    _no_reason = sorted(r for r, why in _UNTRACKED_OK.items() if not (why or '').strip())
    chk('inventory: every untracked-route exemption carries a rationale', not _no_reason,
        'an exemption with no reason is an unmonitored dependency waiting to happen: '
        + str(_no_reason))

    # The watch list calls this critical, so it has to be checked against the file it protects.
    # A silent change from 4 to 3 would mis-state a go/no-go gate.
    _ac = open(os.path.join(ROOT, 'skills/dga-launch-gate/references/assessment-criteria.md'),
               encoding='utf-8').read()
    _mand = _ac.split('### Mandatory compliance', 1)[-1].split('### Recommended', 1)[0]
    _n_mand = len(re.findall(r'^- \[ \] \*\*', _mand, re.M))
    chk('inventory: mandatory-criteria fact matches the launch-gate reference',
        _facts['mandatory assessment criteria'] == _n_mand == 4,
        f"inventory says {_facts['mandatory assessment criteria']}, "
        f"assessment-criteria.md lists {_n_mand}, DGA publishes 4")

    chk('inventory: published version agrees with dga-version.md',
        _inv['$meta']['publishedVersion'] in _ver
        and _facts['published version'] == _inv['$meta']['publishedVersion'])

# --- installed skills must not point at files the installer does not ship -----
# `install-skills.sh` copies skills/ and agents/ into ~/.claude. Everything else in this repo -
# harvest/, evals/, COVERAGE.md, README.md - is left behind. A reference to one of those reads
# fine in the repo and is a dead end for every installed user. The ../ check below catches path
# escapes; this catches the repo-root form, which is what the dark-theme work actually used.
UNSHIPPED = ('harvest/', 'evals/', 'COVERAGE.md', 'README.md', 'AGENTS.md', 'SECURITY.md')
_OK_URL = re.compile(
    r'(?:https://github\.com/mohamedsamy911/dga-kit/blob/[A-Za-z0-9._-]+/'
    r'|https://raw\.githubusercontent\.com/mohamedsamy911/dga-kit/[A-Za-z0-9._-]+/)$')
# A shell command inside a fenced block is not a reference - a maintainer runs it from a clone.
_FENCE = re.compile(r'^```.*?^```', re.S | re.M)
_dangling = []
for _dir, _, _files in os.walk(os.path.join(ROOT, 'skills')):
    for _f in _files:
        if not _f.endswith(('.md', '.json', '.mjs', '.js', '.css')):
            continue
        _p = os.path.join(_dir, _f)
        _txt = _FENCE.sub('', open(_p, encoding='utf-8').read())
        for _m in re.finditer(r'[`\[(\s]((?:harvest|evals)/[A-Za-z0-9_./-]+|COVERAGE\.md|README\.md|AGENTS\.md|SECURITY\.md)', _txt):
            # Only a canonical GitHub URL exempts an occurrence, checked immediately before
            # THIS match. Anything looser - "preceded by a slash", "a URL somewhere in the file"
            # - waves through a dead /harvest/... path or a bare mention beside a good link.
            if _OK_URL.search(_txt[:_m.start()]):
                continue
            _dangling.append(os.path.relpath(_p, ROOT).replace('\\', '/') + ' -> ' + _m.group(1).rstrip('.'))
chk('installed skills reference nothing outside skills/', not _dangling,
    'these resolve in the repo and break once installed; use a full GitHub URL: '
    + str(sorted(set(_dangling))[:8]))

# --- provenance + $verify convention -----------------------------------------
# A convention nothing checks is a comment style. These are the rules that make
# $source and $verify load-bearing.
STATUSES = {
    'disputed', 'confirmed-defect-in-source', 'confirmed-naming-hazard', 'confirmed-hazard',
    'likely-corrected-upstream', 'unavailable-upstream', 'dga-silent',
    'gap-in-extraction-method', 'faithful-to-source',
}
def _sections():
    """(name, node) for every section carrying its own provenance.

    Walks one level into a section too: role.dark is a section in its own right - separate
    source, separate read date, separate $verify - and a top-level-only walk silently skipped
    all of it. A $verify entry nobody validates is exactly the failure mode this file exists
    to prevent.
    """
    for k, v in t.items():
        if k == '$meta' or not isinstance(v, dict):
            continue
        yield k, v
        for k2, v2 in v.items():
            if not k2.startswith('$') and isinstance(v2, dict) and '$source' in v2:
                yield f'{k}.{k2}', v2

sections = [n for n, _ in _sections()]
_node = dict(_sections())
# role.dark declares its own $source and $verify. A top-level-only walk skipped both, leaving
# six $verify entries unvalidated. Pin that the walk reaches it.
chk('provenance: the walk reaches nested role.dark', 'role.dark' in sections)
missing_src = [k for k in sections if '$source' not in _node[k]]
chk('provenance: every section carries $source', not missing_src, str(missing_src))

no_date = [k for k in sections
           if '$source' in _node[k] and not _node[k]['$source'].get('retrieved')]
chk('provenance: every $source carries a read date', not no_date, str(no_date))

bad_entries, bad_status = [], []
for k in sections:
    for e in _node[k].get('$verify', []):
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
orphan = [e['key'] for k in sections for e in _node[k].get('$verify', [])
          if e['status'] == 'disputed' and e['key'].split('.')[-1] not in xtext]
chk('$verify: every disputed value is written up in the cross-reference', not orphan, str(orphan))

print()
if failures:
    print(f'{len(failures)} FAILING — fixtures disagree with tokens.json')
    sys.exit(1)
print('All fixtures valid against tokens.json')
