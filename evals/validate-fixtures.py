#!/usr/bin/env python3
"""Validates that eval fixtures match the actual harvested tokens.

Covers both suites: evals/dga-design-review/ and evals/dga-ui-adapter/.

An eval asserting a wrong value is worse than no eval — it teaches the skill a false rule.
Run after every token re-harvest:  python3 evals/validate-fixtures.py
"""
import json, os, re, subprocess, sys

# PyYAML is not in the standard library, and the openai.yaml checks below genuinely need a parser
# - regex-scraping them is what made an earlier version of that guard vacuous. A missing parser
# therefore has to FAIL loudly rather than skip: a check that quietly does not run is the exact
# failure mode this file exists to prevent. `pip install pyyaml`.
try:
    import yaml
except ImportError:                                   # noqa: BLE001 - reported as a check below
    yaml = None

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

# The dark-theme finding has to be corrected EVERYWHERE, not just where someone looked. The
# claim "DGA publishes dark values only in Figma" was true when this kit was written and is false
# now - 402 declarations sit in the public CSS. It was corrected in README, three SKILL.md files
# and token-wiring.md, and then found surviving twice more: in tokens.json's own $meta.$note, and
# in an eval case that GRADED the false claim as the right answer. Grep is not a review process;
# this is.
#
# Scoped to SENTENCES, not lines, and that is the whole difficulty. A line-scoped version of this
# check passed both real defects: the JSON note keeps its correction on the same physical line (so
# the exemption swallowed the claim beside it), and the eval case wrapped one sentence across two
# lines (so neither line held both halves). Sentences are the unit the claim is actually made in.
_DARK_WORD = re.compile(r'\bdark\b', re.I)
_FIGMA_ONLY = re.compile(
    r'figma[- ]only|only in the[^.]{0,60}figma|figma variable collection'
    r'|not in the public css', re.I)
# A sentence that NAMES the old claim in order to correct it is the opposite of the defect - but
# only when the correction is in THAT sentence. A disclaimer one sentence later does not license
# a false statement here.
_CORRECTION = re.compile(r'used to|no longer|was wrong|NOT among them|not figma-only'
                         r'|now false|is false', re.I)


def _blocks(text):
    """Lines, with WRAPPED continuations rejoined - and nothing else joined.

    An earlier version flattened every newline to a space. That merged independent markdown table
    rows into one pseudo-sentence, so a row about responsive radius sitting near a row mentioning
    dark read as a single false claim. Only an indented continuation belongs to the line above,
    and never into a table row.
    """
    out = []
    for line in text.split('\n'):
        cont = (out and line[:1].isspace() and line.strip()
                and not out[-1].lstrip().startswith('|'))
        if cont:
            out[-1] += ' ' + line.strip()
        else:
            out.append(line)
    return out


def _sentences(text):
    """Sentences, the unit a claim is actually made in. Em dashes end one; table pipes do not."""
    for b in _blocks(text):
        for s in re.split(r'(?<=[.:;!?])\s+|\s\u2014\s|\s--\s', b):
            if s.strip():
                yield s


def _stale_dark(text):
    return [s for s in _sentences(text)
            if _DARK_WORD.search(s) and _FIGMA_ONLY.search(s) and not _CORRECTION.search(s)]


_stale = []
_scan = [os.path.join(ROOT, f) for f in ('README.md', 'COVERAGE.md')]
for _base in ('skills', 'evals'):
    for _dir, _, _files in os.walk(os.path.join(ROOT, _base)):
        _scan += [os.path.join(_dir, f) for f in _files
                  if f.endswith(('.md', '.json', '.mjs', '.css'))]
for _fp in _scan:
    for _s in _stale_dark(open(_fp, encoding='utf-8').read()):
        _stale.append(os.path.relpath(_fp, ROOT).replace(os.sep, '/') + ': ' + _s.strip()[:90])
chk('dark: no shipped file still calls the dark values Figma-only', not _stale,
    str(_stale) + ' - DGA publishes them in the public CSS; unactivatable, not absent')

