#!/usr/bin/env python3
"""Generate DGA's component token NAMES as kit assets.

Every value is in tokens.json or excluded there by name (0 left to triage, 2026-10-18), but a team had to
map `--button-background-transparent-hovered` to a value by hand. This writes:

  harvest/raw/component-roles-snapshot.txt          DGA's light :root, last declaration wins
  skills/dga-design-system/assets/component-roles.json   DGA name -> declared / resolved / kitToken
  skills/dga-design-system/assets/component-roles.css    --dga-<name>: var(--dga-<kit token>) | literal

kitToken follows DGA's OWN alias chain (`var(--alpha-white-20)` -> `--colors-alpha-alpha-white-20`)
until a hop names a kit token whose value matches. It never maps by value alone: #161616 is both
text.default and base.black, and guessing between them would invent a semantic DGA did not state.
Light only: DGA's dark selector can never match (foundations.md).

  python harvest/build-component-roles.py          fetch the live stylesheet, rewrite all three
  python harvest/build-component-roles.py --check  rebuild from the snapshot (offline); exit 1 on drift
"""
import importlib.util
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'skills', 'dga-design-system', 'assets')
SNAPSHOT = os.path.join(ROOT, 'harvest', 'raw', 'component-roles-snapshot.txt')
OUT_JSON = os.path.join(ASSETS, 'component-roles.json')
OUT_CSS = os.path.join(ASSETS, 'component-roles.css')
U = 'https://github.com/mohamedsamy911/dga-kit/blob/master/harvest/build-component-roles.py'

_spec = importlib.util.spec_from_file_location('reconcile', os.path.join(ROOT, 'harvest', 'reconcile-tokens.py'))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

# DGA's component-level families. The kit already models colors/alpha (color.*), text and
# background (role.*), spacing, radius, width, shadow, gradient, container and paragraph width.
FAMILIES = ('accordion', 'border', 'button', 'buttons', 'card', 'components', 'control', 'controls',
            'featuredicons', 'form', 'icon', 'link', 'model', 'notification', 'pagination',
            'progressindicator', 'stepper', 'tab', 'table', 'tag', 'tooltip')


# DGA primitive name -> the kit name tokens.css emits for it. A hop links only if the kit name
# exists AND its value equals the role's resolved value; the name alone is not enough.
_RULES = [
    (r'--colors-primary-sa-flag-500-alpha-10', '--dga-color-alpha-sa-flag-500-alpha-10'),
    (r'--colors-alpha-alpha-(.+)', r'--dga-color-alpha-\1'),
    (r'--alpha-(.+)', r'--dga-color-alpha-\1'),
    (r'--colors-(.+-\d+)-primary', r'--dga-color-\1'),     # DGA's own name for a ramp's base step
    (r'--colors-(.+)', r'--dga-color-\1'),
    (r'--spacing-(.+)', r'--dga-space-\1'),
    (r'--(text|background|radius|shadow|width)-(.+)', r'--dga-\1-\2'),
]


def kit_css():
    """Every custom property tokens.css emits, name -> value."""
    css = io.open(os.path.join(ASSETS, 'tokens.css'), encoding='utf-8').read()
    return dict(re.findall(r'(--dga-[\w-]+)\s*:\s*([^;]+);', css))


def kit_name(dga, kit):
    for pat, rep in _RULES:
        if re.fullmatch(pat, dga):
            k = re.sub(pat, rep, dga)
            return k if k in kit else None
    return None


def light_root(css):
    light, _dark, _other = R.scope_maps(R.declarations(css))
    return light


def build(light, tok):
    kit = kit_css()
    roles = {}
    for name in sorted(light):
        fam = name[2:].split('-')[0]
        if fam not in FAMILIES:
            continue
        declared = light[name]
        resolved = R.resolve(declared, light, {}, 'light')
        token, cur = None, declared
        for _ in range(8):                      # walk DGA's own chain, one whole-value var() per hop
            m = re.fullmatch(r'var\(\s*(--[\w-]+)\s*\)', cur.strip())
            if not m:
                break
            hop = m.group(1)
            k = kit_name(hop, kit)
            if k and R.norm(kit[k]) == R.norm(resolved):
                token = k
                break
            cur = light.get(hop, '')
        roles[name] = {'declared': declared, 'resolved': resolved, 'kitToken': token}
    return roles


def render(roles, build_id):
    meta = {
        'source': 'https://design.dga.gov.sa — light :root CSS custom properties',
        'stylesheetBuild': build_id,
        'scope': 'light',
        'families': list(FAMILIES),
        'totalRoles': len(roles),
        'linkedToKitToken': sum(1 for r in roles.values() if r['kitToken']),
        'generator': U,
        '$note': ('DGA\'s component token names, generated - do not edit. Keys are DGA\'s exact names; component-roles.css emits each as --dga-<name> '
                  '(load it after tokens.css). kitToken follows DGA\'s own alias chain and is null '
                  'where no hop names a kit token, never guessed from a shared value. These are '
                  'stylesheet names DGA publishes, not component recipes.'),
    }
    j = json.dumps({'$meta': meta, 'roles': roles}, indent=2, ensure_ascii=False) + '\n'
    lines = ['/* Generated by %s from DGA stylesheet build %s - do not edit.' % (U, build_id),
             '   DGA\'s component token names, light theme. Load after tokens.css: most resolve through it. */',
             ':root {']
    for name, r in roles.items():
        val = 'var(%s)' % r['kitToken'] if r['kitToken'] else r['resolved']
        lines.append('  --dga-%s: %s;' % (name[2:], val))
    lines.append('}')
    return j, '\n'.join(lines) + '\n'


def snapshot_text(light, build_id):
    return 'build %s\n' % build_id + ''.join('%s: %s\n' % (k, light[k]) for k in sorted(light))


def read_snapshot():
    with io.open(SNAPSHOT, encoding='utf-8') as f:
        first, *rest = f.read().splitlines()
    light = dict(l.split(': ', 1) for l in rest if l)
    return light, first.split(' ', 1)[1]


def main(argv):
    tok = json.load(io.open(os.path.join(ASSETS, 'tokens.json'), encoding='utf-8'))
    if '--check' in argv:
        light, build_id = read_snapshot()
        j, c = render(build(light, tok), build_id)
        stale = [p for p, want in ((OUT_JSON, j), (OUT_CSS, c))
                 if io.open(p, encoding='utf-8').read() != want]
        if stale:
            print('component roles are STALE - run python harvest/build-component-roles.py:',
                  ', '.join(os.path.relpath(p, ROOT) for p in stale))
            return 1
        print('component roles are current (%d names)' % len(build(light, tok)))
        return 0
    css, build_id = R.get_css()
    light = light_root(css)
    for p, text in ((SNAPSHOT, snapshot_text(light, build_id)), *zip((OUT_JSON, OUT_CSS),
                                                                     render(build(light, tok), build_id))):
        io.open(p, 'w', encoding='utf-8', newline='\n').write(text)
    print('wrote %s, component-roles.json and component-roles.css' % os.path.relpath(SNAPSHOT, ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
