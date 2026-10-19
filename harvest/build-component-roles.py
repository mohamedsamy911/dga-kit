#!/usr/bin/env python3
"""Generate DGA's component token NAMES as kit assets.

Every value is in tokens.json or excluded there by name (0 left to triage, 2026-10-18), but a team had to
map `--button-background-transparent-hovered` to a value by hand. This writes:

  harvest/raw/component-roles-snapshot.txt          DGA's light :root with the desktop @media block
                                                    only, last declaration wins
  harvest/raw/component-roles-responsive.txt        the tablet and mobile values that differ
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
RESPONSIVE = os.path.join(ROOT, 'harvest', 'raw', 'component-roles-responsive.txt')
# DGA sets its responsive component spacing in three @media :root blocks. Each block is read on its
# own: DGA's file puts min-width:768px after min-width:1025px, so its cascade gives wide screens
# the tablet value - a defect, not a design. Modes and widths are DGA's (Figma Foundations file,
# harvest/raw/2026-10-19-figma-foundations.md). The tablet query is bounded on both sides, the
# kit's fix: a mobile value equal to desktop must not inherit the tablet one.
MODES = (('desktop', 'min-width: 1025px', None),
         ('tablet', 'min-width: 768px', '(min-width: 768px) and (max-width: 1024px)'),
         ('mobile', 'max-width: 767px', '(max-width: 767px)'))
_MEDIA = re.compile(rb'@media([^{]*)\{\s*:root\s*\{[^{}]*\}\s*\}')
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


def mode_maps(css):
    """{mode: light map} with only that mode's @media block kept, the other two removed."""
    blocks = [(m.span(), m.group(1).decode('utf-8', 'replace')) for m in _MEDIA.finditer(css)]
    out = {}
    for mode, query, _ in MODES:
        if sum(query in q for _, q in blocks) != 1:
            raise SystemExit('expected exactly one @media block for %s' % query)
        cut, last = [], 0
        for (a, b), q in blocks:
            if query not in q:
                cut.append(css[last:a])
                last = b
        cut.append(css[last:])
        out[mode] = light_root(b''.join(cut))
    return out


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


def build_modes(maps, tok):
    """Desktop roles, each carrying the tablet/mobile row where that mode differs."""
    roles = build(maps['desktop'], tok)
    for mode, _, _ in MODES[1:]:
        other = build(maps[mode], tok)
        for name, r in roles.items():
            o = other.get(name)
            if o and (o['declared'], o['resolved']) != (r['declared'], r['resolved']):
                r.setdefault('responsive', {})[mode] = o
    return roles


def render(roles, build_id):
    meta = {
        'source': 'https://design.dga.gov.sa — light :root CSS custom properties',
        'stylesheetBuild': build_id,
        'scope': 'light',
        'families': list(FAMILIES),
        'totalRoles': len(roles),
        'linkedToKitToken': sum(1 for r in roles.values() if r['kitToken']),
        'responsive': {m: q for m, _, q in MODES[1:]},
        'responsiveRoles': sum(1 for r in roles.values() if r.get('responsive')),
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
    def val(r):
        return 'var(%s)' % r['kitToken'] if r['kitToken'] else r['resolved']
    for name, r in roles.items():
        lines.append('  --dga-%s: %s;' % (name[2:], val(r)))
    lines.append('}')
    for mode, _, query in MODES[1:]:
        rows = [(n, r['responsive'][mode]) for n, r in roles.items() if mode in r.get('responsive', {})]
        if rows:
            lines += ['/* %s: DGA\'s per-mode value. Desktop is the :root above. */' % mode,
                      '@media %s {' % query, '  :root {']
            lines += ['    --dga-%s: %s;' % (n[2:], val(o)) for n, o in rows]
            lines += ['  }', '}']
    return j, '\n'.join(lines) + '\n'


def snapshot_text(light, build_id):
    return 'build %s\n' % build_id + ''.join('%s: %s\n' % (k, light[k]) for k in sorted(light))


def responsive_text(maps):
    d = maps['desktop']
    return ''.join('%s %s: %s\n' % (mode, k, maps[mode][k]) for mode, _, _ in MODES[1:]
                   for k in sorted(maps[mode]) if maps[mode][k] != d.get(k))


def read_snapshot():
    with io.open(SNAPSHOT, encoding='utf-8') as f:
        first, *rest = f.read().splitlines()
    light = dict(l.split(': ', 1) for l in rest if l)
    maps = {'desktop': light, 'tablet': dict(light), 'mobile': dict(light)}
    with io.open(RESPONSIVE, encoding='utf-8') as f:
        for l in f.read().splitlines():
            mode, kv = l.split(' ', 1)
            k, v = kv.split(': ', 1)
            maps[mode][k] = v
    return maps, first.split(' ', 1)[1]


def main(argv):
    tok = json.load(io.open(os.path.join(ASSETS, 'tokens.json'), encoding='utf-8'))
    if '--check' in argv:
        maps, build_id = read_snapshot()
        roles = build_modes(maps, tok)
        j, c = render(roles, build_id)
        stale = [p for p, want in ((OUT_JSON, j), (OUT_CSS, c))
                 if io.open(p, encoding='utf-8').read() != want]
        if stale:
            print('component roles are STALE - run python harvest/build-component-roles.py:',
                  ', '.join(os.path.relpath(p, ROOT) for p in stale))
            return 1
        print('component roles are current (%d names)' % len(roles))
        return 0
    css, build_id = R.get_css()
    maps = mode_maps(css)
    for p, text in ((SNAPSHOT, snapshot_text(maps['desktop'], build_id)),
                    (RESPONSIVE, responsive_text(maps)),
                    *zip((OUT_JSON, OUT_CSS), render(build_modes(maps, tok), build_id))):
        io.open(p, 'w', encoding='utf-8', newline='\n').write(text)
    print('wrote %s, component-roles.json and component-roles.css' % os.path.relpath(SNAPSHOT, ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