# Vacuous until proven otherwise, and it HAS been vacuous once: pin both real sentences verbatim,
# in both word orders, plus the corrected forms that must NOT trip it.
chk('dark: the stale-claim detector catches both sentences it was written for',
    _stale_dark('Known-incomplete areas are the PC 1.0 Figma-only values (dark theme, responsive '
                'radius/spacing, mobile kit), not the foundation pages.')
    and _stale_dark('states that DGA documents a dark variant for every semantic colour but '
                    'publishes the values \n  only in the PC 1.0 Foundations Figma variable '
                    'collections \u2014 they are not in the public CSS')
    # the real corrected sentence: the Figma-only list survives, dark is no longer in it
    and not _stale_dark('Known-incomplete areas are the PC 1.0 Figma-only values (responsive radius/spacing, mobile kit), not the foundation pages.')
    and not _stale_dark('This kit used to list dark values as Figma-only.')
    and not _stale_dark('DGA publishes 402 dark declarations in its public CSS.')
    # the COVERAGE.md table that a newline-flattening version wrongly flagged
    and not _stale_dark('| **Dark theme values** | carried under role.dark | public CSS |\n'
                        '| **Responsive radius & spacing** | wrong on two of three breakpoints '
                        '| PC 1.0 Foundations Figma variable collections |'),
    'the detector would pass a file that still carries the old claim')

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
    # Structure first. A truncated or overwritten inventory used to surface as a bare KeyError
    # forty lines further down, which reads like a broken test rather than a broken file - and
    # this file was overwritten for real during development by a tool writing a fixture to the
    # production path.
    _shape = [k for k in ('$meta', 'contracts', 'tierA', 'sources') if k not in _inv]
    chk('inventory: has its top-level structure', not _shape,
        f'missing {_shape} - regenerate with: python3 harvest/sources.py --baseline')
    _no_cat = [s2.get('url', '?') for s2 in _inv['sources'] if 'category' not in s2]
    chk('inventory: every source declares a category', not _no_cat, str(_no_cat[:5]))
    _cats = {s2['category'] for s2 in _inv['sources'] if 'category' in s2}
    chk('inventory: the route-bearing categories are present',
        {'component', 'template', 'foundation'} <= _cats,
        f'found {sorted(_cats)} - a fixture may have been written over the real inventory')

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

    # --- the sentinel's own baselines ------------------------------------------
    # A critical fact recorded as null is not a watched fact - it is a watch that silently
    # stopped. This happened for real: text.secondary is declared as var(--colors-secondary-
    # gold-600-primary), so an extractor matching only a literal hex returned None and the
    # kit's headline token quietly went unmonitored.
    _facts_css = (_inv['tierA'].get('stylesheet') or {}).get('facts') or {}
    chk('sentinel: the stylesheet facts were extracted at all', bool(_facts_css))
    _null = sorted(k for k, v in _facts_css.items() if v is None)
    chk('sentinel: no critical fact is null', not _null,
        'a null fact is a watch that stopped, not a fact: ' + str(_null))
    chk('sentinel: text.secondary resolves through its var() reference',
        _facts_css.get('text.secondary.resolved') == t['role']['text']['secondary'],
        f"css says {_facts_css.get('text.secondary.resolved')!r}, "
        f"tokens.json says {t['role']['text']['secondary']!r}")
    chk('sentinel: the dark selector is still the unmatchable one',
        _facts_css.get('darkSelectorUnmatchable') is True
        and _facts_css.get('darkSelectorFixed') is False,
        'if DGA fixed it, role.dark stops being audit-only and the guidance changes - see '
        'harvest/FRESHNESS.md')

    # The route table read out of the SPA bundle is what makes the counts curl-checkable. If it
    # ever comes back empty the contract check silently passes on nothing.
    _bundle = _inv['tierA'].get('bundle') or {}
    chk('sentinel: the route table was read from the bundle', bool(_bundle.get('counts')))
    for _g in ('components', 'templates', 'foundations', 'thoughts'):
        chk(f'sentinel: live {_g} count matches the contract',
            _bundle.get('counts', {}).get(_g) == _inv['contracts'][_g],
            f"bundle {_bundle.get('counts', {}).get(_g)} vs contract {_inv['contracts'][_g]}")
    chk('sentinel: the release list matches the published version',
        _inv['$meta']['publishedVersion'] in (_bundle.get('routes', {}).get('releases') or []),
        str(_bundle.get('routes', {}).get('releases')))

    # Version ordering is a string compare in every language that has ever got it wrong. Pin it
    # here rather than discovering it from a FRESHNESS.md that confidently names 1.0.9 as latest.
    sys.path.insert(0, os.path.join(ROOT, 'harvest'))
    try:
        import sources as _srcmod
        _vk = _srcmod.version_key
        chk('sentinel: 1.0.10 sorts above 1.0.9, not below', _vk('1.0.10') > _vk('1.0.9'))
        chk('sentinel: max() over releases is numeric',
            max(['1.0.9', '1.0.10', '1.0.2'], key=_vk) == '1.0.10')
        chk('sentinel: a non-numeric segment does not raise', _vk('1.1.0-beta') == (1, 1, 0))
        chk('sentinel: the stored release list is in numeric order',
            (_bundle.get('routes', {}).get('releases') or [])
            == sorted(_bundle.get('routes', {}).get('releases') or [], key=_vk))
    finally:
        sys.path.pop(0)

    # --- the workflows ---------------------------------------------------------
    # Plain string checks, not a YAML parse: the eval suite is pure stdlib and adding a pyyaml
    # dependency to assert four facts about two files is a bad trade.
    _wf_dir = os.path.join(ROOT, '.github', 'workflows')
    _fresh_wf = os.path.join(_wf_dir, 'dga-freshness.yml')
    _ci_wf = os.path.join(_wf_dir, 'ci.yml')
    chk('workflow: the freshness sentinel is wired up', os.path.exists(_fresh_wf))
    chk('workflow: CI runs the offline checks', os.path.exists(_ci_wf))

    if os.path.exists(_fresh_wf):
        _w = open(_fresh_wf, encoding='utf-8').read()
        chk('workflow: the sentinel actually runs --check',
            'harvest/sources.py --check' in _w)
        # The whole design rests on the automation reporting rather than deciding. A workflow
        # with contents:write could commit an accepted baseline, which would silently close the
        # review gate that everything else in this repo defers to.
        chk('workflow: the sentinel cannot write to the repo',
            'contents: read' in _w and 'contents: write' not in _w,
            'contents:write would let it accept its own findings')
        chk('workflow: the sentinel can open the review issue', 'issues: write' in _w)
        # It must not EXECUTE --baseline. Mentioning it in a comment, or printing it into the
        # issue body as the instruction a human should follow, is the whole point - so look for
        # an actual invocation rather than the string.
        _runs_baseline = [l.strip() for l in _w.splitlines()
                          if 'sources.py --baseline' in l
                          and not l.strip().startswith('#')
                          and 'echo' not in l]
        chk('workflow: the sentinel never executes --baseline', not _runs_baseline,
            'accepting a baseline is a human step, by design: ' + str(_runs_baseline))
        # exit 1 is "review pending", a RESULT. Only >1 is a broken sentinel. Conflating them
        # either turns every real DGA change into a red build, or hides a broken check.
        chk('workflow: exit 1 is treated as a finding, not a failure',
            '-gt 1' in _w and "exit_code == '1'" in _w)
        chk('workflow: the report is uploaded as an artifact',
            'upload-artifact' in _w and 'harvest/FRESHNESS.md' in _w)
        chk('workflow: it reuses one rolling issue instead of opening one a week',
            'gh issue comment' in _w and 'gh issue create' in _w)
        # An open-only lifecycle leaves the issue standing after a maintainer accepts the
        # baseline, and the next unrelated finding gets appended to an issue whose body
        # describes something already resolved - history that reads as still open.
        chk('workflow: a clean run closes the rolling issue', 'gh issue close' in _w)
        chk('workflow: the close arm is gated on a clean run',
            "exit_code == '0'" in _w,
            'closing must be conditioned on exit 0, not run unconditionally')
        chk('workflow: both arms of the lifecycle are present',
            _w.count("steps.sentinel.outputs.exit_code == '1'") >= 1
            and _w.count("steps.sentinel.outputs.exit_code == '0'") >= 1)
        chk('workflow: the close only targets its own labelled issue',
            _w.split('gh issue close')[0].rsplit('gh issue list', 1)[-1].count('dga-freshness') >= 1,
            'closing an issue this workflow did not open would be someone else\'s ticket')

    if os.path.exists(_ci_wf):
        _c = open(_ci_wf, encoding='utf-8').read()
        for _cmd in ('evals/validate-fixtures.py', 'evals/check-quote-fidelity.py --ci',
                     'check-contrast.mjs --test', 'generate-tokens.mjs', 'install-skills.sh'):
            chk(f'workflow: CI runs {_cmd}', _cmd in _c)
        chk('workflow: CI does not reach the network',
            'sources.py --check' not in _c and 'sources.py --baseline' not in _c,
            'the offline suite must stay runnable without design.dga.gov.sa')

    # --- tier B: the deep harvest ----------------------------------------------
    sys.path.insert(0, os.path.join(ROOT, 'harvest'))
    try:
        import deep as _deep
        # The extraction contract has three traps that were each hit for real. If the snippet
        # ever loses one, captures silently become the nav drawer, or Arabic, or the SPA shell.
        chk('deep: extraction clicks an in-page link rather than deep-linking',
            ".click()" in _deep.EXTRACT_JS and 'a[href=' in _deep.EXTRACT_JS)
        chk('deep: extraction walks up from the h1 to the CONTENT main',
            "querySelector('h1')" in _deep.EXTRACT_JS and "tagName !== 'MAIN'" in _deep.EXTRACT_JS)
        chk('deep: extraction does not trust querySelector(main)',
            "querySelector('main')" not in _deep.EXTRACT_JS,
            'the first <main> is the navigation drawer')
        # Footer and contact chrome appear on all ~91 pages. Leaving them in means one footer
        # edit churns every hash at once and buries the real change.
        _sample = 'Body text.\n\nContact Us\nConnect With Us\n\nDS-DGA@dga.gov.sa\nSitemap'
        chk('deep: normalisation strips the site chrome',
            _deep.normalise(_sample) == 'Body text.',
            repr(_deep.normalise(_sample)))
        chk('deep: identical text hashes identically',
            _deep.digest('a\n\nb') == _deep.digest('a\n\nb'))
        chk('deep: whitespace-only differences do not churn the hash',
            _deep.digest('a  b') == _deep.digest('a b'))

        # THE REVIEW GATE, tested by behaviour rather than by reading the source. Reporting must
        # write nothing: a run that stored the new snapshot while reporting the change would
        # compare against its own output next time, say "unchanged", and destroy a diff nobody
        # had read - the automation accepting its own finding.
        import tempfile as _tf
        _real_snaps, _real_inv = _deep.SNAPS, _deep.INV
        try:
            _tmp = _tf.mkdtemp()
            _deep.SNAPS = os.path.join(_tmp, 'snaps')
            _deep.INV = os.path.join(_tmp, 'inv.json')
            _cap = {'/x/page': 'Hello.\n\nContact Us\nConnect With Us\nSitemap'}
            _fake_inv = {'sources': []}

            _res, _pend, _blk = _deep.process(_cap, _fake_inv)    # default = report only
            chk('deep: reporting writes no snapshot',
                not os.path.isdir(_deep.SNAPS) or not os.listdir(_deep.SNAPS))
            chk('deep: reporting writes no inventory', not os.path.exists(_deep.INV))
            chk('deep: a page with no baseline is NEW, and NEW is pending',
                _res[0]['status'] == 'NEW' and len(_pend) == 1,
                'accepting a first harvest at exit 0 would let it through unread')

            _deep.process(_cap, _fake_inv, accept=True)
            chk('deep: --accept is what writes the snapshot',
                os.path.isdir(_deep.SNAPS) and len(os.listdir(_deep.SNAPS)) == 1)

            _res2, _pend2, _ = _deep.process(_cap, _fake_inv)
            chk('deep: an accepted page then reports unchanged',
                _res2[0]['status'] == 'unchanged' and not _pend2)

            # And the property the bug actually broke: report twice, diff survives both times.
            _cap2 = {'/x/page': 'Hello there.\n\nContact Us\nConnect With Us\nSitemap'}
            _a, _, _ = _deep.process(_cap2, _fake_inv)
            _b, _, _ = _deep.process(_cap2, _fake_inv)
            chk('deep: a change stays reproducible across repeated reports',
                _a[0]['status'] == 'CHANGED' and _b[0]['status'] == 'CHANGED'
                and _a[0]['diff'] == _b[0]['diff'],
                'the second run must not compare against the first run own output')
            # A harvest with holes is a FAILED harvest, not a clean one. A browser that died
            # on forty routes would otherwise report the pages it managed as the whole run.
            _r3, _p3, _b3 = _deep.process({'/x/page': None}, _fake_inv)
            chk('deep: a capture the driver could not take is EMPTY, and blocks',
                _r3[0]['status'] == 'EMPTY' and len(_b3) == 1)

            _r4, _p4, _b4 = _deep.process({}, _fake_inv, expected=['/x/page', '/x/other'])
            chk('deep: a route the driver never reported is MISSING, not absent',
                sorted(r['status'] for r in _r4) == ['MISSING', 'MISSING'] and len(_b4) == 2,
                'silently omitting a route is how a partial harvest looks clean')

            # And acceptance must be refused outright, not applied to the pages that did return.
            _snapshot_before = sorted(os.listdir(_deep.SNAPS)) if os.path.isdir(_deep.SNAPS) else []
            _deep.process({'/x/page': 'text', '/x/gone': None}, _fake_inv, accept=True)
            _snapshot_after = sorted(os.listdir(_deep.SNAPS)) if os.path.isdir(_deep.SNAPS) else []
            chk('deep: --accept writes NOTHING while any capture is missing',
                _snapshot_before == _snapshot_after,
                'accepting the pages that did return records a partial run as the baseline, and '
                'the missing ones then look unchanged forever')
        finally:
            _deep.SNAPS, _deep.INV = _real_snaps, _real_inv

        # The driver cannot be run here, so pin the property that makes it safe: it seeds every
        # requested route, so a failure surfaces as an empty capture instead of disappearing.
        _src = open(os.path.join(ROOT, 'harvest', 'deep.py'), encoding='utf-8').read()
        chk('deep: the playwright driver seeds every requested route',
            'out = {r: None for r in routes}' in _src,
            'a driver that only records successes reports a partial harvest as complete')
    finally:
        sys.path.pop(0)

    # Snapshots are machine-owned and must not leak into the human-curated evidence, or the
    # quote-fidelity corpus fills with unfenced page dumps nobody vetted.
    _snap = os.path.join(ROOT, 'harvest', 'snapshots')
    if os.path.isdir(_snap):
        chk('deep: snapshots are separate from the curated captures',
            not any(f.endswith('.md') for f in os.listdir(_snap)),
            'harvest/raw/ is curated evidence with <!-- dga --> fences; snapshots are not')

    # --- plugin manifests: resist plausible "fixes" ------------------------------
    # An external review recommended three changes here that would each BREAK loading. They are
    # plausible if you assume paths resolve from the manifest file. They do not: they resolve
    # from the PLUGIN ROOT, the directory containing .claude-plugin/ or .codex-plugin/.
    #
    # SCOPE, stated so these are not read as more than they are: the checks in THIS block are
    # STRUCTURAL. They prove the manifests keep the shape a known-good dual-target plugin uses;
    # they do not by themselves prove Claude Code loads the plugin.
    #
    # The Codex half is no longer merely structural, and this comment used to say it was: Codex
    # publishes its contract locally in the plugin-creator system skill shipped with its CLI, and
    # the `codex:` checks further down run against it. This repo's manifest passes Codex's own
    # scripts/validate_plugin.py.
    #
    # Evidence, re-fetched 2026-08-28 from tag v4.9.0 (the current release; this comment
    # previously cited 4.8.4, the locally installed copy, which had fallen a minor behind).
    # ponytail is a published, working, dual-target plugin. Its
    # .claude-plugin/marketplace.json uses "source": "./"; its .claude-plugin/plugin.json
    # declares NO skills or agents key; its .codex-plugin/plugin.json declares "skills":
    # "./skills/" while its skills live at the repo root, not inside .codex-plugin/. No plugin
    # installed on this machine - Anthropic's own included - declares skills/agents/commands in
    # plugin.json. Discovery is by convention from the plugin root.
    _mk = json.load(open(os.path.join(ROOT, '.claude-plugin/marketplace.json'), encoding='utf-8'))
    chk('manifest: marketplace source stays "./" (the plugin root, not .claude-plugin/)',
        _mk['plugins'][0]['source'] == './',
        'pointing this at .claude-plugin/ loses skills/ and agents/, which are a level up')

    _cp = json.load(open(os.path.join(ROOT, '.claude-plugin/plugin.json'), encoding='utf-8'))
    chk('manifest: claude plugin.json declares no skills/agents mapping',
        not ({'skills', 'agents', 'commands'} & set(_cp)),
        'these are auto-discovered from the plugin root; no installed plugin declares them')

    _xp = json.load(open(os.path.join(ROOT, '.codex-plugin/plugin.json'), encoding='utf-8'))
    chk('manifest: codex skills path is root-relative, not manifest-relative',
        _xp.get('skills') == './skills/',
        '"../skills/" would escape the repo - ponytail uses "./skills/" with skills at root')

    # Every manifest that carries a description must carry the caveat with it. The three drifted:
    # marketplace.json and the codex manifest said "Unofficial ... Not affiliated with or endorsed
    # by DGA", while plugin.json said "compliance" flat. plugin.json is the one a user reads in
    # the install prompt, so it was the worst place to drop it.
    _descs = []
    for _mf, _label in ((_cp, '.claude-plugin/plugin.json'),
                        (_xp, '.codex-plugin/plugin.json'),
                        (_mk, '.claude-plugin/marketplace.json')):
        _descs += [(_label, _mf['description'])] if 'description' in _mf else []
        _descs += [(_label, _p['description']) for _p in _mf.get('plugins', [])
                   if 'description' in _p]
    _uncaveated = [_l for _l, _d in _descs if 'unofficial' not in _d.lower()]
    chk('manifest: every description says unofficial', not _uncaveated, str(_uncaveated))
    _no_disclaimer = [_l for _l, _d in _descs
                      if 'not a dga certification' not in _d.lower()
                      and 'not affiliated' not in _d.lower()]
    chk('manifest: every description disclaims endorsement', not _no_disclaimer,
        str(_no_disclaimer))

    # --- the Codex install path, established 2026-08-28 -----------------------
    # `codex plugin add` installs from a MARKETPLACE, never from a bare plugin manifest, so
    # .codex-plugin/plugin.json alone was not installable. Codex documents this in the
    # plugin-creator system skill that ships with its CLI
    # (~/.codex/skills/.system/plugin-creator/references/plugin-json-spec.md, "Repo/team plugin:
    # <repo-root>/.agents/plugins/marketplace.json"), and ponytail - installed and working as a
    # Codex git marketplace - ships exactly this file. The repo's manifest passes Codex's own
    # scripts/validate_plugin.py.
    _cx = json.load(open(os.path.join(ROOT, '.agents/plugins/marketplace.json'), encoding='utf-8'))
    chk('codex: the marketplace catalogue exists and names this plugin',
        _cx['name'] == 'dga-kit' and _cx['plugins'][0]['name'] == _xp['name'],
        'codex plugin add dga-kit@dga-kit resolves <plugin>@<marketplace>')
    _src = _cx['plugins'][0]['source']
    chk('codex: the marketplace source is a url pointing at this repository',
        _src['source'] == 'url' and _src['url'].endswith('mohamedsamy911/dga-kit.git'), str(_src))
    # A ref that is not the real default branch fetches nothing. ponytail uses "main"; this repo
    # is "master", and copying ponytail's file verbatim would have shipped a dead marketplace.
    _head = open(os.path.join(ROOT, '.git', 'HEAD'), encoding='utf-8').read().strip()
    chk('codex: the marketplace ref matches this repository default branch',
        _src.get('ref') == 'master' and _head.endswith('/master'),
        f"marketplace ref {_src.get('ref')!r} vs HEAD {_head!r}")
    # Both policy values are validated against their enumerations. An earlier version checked
    # `installation` and merely asserted `authentication` was PRESENT, so setting it to "INVALID"
    # passed - the check named a field it never validated.
    _pol = _cx['plugins'][0].get('policy', {})
    _pol_bad = []
    if _pol.get('installation') not in ('NOT_AVAILABLE', 'AVAILABLE', 'INSTALLED_BY_DEFAULT'):
        _pol_bad.append(f"installation={_pol.get('installation')!r}")
    if _pol.get('authentication') not in ('ON_INSTALL', 'ON_USE'):
        _pol_bad.append(f"authentication={_pol.get('authentication')!r}")
    if not _cx['plugins'][0].get('category'):
        _pol_bad.append('category missing')
    chk('codex: policy values are inside their documented enumerations', not _pol_bad,
        str(_pol_bad))
    # Every field Codex's validate_plugin.py requires. Pinned so a manifest edit cannot quietly
    # drop one and break installation for every Codex user.
    _req_iface = ('displayName', 'shortDescription', 'longDescription', 'developerName',
                  'category', 'capabilities')
    _missing_iface = [k for k in _req_iface if not _xp.get('interface', {}).get(k)]
    chk('codex: the manifest carries every interface field the validator requires',
        not _missing_iface and (_xp['interface'].get('defaultPrompt')
                                or _xp['interface'].get('default_prompt')),
        str(_missing_iface) + ' (validate_plugin.py rejects a manifest missing any of these)')
    chk('codex: the manifest declares no agents key',
        'agents' not in _xp,
        "Codex's plugin contract has no agents field and validate_plugin.py rejects unknown keys")
    # The docs must not re-assert the claim this evidence overturned, nor promise the agents.
    _install_md = open(os.path.join(ROOT, 'INSTALL.md'), encoding='utf-8').read()
    chk('codex: INSTALL.md no longer claims there is no verified Codex path',
        'no verified Codex install path' not in _install_md)
    chk('codex: INSTALL.md still says the agents are not installed by Codex',
        'no top-level `agents` field' in ' '.join(_install_md.split()),
        'Codex installs the skills only - promising the agents would be a false claim')

    # --- per-skill Codex UI metadata -----------------------------------------
    # `<skill>/agents/openai.yaml` is read by Codex's own validator at
    # `skill_root / "agents" / "openai.yaml"` (validate_plugin.py:464). It is UI metadata and
    # invocation policy - NOT an agent definition, and NOT the repo-root agents/ directory. This
    # kit's docs conflated those two, so both halves are pinned: the files must exist and be
    # valid, and INSTALL.md must keep the distinction.
    chk('codex: a YAML parser is available to validate openai.yaml',
        yaml is not None,
        'pip install pyyaml - without it the openai.yaml checks cannot run, and a check that '
        'does not run must not report success')
    _sk_dir = os.path.join(ROOT, 'skills')
    _skills = sorted(d for d in os.listdir(_sk_dir) if os.path.isdir(os.path.join(_sk_dir, d)))
    _missing_yaml, _bad_yaml = [], []
    for _sk in _skills:
        _y = os.path.join(_sk_dir, _sk, 'agents', 'openai.yaml')
        if not os.path.isfile(_y):
            _missing_yaml.append(_sk)
            continue
        # PARSED, not regex-matched. The first version of this check scraped values with
        # regexes, so a file could satisfy every pattern and still be invalid YAML - appending a
        # bare ':' to an otherwise-good file passed this check while PyYAML rejected the file
        # outright. Codex reads these with a YAML parser, so this must too.
        if yaml is None:
            break
        try:
            _doc = yaml.safe_load(open(_y, encoding='utf-8'))
        except yaml.YAMLError as _exc:
            _bad_yaml.append(f'{_sk}: not valid YAML - {str(_exc).splitlines()[0]}')
            continue
        if not isinstance(_doc, dict):
            _bad_yaml.append(f'{_sk}: openai.yaml must be a mapping, got {type(_doc).__name__}')
            continue
        _iface = _doc.get('interface')
        if not isinstance(_iface, dict):
            _bad_yaml.append(f'{_sk}: missing an `interface` mapping')
            continue
        _short, _prompt = _iface.get('short_description'), _iface.get('default_prompt')
        # short_description is capped at 25-64 chars by openai_yaml.md; default_prompt must name
        # the skill as $skill-name or the starter prompt invokes nothing.
        if not isinstance(_short, str) or not (25 <= len(_short) <= 64):
            _bad_yaml.append(f'{_sk}: short_description '
                             f'{len(_short) if isinstance(_short, str) else "missing"} chars, '
                             f'must be 25-64')
        if not isinstance(_iface.get('display_name'), str) or not _iface['display_name'].strip():
            _bad_yaml.append(f'{_sk}: display_name must be a non-empty string')
        if not isinstance(_prompt, str) or ('$' + _sk) not in _prompt:
            _bad_yaml.append(f'{_sk}: default_prompt must mention ${_sk}')
        # EXPLICIT, not defaulted. Every one of these files says the value is "pinned rather
        # than inherited", so accepting its absence made the guard contradict the thing it
        # guards - deleting the whole policy block passed.
        _pol2 = _doc.get('policy')
        if not isinstance(_pol2, dict) or 'allow_implicit_invocation' not in _pol2:
            _bad_yaml.append(f'{_sk}: policy.allow_implicit_invocation must be stated, not '
                             f'left to the default the comment says it is pinning')
        elif not isinstance(_pol2['allow_implicit_invocation'], bool):
            _bad_yaml.append(f'{_sk}: policy.allow_implicit_invocation must be a boolean')
        # Unknown keys. Codex's own validator rejects them, so a file could pass here and fail
        # there - this check claimed a parity it did not have. Sets mirror validate_plugin.py.
        _ROOT_OK = {'interface', 'policy', 'dependencies'}
        _IFACE_OK = {'display_name', 'short_description', 'icon_small', 'icon_large',
                     'brand_color', 'default_prompt'}
        for _k in sorted(set(_doc) - _ROOT_OK):
            _bad_yaml.append(f'{_sk}: unknown top-level key {_k!r} - Codex rejects it')
        for _k in sorted(set(_iface) - _IFACE_OK):
            _bad_yaml.append(f'{_sk}: unknown interface key {_k!r} - Codex rejects it')
        # brand_color must be #RRGGBB, as Codex's HEX_COLOR_RE requires.
        _bc = _iface.get('brand_color')
        if _bc is not None and not _re.fullmatch(r'#[0-9A-Fa-f]{6}', str(_bc)):
            _bad_yaml.append(f'{_sk}: brand_color {_bc!r} must be #RRGGBB')
        # Naming an icon path that does not exist is a broken reference in the Codex UI.
        for _k in ('icon_small', 'icon_large'):
            _icon = _iface.get(_k)
            if _icon and not os.path.isfile(os.path.join(_sk_dir, _sk, str(_icon).lstrip('./'))):
                _bad_yaml.append(f'{_sk}: {_k} {_icon} does not exist')
    chk('codex: every skill ships agents/openai.yaml', not _missing_yaml, str(_missing_yaml))
    chk('codex: every openai.yaml meets the documented constraints', not _bad_yaml,
        str(_bad_yaml))
    chk('codex: openai.yaml is present for all 11 skills', len(_skills) == 11, str(len(_skills)))

    # The distinction the docs got wrong: skill-level agents/openai.yaml (metadata, read) vs a
    # repo-root agents/ directory (agent definitions, NOT installed by Codex).
    # Whitespace-collapsed: these phrases wrap across lines in the rendered paragraph, and
    # matching raw text made the check fail on re-wrapping rather than on meaning.
    _inst = open(os.path.join(ROOT, 'INSTALL.md'), encoding='utf-8').read()
    _inst_flat = ' '.join(_inst.split())
    chk('codex: INSTALL.md keeps the two meanings of agents/ apart',
        'agents/openai.yaml' in _inst_flat and 'no top-level `agents` field' in _inst_flat,
        'the page must not imply Codex has no agents/ concept - it has one, for skill metadata')

    # Whatever the manifests claim must actually be there.
    chk('manifest: the skills directory the codex manifest names exists',
        os.path.isdir(os.path.join(ROOT, _xp['skills'].strip('./') or 'skills')))
    for _m, _label in ((_cp, 'claude'), (_xp, 'codex')):
        chk(f'manifest: {_label} version matches the other', _m['version'] == _cp['version'],
            f"claude {_cp['version']} vs codex {_xp['version']}")

    # --- README claims ----------------------------------------------------------
    # The front page is the most-read and least-tested file in the repo. It carried "dark theme:
    # not public" for a day after the dark values were found in DGA's own CSS. Pin the numbers.
    _rm = open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
    chk('readme: does not still call the dark theme Figma-only',
        'Figma-only values (dark theme' not in _rm and 'dark theme, responsive' not in _rm,
        'DGA publishes 402 dark declarations - that claim was wrong')
    chk('readme: the dark declaration count matches the capture',
        f'**{len(json.load(open(os.path.join(ROOT, "harvest/raw/2026-08-27-dark-theme-roles.json"), encoding="utf-8")))} dark declarations**' in _rm)
    # Count every mention, not "is the substring present": the README says "11 skills" twice, so
    # a single stale one hides behind the other.
    _n_sk = len([d for d in os.listdir(os.path.join(ROOT, 'skills')) if d.startswith('dga-')])
    _n_ag = len([f for f in os.listdir(os.path.join(ROOT, 'agents')) if f.endswith('.md')])
    _sk_claims = set(re.findall(r'(\d+) skills', _rm))
    _ag_claims = set(re.findall(r'(\d+) agents', _rm))
    chk('readme: every skill count claimed matches what ships',
        _sk_claims == {str(_n_sk)}, f'README says {sorted(_sk_claims)}, {_n_sk} ship')
    chk('readme: every agent count claimed matches what ships',
        _ag_claims == {str(_n_ag)}, f'README says {sorted(_ag_claims)}, {_n_ag} ship')
    chk('readme: the eval case count is right',
        f'{sum(len(os.listdir(os.path.join(ROOT, "evals", s2, "cases"))) for s2 in ("dga-design-review", "dga-ui-adapter"))} eval cases' in _rm)
    chk('readme: every path named in the Layout block exists',
        all(os.path.exists(os.path.join(ROOT, m)) for m in
            re.findall(r'^\s{2,}(harvest/[A-Za-z0-9_./-]+|evals/[A-Za-z0-9_.-]+)\s', _rm, re.M)))

    chk('automation: the scenario suite exists',
        os.path.exists(os.path.join(ROOT, 'evals', 'test-automation.py')),
        'without it a monitor that silently stopped working looks like a quiet week')

    _fresh = os.path.join(ROOT, 'harvest/FRESHNESS.md')
    chk('sentinel: harvest/FRESHNESS.md exists', os.path.exists(_fresh),
        'run: python3 harvest/sources.py --check')

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
UNSHIPPED = ('harvest/', 'evals/', 'COVERAGE.md', 'README.md', 'AGENTS.md', 'SECURITY.md',
             'CHANGELOG.md')
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
        for _m in re.finditer(r'[`\[(\s]((?:harvest|evals)/[A-Za-z0-9_./-]+|COVERAGE\.md|README\.md|AGENTS\.md|SECURITY\.md|CHANGELOG\.md)', _txt):
            # Only a canonical GitHub URL exempts an occurrence, checked immediately before
            # THIS match. Anything looser - "preceded by a slash", "a URL somewhere in the file"
            # - waves through a dead /harvest/... path or a bare mention beside a good link.
            if _OK_URL.search(_txt[:_m.start()]):
                continue
            _dangling.append(os.path.relpath(_p, ROOT).replace('\\', '/') + ' -> ' + _m.group(1).rstrip('.'))
_sh = open(os.path.join(ROOT, 'install-skills.sh'), encoding='utf-8').read()
# Comment lines are exempt: the replacement is DOCUMENTED in a comment naming `xargs -r`, and a
# whole-file substring check flagged that explanation as the defect it was explaining.
_sh_code = '\n'.join(l for l in _sh.split('\n') if not l.lstrip().startswith('#'))
# --- quote-coverage figures in the docs must be the REAL ones ----------------
# README, COVERAGE and CHANGELOG each quote "N of M blockquotes". Those went stale the moment
# anyone added a blockquote anywhere in skills/ - which is exactly what happened: three documents
# said 7 of 84 while the checker reported 7 of 87. Hand-syncing a number across three files is a
# process that fails silently, so compute the real figure and compare.
sys.path.insert(0, os.path.join(ROOT, 'evals'))
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    'qf', os.path.join(ROOT, 'evals', 'check-quote-fidelity.py'))
_qf = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_qf)          # importable by design: no module-level side effects
_qf_total = sum(1 for _d, _, _fs in os.walk(os.path.join(ROOT, 'skills'))
                for _f in _fs if _f.endswith('.md')
                for _ln, _q in _qf.blockquotes(os.path.join(_d, _f))
                if len(_q) >= _qf.MIN_LEN)
_stale_counts = []
for _rel in ('README.md', 'COVERAGE.md', 'CHANGELOG.md'):
    _txt = open(os.path.join(ROOT, _rel), encoding='utf-8').read()
    for _m in re.finditer(r'(\d+) of (\d+) blockquotes?', _txt):
        if int(_m.group(2)) != _qf_total:
            _stale_counts.append(f'{_rel}: "{_m.group(0)}" but the real total is {_qf_total}')
chk('docs: every "N of M blockquotes" matches the actual count', not _stale_counts,
    str(_stale_counts))
chk('docs: the blockquote total is non-trivial', _qf_total > 50,
    f'computed {_qf_total} - the walk is probably broken, which would make the check vacuous')

# --- the installers must ship exactly what the repo contains -----------------
# The invariant nothing checked: both installers hardcode their allowlists, so a skill added to
# skills/ is simply not installed. Proven by adding one - the ONLY failure was a hardcoded "11",
# which a maintainer fixes by typing "12", and the installer stays silently broken. That is the
# worst shape of gap: the symptom check points somewhere else, so acting on it makes the real
# defect permanent. Both installers, both directions, and against each other.
_disk_skills = sorted(d for d in os.listdir(os.path.join(ROOT, 'skills'))
                      if os.path.isdir(os.path.join(ROOT, 'skills', d)))
_disk_agents = sorted(f[:-3] for f in os.listdir(os.path.join(ROOT, 'agents'))
                      if f.endswith('.md'))
_sh_txt = open(os.path.join(ROOT, 'install-skills.sh'), encoding='utf-8').read()
_ps_txt = open(os.path.join(ROOT, 'install-skills.ps1'), encoding='utf-8').read()


def _names(txt, pattern):
    _m = _re.search(pattern, txt, _re.S)
    return sorted(set(_re.findall(r'dga-[a-z0-9-]+', _m.group(1)))) if _m else []


_sh_sk = _names(_sh_txt, r'SKILLS=\((.*?)\)')
_sh_ag = _names(_sh_txt, r'AGENTS=\((.*?)\)')
_ps_sk = _names(_ps_txt, r'\$skills \s*=\s*@\((.*?)\)'.replace(' ', ''))
_ps_ag = _names(_ps_txt, r'\$agents \s*=\s*@\((.*?)\)'.replace(' ', ''))
chk('installer: bash SKILLS list equals the skills on disk', _sh_sk == _disk_skills,
    f'missing {sorted(set(_disk_skills) - set(_sh_sk))} / extra '
    f'{sorted(set(_sh_sk) - set(_disk_skills))} - an unlisted skill is silently not installed')
chk('installer: bash AGENTS list equals the agents on disk', _sh_ag == _disk_agents,
    f'missing {sorted(set(_disk_agents) - set(_sh_ag))} / extra '
    f'{sorted(set(_sh_ag) - set(_disk_agents))}')
chk('installer: powershell skills list equals the skills on disk', _ps_sk == _disk_skills,
    f'missing {sorted(set(_disk_skills) - set(_ps_sk))} / extra '
    f'{sorted(set(_ps_sk) - set(_disk_skills))}')
chk('installer: powershell agents list equals the agents on disk', _ps_ag == _disk_agents,
    f'missing {sorted(set(_disk_agents) - set(_ps_ag))} / extra '
    f'{sorted(set(_ps_ag) - set(_disk_agents))}')
chk('installer: the two installers agree with each other',
    _sh_sk == _ps_sk and _sh_ag == _ps_ag,
    'bash and powershell would install different sets')
# Non-vacuous by construction: the lists must be non-trivial, or every comparison above is
# comparing two empty lists and passing.
chk('installer: the parsed lists are non-empty',
    len(_sh_sk) >= 5 and len(_ps_sk) >= 5 and len(_sh_ag) >= 3 and len(_ps_ag) >= 3,
    f'parsed sh={len(_sh_sk)}/{len(_sh_ag)} ps1={len(_ps_sk)}/{len(_ps_ag)} - if these are 0 the '
    f'array patterns stopped matching and the checks above became vacuous')

# --- documented contrast totals must come from the checker -------------------
# The invariant nothing checked: token-wiring.md said "exactly one DGA text token fails AA" and
# "its FAIL list is text.secondary alone", both true only of --theme light, while the default
# reports 20. Nothing compared a documented total to the tool that produces it.
_node_json = None
try:
    _proc = subprocess.run(
        ['node', os.path.join(ROOT, 'skills/dga-design-system/assets/check-contrast.mjs'),
         '--json'],
        capture_output=True, text=True, timeout=120)
    if _proc.returncode == 0:
        _node_json = json.loads(_proc.stdout)
except (OSError, ValueError, subprocess.SubprocessError):
    _node_json = None
chk('contrast: the checker can be read for its totals', _node_json is not None,
    'node is required to derive the documented contrast numbers; without it this check and the '
    'one below cannot run, and a check that cannot run must not report success')
if _node_json is not None:
    # `fails` is already the filtered list; rows carry theme/ratio/aaNormal, not a verdict
    # string. Filtering on a 'verdict' key that does not exist yielded zero - which the
    # non-trivial check below caught, which is exactly why it is there.
    _fails = [r for r in _node_json.get('fails', []) if isinstance(r, dict)]
    _light = len([r for r in _fails if r.get('theme') == 'light'])
    _dark = len([r for r in _fails if r.get('theme') == 'dark'])
    _totals = {'light': _light, 'dark': _dark, 'both': len(_fails)}
    chk('contrast: the derived totals are non-trivial', _totals['both'] > 0,
        f'{_totals} - zero failures means the JSON shape changed and both checks went vacuous')
    # Any document stating "reports N failures" must state the real N.
    # Matches "reports 20 failures", "reports **5** failing pairings", "reports **20**".
    _TOTAL_RE = _re.compile(r'reports?\s+\*{0,2}(\d+)\*{0,2}\s*'
                            r'(?:failing pairings|failures)')
    # A pattern that matches nothing makes the loop below vacuous - pin it against the real
    # sentences it is written for.
    chk('contrast: the total-matching pattern actually matches',
        bool(_TOTAL_RE.search('reports **5 failing pairings** from 1 token'))
        and bool(_TOTAL_RE.search('and reports 20 failures'))
        and bool(_TOTAL_RE.search('reports **20** failures')),
        'the documented-totals check cannot fire')
    _bad_totals = []
    for _rel in ('README.md', 'INSTALL.md', 'COVERAGE.md',
                 'skills/dga-ui-adapter/references/token-wiring.md',
                 'skills/dga-design-system/references/CONTRAST-AUDIT.md'):
        _fp = os.path.join(ROOT, _rel)
        if not os.path.isfile(_fp):
            continue
        _t = ' '.join(open(_fp, encoding='utf-8').read().split())
        for _m2 in _re.finditer(_TOTAL_RE, _t):
            if int(_m2.group(1)) not in _totals.values():
                _bad_totals.append(f'{_rel}: "{_m2.group(0)}" but real totals are {_totals}')
    chk('contrast: documented failure totals match the checker', not _bad_totals,
        str(_bad_totals))

# --- npm package facts must match their recorded evidence --------------------
# These are NOT DGA facts, and that was the defect: the version table, "175 components" and
# "48 components carry [dir=rtl]" sat under a DGA /developing citation, implying DGA published
# them. DGA publishes none of it. Two of the numbers were also simply wrong - the package ships
# 123 components, and 48 is @platformscode/core's VERSION count, conflated with a component
# count. Both are corrected against harvest/raw/2026-08-28-npm-packages.md, and pinned here so a
# future edit cannot drift the doc away from its evidence offline.
_pkg_doc = open(os.path.join(ROOT, 'skills/dga-react/references/official-packages.md'),
                encoding='utf-8').read()
# WHOLE-KIT scan. The first version of this guard read only official-packages.md - the file I
# happened to edit - and passed while COVERAGE.md and dga-react/SKILL.md both still published
# "175 components". A guard scoped to the file you corrected certifies your edit, not the repo.
_kit_docs = {}
for _base in ('skills', 'agents'):
    for _d, _, _fs in os.walk(os.path.join(ROOT, _base)):
        for _f in _fs:
            if _f.endswith('.md'):
                _p2 = os.path.join(_d, _f)
                _kit_docs[os.path.relpath(_p2, ROOT).replace(os.sep, '/')] = \
                    open(_p2, encoding='utf-8').read()
for _rel in ('README.md', 'COVERAGE.md', 'INSTALL.md', 'CHANGELOG.md'):
    _kit_docs[_rel] = open(os.path.join(ROOT, _rel), encoding='utf-8').read()
_pkg_ev = open(os.path.join(ROOT, 'harvest/raw/2026-08-28-npm-packages.md'),
               encoding='utf-8').read()
chk('npm: the package evidence capture exists', bool(_pkg_ev))
for _n, _what in (('123', 'component count'), ('19', 'RTL component count'),
                  ('0.0.52', 'core version'), ('0.1.45', 'react wrapper version')):
    chk(f'npm: doc and evidence agree on the {_what} ({_n})',
        _n in _pkg_doc and _n in _pkg_ev)
# The two wrong numbers must not come back as live claims. They survive only inside the
# correction notes that explain them, which is why this looks for the claim, not the digits.
for _bad, _why in (('175 component', 'unsupported by any source'),
                   ('175 Stencil', 'unsupported by any source'),
                   ('48 components carry', 'a version count, not a component count')):
    _live = []
    for _rel, _txt in sorted(_kit_docs.items()):
        _live += [f'{_rel}: {ln.strip()[:70]}' for ln in _txt.split(chr(10))
                  if _bad in ln and 'previously' not in ln.lower() and 'Corrected' not in ln]
    chk(f'npm: "{_bad}" is not asserted anywhere in the kit ({_why})', not _live, str(_live))
# "RTL is handled" full stop was true of neither the package nor the docs: 19 of 123 components
# carry [dir=rtl]. An installed skill said it flatly, which is the sentence someone plans an
# Arabic-first build around.
_rtl_flat = []
for _rel, _txt in sorted(_kit_docs.items()):
    _rtl_flat += [f'{_rel}: {ln.strip()[:70]}' for ln in _txt.split(chr(10))
                  if 'RTL is handled' in ln and 'partial' not in ln.lower()]
chk('npm: no doc claims RTL is handled without qualifying it', not _rtl_flat, str(_rtl_flat))
chk('npm: the doc separates DGA\'s instruction from npm-derived facts',
    'must not be conflated' in _pkg_doc and 'registry' in _pkg_doc.lower(),
    'the numbers must not sit under the /developing citation alone')

# --- AGENTS.md must list the gates CI actually runs --------------------------
# It drifted: AGENTS.md named two gates while ci.yml ran six, so a contributor doing "the gates
# before committing" was checking a third of what the pipeline checked - and finding out in CI.
# The list is documentation of a contract, which makes it exactly the kind of thing that rots
# silently unless something compares it.
_agents_md = open(os.path.join(ROOT, 'AGENTS.md'), encoding='utf-8').read()
_ci_yml = open(os.path.join(ROOT, '.github/workflows/ci.yml'), encoding='utf-8').read()
# DERIVED from ci.yml, and compared in BOTH directions. Two earlier versions were vacuous: a
# hardcoded tuple only proved that six remembered commands appeared in both files, and the
# replacement recognised only three command shapes, so `run: npm test` was invisible - and it
# dropped the reverse check entirely, so a gate deleted from CI while still documented passed.
#
# Now: every `run:` line in the workflow that looks like a check is extracted, and each must be
# documented; and every gate AGENTS.md documents must still appear in the workflow.
_RUN_RE = _re.compile(r'^\s*(?:- )?run:\s*(.+)$', _re.M)
_SKIP = ('actions/', 'pip install', 'npm init', 'npm i ', 'npm install', 'mkdir', 'cp ', 'printf',
         'export ', 'git diff', 'grep ', 'test ', 'echo ', 'npx tailwindcss', 'if ', 'foreach',
         'New-Item', 'Write-Output', '$', 'bash install-skills.sh')
_ci_gates = set()
for _m in _RUN_RE.finditer(_ci_yml):
    for _cmd in _m.group(1).split(chr(10)):
        _cmd = _cmd.strip()
        if not _cmd or _cmd.startswith('#') or _cmd.startswith('|'):
            continue
        if any(_cmd.startswith(_p) for _p in _SKIP):
            continue
        if _re.match(r'(python|node|bash|npm|npx|pwsh)\s', _cmd):
            _ci_gates.add(' '.join(_cmd.split()))
# Multi-line `run: |` blocks put the commands on following lines, so sweep those too.
for _line in _ci_yml.split(chr(10)):
    _line = _line.strip()
    if _re.match(r'(python|node|bash)\s+(evals/|skills/|-n install-skills)', _line):
        _ci_gates.add(' '.join(_line.split()))
_ci_gates = {g for g in _ci_gates if not any(g.startswith(p) for p in _SKIP)}
chk('gates: the workflow actually declares gate commands', len(_ci_gates) >= 5,
    f'derived {sorted(_ci_gates)} - a short list means the pattern stopped matching and every '
    f'assertion below it went vacuous')

def _gate_key(cmd):
    """The identifying fragment of a gate command, for comparing workflow against docs."""
    _t = _re.search(r'(evals/[A-Za-z0-9_.-]+\.py|[A-Za-z0-9_.-]+\.mjs|install-skills\.sh)', cmd)
    if not _t:
        return None
    _f = _t.group(1)
    if _f.endswith('.mjs'):
        _f = _f.rsplit('/', 1)[-1]
    return _f + (' --test' if '--test' in cmd else '')

_ci_keys = {k for k in (_gate_key(g) for g in _ci_gates) if k}
_missing_doc = sorted(k for k in _ci_keys if k not in _agents_md)
chk('gates: AGENTS.md documents every gate CI runs', not _missing_doc,
    str(_missing_doc) + ' - CI runs these; a contributor reading AGENTS.md would not know')

# The reverse: a gate removed from CI but still documented is a contributor running a check the
# pipeline no longer enforces, which is how a gate silently stops being a gate.
_doc_block = _agents_md.split('## Before you commit', 1)[-1].split('##', 1)[0]
_doc_keys = {k for k in (_gate_key(l) for l in _doc_block.split(chr(10))) if k}
_missing_ci = sorted(k for k in _doc_keys if k not in _ci_keys)
chk('gates: CI still runs every gate AGENTS.md documents', not _missing_ci,
    str(_missing_ci) + ' - documented as a gate but absent from the workflow')

_ps1 = open(os.path.join(ROOT, 'install-skills.ps1'), encoding='utf-8').read()
_ps1_code = chr(10).join(l for l in _ps1.split(chr(10)) if not l.lstrip().startswith('#'))
# PowerShell's $HOME is ReadOnly+AllScope: a test harness cannot redirect it by assignment, and
# $env:USERPROFILE does not feed it. So while the installer derived its paths from $HOME directly,
# there was NO way to exercise it without writing into the real profile - which is why it had
# never been run by CI at all. -ClaudeHome makes the destination an input. Both halves are pinned:
# the parameter must exist, and no path may be built from $HOME behind its back.
chk('installer: install-skills.ps1 takes -ClaudeHome', '$ClaudeHome = $HOME' in _ps1_code,
    'without it the script cannot be tested anywhere but the real profile')
_home_joins = [l.strip() for l in _ps1_code.split(chr(10))
               if 'Join-Path $HOME' in l]
chk('installer: no path is built from $HOME behind the parameter', not _home_joins,
    str(_home_joins) + ' - these ignore -ClaudeHome, so a test would write to the real profile')

chk('installer: no GNU-only xargs -r', 'xargs -r' not in _sh_code,
    'BSD xargs on macOS rejects -r, and set -euo pipefail turns that into a silent skip - on the '
    'platform install-skills.sh advertises support for')
chk('installer: the scan_dirs helper that replaced it exists',
    'scan_dirs()' in _sh and 'scan_dirs grep' in _sh)

chk('installed skills reference nothing outside skills/', not _dangling,
    'these resolve in the repo and break once installed; use a full GitHub URL: '
    + str(sorted(set(_dangling))[:8]))

# --- provenance + $verify convention -----------------------------------------
# A convention nothing checks is a comment style. These are the rules that make
# $source and $verify load-bearing.
STATUSES = {
    'disputed', 'confirmed-defect-in-source', 'confirmed-naming-hazard', 'confirmed-hazard',
    'likely-corrected-upstream', 'unavailable-upstream', 'published-but-unactivatable',
    'dga-silent',
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


# --- the token COUNT contract: what was read vs what is shipped -----------------
# DGA declares 1,052 custom properties on :root. tokens.json ships far fewer, because most of
# those are aliases and per-component role vars resolving to values already carried. The prose
# used to convert one number into the other - "1,052 design tokens", "All 1,052 DGA values are
# already extracted" - which promises a developer wiring a theme 3.5x what the file holds. That
# is the same defect class check-quote-fidelity.py catches for quotes, applied to numbers, and
# nothing caught it. Two rules: the counts in $meta must be the real leaf counts, and no prose
# may describe 1,052 as a token count.
def _leaves(o):
    n = 0
    if isinstance(o, dict):
        for k, v in o.items():
            if k.startswith('$'):
                continue
            n += _leaves(v) if isinstance(v, (dict, list)) else 1
    return n

_dark_n = _leaves(t['role']['dark'])
_all_n = _leaves(t)
chk('counts: $meta.carriedDarkValues is the real role.dark leaf count',
    t['$meta'].get('carriedDarkValues') == _dark_n,
    f"$meta says {t['$meta'].get('carriedDarkValues')}, tokens.json holds {_dark_n}")
chk('counts: $meta.carriedValues is the real non-dark leaf count',
    t['$meta'].get('carriedValues') == _all_n - _dark_n,
    f"$meta says {t['$meta'].get('carriedValues')}, tokens.json holds {_all_n - _dark_n}"
    ' - update $meta AND every doc quoting it')
chk('counts: carried is strictly fewer than what was read',
    t['$meta']['carriedValues'] < t['$meta']['totalCssVarsOnPage'])

# 1,052 may only ever be described as what was READ. Naming it a count of tokens or values, or
# writing "all 1,052", asserts coverage this file does not have.
def _unfenced(path):
    """Yield (lineno, line) for lines OUTSIDE ``` blocks.

    Documentation has to be able to quote the defect it is describing - COVERAGE.md spells out
    the exact overclaiming phrasings these guards forbid, and a whole-file scan flagged the
    explanation as the defect it was explaining. Same reasoning as _FENCE above; done as a state
    toggle rather than a regex strip so line numbers stay real.
    """
    fenced = False
    for i, line in enumerate(open(os.path.join(ROOT, path), encoding='utf-8', errors='replace'), 1):
        if line.lstrip().startswith('```'):
            fenced = not fenced
            continue
        if not fenced:
            yield i, line

_OVERCLAIM = re.compile(r'(?i)\b(?:all\s+1,?052|1,?052\s+(?:dga\s+)?(?:design\s+)?(?:tokens|values)\b)')
_docs = []
for _dp, _dn, _fn in os.walk(ROOT):
    if any(p in _dp for p in ('.git', 'node_modules', '__pycache__')):
        continue
    _docs += [os.path.join(_dp, f) for f in _fn if f.endswith(('.md', '.json'))]
_over = []
for _f in _docs:
    for _i, _line in _unfenced(os.path.relpath(_f, ROOT)):
        if _OVERCLAIM.search(_line):
            _over.append(os.path.relpath(_f, ROOT).replace(os.sep, '/') + f':{_i}')
chk('counts: no doc calls the 1,052 read a count of tokens shipped', not _over,
    str(_over) + f" - say \"{t['$meta']['carriedValues']} token values, read from 1,052 CSS"
    ' custom properties\"')

# ...and the docs that DO state the shipped count must state the current one.
_CARRIES = ['README.md', 'skills/dga-ui-adapter/SKILL.md', 'skills/dga-design-system/SKILL.md',
            'skills/dga-design-system/references/foundations.md',
            'skills/dga-tokens-sync/SKILL.md',
            '.claude-plugin/plugin.json', '.codex-plugin/plugin.json']
_stale = [f for f in _CARRIES
          if str(t['$meta']['carriedValues']) not in open(os.path.join(ROOT, f), encoding='utf-8').read()]
chk('counts: every doc that sizes the token set quotes $meta.carriedValues', not _stale,
    f"{_stale} do not mention {t['$meta']['carriedValues']}")

# --- values restated in prose must match tokens.json ---------------------------
# COVERAGE.md says rules live once, in dga-design-system/references/. Mostly true - but the
# breakpoint bands and the spacing scale are restated verbatim in review, mockup and ui-adapter
# prose, because a skill that has to send you to another file for the four numbers it uses on
# every screen is a worse skill. That duplication is deliberate; going UNGUARDED was not. Prose
# is what the model actually reads, so a drifted copy outranks the correct token.
_PROSE = [os.path.relpath(f, ROOT).replace(os.sep, '/') for f in _docs if f.endswith('.md')]

_bp = [t['breakpoint'][k]['token'] for k in ('mobile', 'tablet', 'desktop')]
_want_bands = {f'0-{_bp[0] - 1}', f'{_bp[0]}-{_bp[1] - 1}',
               f'{_bp[1]}-{_bp[2] - 1}', f'{_bp[2]}+'}
# The regex must NOT spell out the expected bands - the first version listed them as literal
# alternatives, so a drifted "600-899" simply failed to match and the check went green on a
# real regression. Match the SHAPE, compare the values.
_BAND = re.compile(r'\b(\d{1,4}-\d{3,4}|\d{3,4}\+)')
# "Scored 1-100 in ten named bands" is a score range, not a breakpoint: the word "band" alone
# is too broad. All three real restatement sites name a device tier or xl.
_BAND_LINE = re.compile(r'(?i)\b(breakpoint|mobile|tablet|desktop|xl)\b')
_bad = []
for _f in _PROSE:
    for _i, _line in _unfenced(_f):
        _norm = _line.replace('\u2013', '-').replace('\u2014', '-')
        if not _BAND_LINE.search(_norm):
            continue
        _off = [b for b in _BAND.findall(_norm) if b not in _want_bands]
        if _off:
            _bad.append(f'{_f}:{_i} {_off}')
chk('prose: every restated breakpoint band matches tokens.json', not _bad,
    f'expected {sorted(_want_bands)} from tokens.json {_bp} - drifted: {_bad}')

# The named spacing scale, restated in dga-design-review's grid pass.
_scale = t['space']['named']
_bad = []
for _f in _PROSE:
    _txt = open(os.path.join(ROOT, _f), encoding='utf-8', errors='replace').read()
    for _m in re.finditer(r'`(none|xxs|xs|sm|md|lg|xl|2xl|3xl|4xl)`\s+(\d+)\b', _txt):
        _k, _v = _m.group(1), _m.group(2)
        if _k in _scale and _scale[_k].rstrip('px') != _v:
            _bad.append(f'{_f}: `{_k}` {_v} vs tokens.json {_scale[_k]}')
chk('prose: every restated spacing step matches tokens.json', not _bad, str(_bad))

# The paragraph max-width, restated in six places across review, mockup and the references.
# Phrased as the invariant - "a line that sizes running text must say 720px" - rather than as a
# proximity regex, which matched the hex in `text-primary-paragraph #384250`.
_pw = t['container']['paragraph-max-width'].rstrip('px')
_SIZES_TEXT = re.compile(
    r'(?i)paragraphs?\b[^\n]{0,30}?(?:max-?width|width|within)'
    r'|(?:within|max-?width)[^\n]{0,30}?\bparagraphs?\b'
    r'|paragraphs?\s+\*{0,2}\d')
_bad = []
for _f in _PROSE:
    for _i, _line in _unfenced(_f):
        # A line that names the token but states no size cannot drift - only gate lines
        # that actually carry a width figure.
        if _SIZES_TEXT.search(_line) and re.search(r'\b\d{3,4}\b', _line) and _pw not in _line:
            _bad.append(f'{_f}:{_i} {_line.strip()[:70]}')
chk('prose: every line sizing running text states the paragraph max-width', not _bad,
    f'tokens.json says {_pw}px - {_bad}')

# --- the reconciliation figures ------------------------------------------------
# The gap between what DGA declares and what tokens.json carries was described for two releases
# as "aliases resolving to values already carried". The reconciler disproved that, and its
# figures are now quoted across seven documents - exactly the kind of restated number that rots.
_rec = t['$meta'].get('$reconciliation', {})
chk('reconciliation: tokens.json records it', bool(_rec),
    'regenerate the report, then record $meta.$reconciliation')

if _rec:
    chk('reconciliation: the split adds up',
        (_rec['notCarriedGenericRamp'] + _rec['notCarriedDgaNamespaced']
         + _rec['notCarriedUnknownFamily'] == _rec['notCarried']),
        f"{_rec['notCarriedGenericRamp']} + {_rec['notCarriedDgaNamespaced']} + "
        f"{_rec['notCarriedUnknownFamily']} != {_rec['notCarried']}")
    chk('reconciliation: triage is the non-generic remainder',
        _rec['toTriage'] == _rec['notCarriedDgaNamespaced'] + _rec['notCarriedUnknownFamily'],
        f"toTriage {_rec['toTriage']} != {_rec['notCarriedDgaNamespaced']} + "
        f"{_rec['notCarriedUnknownFamily']}")
    chk('reconciliation: carried + notCarried is every declaration',
        _rec['carried'] + _rec['notCarried'] == _rec['totalDeclarations'],
        f"{_rec['carried']} + {_rec['notCarried']} != {_rec['totalDeclarations']}")
    chk('reconciliation: the report exists',
        os.path.exists(os.path.join(ROOT, 'harvest/RECONCILIATION.md')),
        'regenerate it with the reconciler --write')

    # EVERY count-bearing claim is parsed and compared - not "do the right digits appear
    # somewhere in the file". That weaker rule passed while the README headline said 241,
    # because a correct 240 survived elsewhere in the same document. Each pattern captures the
    # number out of the claim itself, and every occurrence in every document must match.
    #
    # `required` is per-DOCUMENT and load-bearing. A global "was this figure claimed anywhere"
    # tally has the same hole one level up: the README headline going unmatched passed because
    # another file still matched. Each listed document must carry the claim itself.
    _CLAIMS = [
        ('notCarried',
         [r'(\d+)\s+(?:declarations\s+)?resolv\w+\s+to\s+values'],
         ['README.md', 'COVERAGE.md', 'skills/dga-design-system/SKILL.md']),
        ('notCarriedGenericRamp',
         [r'(\d+)\s+(?:are\s+)?the generic ramp',
          r'generic ramp\*{0,2}\s*\((\d+)\s+declarations\)'],
         ['README.md', 'COVERAGE.md', 'skills/dga-design-system/SKILL.md']),
        ('notCarriedDgaNamespaced',
         [r'(\d+)\s+DGA-namespaced'],
         ['README.md', 'COVERAGE.md']),
        ('toTriage',
         [r'(\d+)[^.\n]{0,14}?to triage',
          r'(\d+)\s+values? are NOT carried',
          r'(\d+)\s+values these files do not carry',
          r'(\d+)\s+values the kit does not hold',
          r'(\d+)\s+declarations are not carried'],
         ['README.md', 'COVERAGE.md', 'skills/dga-design-system/SKILL.md',
          'skills/dga-ui-adapter/SKILL.md', 'skills/dga-tokens-sync/SKILL.md',
          'skills/dga-design-system/references/foundations.md']),
    ]
    _wrong, _seen = [], {}
    for _f in _PROSE:
        _txt = re.sub(r'\s+', ' ', ''.join(l for _, l in _unfenced(_f)))
        for _key, _pats, _req in _CLAIMS:
            for _pat in _pats:
                for _m in re.finditer(_pat, _txt):
                    _seen.setdefault(_key, set()).add(_f)
                    if int(_m.group(1)) != _rec[_key]:
                        _wrong.append(f'{_f}: "{_m.group(0)[:44]}" but {_key}={_rec[_key]}')
    chk('reconciliation: every count-bearing claim matches $meta', not _wrong, str(_wrong))

    # ...and each document that is supposed to state a figure must actually still state it.
    _gone = [f'{_k} missing from {_f}' for _k, _p, _req in _CLAIMS for _f in _req
             if _f not in _seen.get(_k, set())]
    chk('reconciliation: every document still states the figures it owns', not _gone,
        str(_gone) + ' - either the claim was dropped or its wording drifted past the pattern; '
        'update _CLAIMS with the new phrasing rather than deleting the check')

    # The retracted wording must not come back - in Markdown OR in a JSON annotation. It read as
    # reassurance and it was false, and tokens.json carried it for a release after the prose
    # had been corrected.
    _RETRACTED = re.compile(
        r'(?i)(aliases and per-component role vars resolving to values already'
        r'|the rest are aliases and per-component role vars'
        r'|has NOT been reconciled)')
    _back = []
    for _f in _PROSE:
        for _i, _line in _unfenced(_f):
            if _RETRACTED.search(_line):
                _back.append(f'{_f}:{_i}')
    for _f in ('skills/dga-design-system/assets/tokens.json',
               'harvest/source-inventory.json'):
        _txt = open(os.path.join(ROOT, _f), encoding='utf-8').read()
        # $reconciliation quotes the retracted claim in order to retract it; that annotation is
        # the record and is exempt by name, nothing else is.
        _txt = re.sub(r'"\$reconciliation":\s*\{.*?\n  \}', '', _txt, flags=re.S)
        if _RETRACTED.search(_txt):
            _back.append(_f)
    chk('reconciliation: the retracted "all aliases" wording has not returned', not _back,
        str(_back) + ' - disproved by the reconciler; see $meta.$reconciliation')


print()
if failures:
    print(f'{len(failures)} FAILING — fixtures disagree with tokens.json')
    sys.exit(1)
print('All fixtures valid against tokens.json')
