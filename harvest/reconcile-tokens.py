#!/usr/bin/env python3
"""Reconciles every custom property DGA declares against the values tokens.json carries.

For two releases the kit explained the difference away as aliasing - "the rest are aliases and
per-component role vars resolving to values already carried" - and marked it unreconciled. This
settles it declaration by declaration. It disproved that claim: 516 declarations resolve to
values the kit does not hold, of which 240 are DGA-namespaced and a real coverage gap.

What it proves, and what it does not: matching is by RESOLVED VALUE, not by name. A var that
resolves to a literal already present in tokens.json carries no value the kit is missing - that
is the claim, and it is the claim this checks. It does NOT establish that each dropped var is a
semantic duplicate of the token it matches; two unrelated roles can both be 8px.

Reuses harvest/sources.py for fetching, its "is this really the site" guards, and var()
resolution - one fetch path, one set of tripwires.

Usage:
  python3 harvest/reconcile-tokens.py             # fetch live, report
  python3 harvest/reconcile-tokens.py --write     # also write harvest/RECONCILIATION.md
  python3 harvest/reconcile-tokens.py --css FILE  # reconcile a saved stylesheet, no network
"""
import importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sources.py lives beside us; load it by path so this works whatever the cwd is. Everything
# network-facing, and every refusal-to-trust-the-response guard, lives there and is reused.
_spec = importlib.util.spec_from_file_location(
    'dga_sources', os.path.join(ROOT, 'harvest', 'sources.py'))
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

DARK_SEL = '[data-theme=dark] :root'


def get_css():
    """The live stylesheet, through sources.py's locator and its guards."""
    status, shell = S.fetch(S.BASE + '/')
    if status != 200:
        raise S.NotTheSite('shell returned HTTP %s' % status)
    m = re.search(rb'href="(/assets/[^"]+\.css)"', shell)
    if not m:
        raise S.NotTheSite('no /assets/index-<hash>.css link in the shell')
    path = m.group(1).decode()
    status, css = S.fetch(S.BASE + path)
    bad = S.asset_problem('stylesheet', status, css)
    if bad:
        raise S.NotTheSite(bad)
    return css, path.split('index-')[-1].split('.css')[0]


def declarations(css):
    """Every custom-property declaration as (selector, name, value).

    Innermost-block regex: an @media wrapper contributes its inner rule's selector, which is what
    we want. Returned in source order, so a later redeclaration of the same name in the same
    selector wins - the same way the cascade resolves it.
    """
    out = []
    for m in re.finditer(rb'([^{}]*)\{([^{}]*)\}', css):
        sel = m.group(1).decode('utf-8', 'replace').strip()
        body = m.group(2).decode('utf-8', 'replace')
        if '--' not in body:
            continue
        for d in re.finditer(r'(--[^\s:;{}]+)\s*:\s*([^;}]+)', body):
            out.append((sel, d.group(1), d.group(2).strip()))
    return out


def norm(v):
    """Compare values the way CSS would, not the way a string would."""
    s = str(v).strip().lower().rstrip(';')
    s = re.sub(r'\s+', ' ', s)
    if re.fullmatch(r'#[0-9a-f]{3}', s):                        # #abc -> #aabbcc
        s = '#' + ''.join(c * 2 for c in s[1:])
    if re.fullmatch(r'#[0-9a-f]{8}', s) and s.endswith('ff'):    # #rrggbbff -> #rrggbb
        s = s[:7]
    if re.fullmatch(r'0(px|rem|em|%)?', s):                      # 0 == 0px == 0rem
        return '0'
    m = re.fullmatch(r'(\d*\.?\d+)rem', s)                       # rem -> px at DGA's 16px root
    if m:
        return '%gpx' % (float(m.group(1)) * 16)
    m = re.fullmatch(r'(\d*\.?\d+)px', s)
    if m:
        return '%gpx' % float(m.group(1))
    return s


def carried_values(tok):
    """Every literal value tokens.json ships, normalised, split light vs dark."""
    sink = (set(), set())

    def walk(node, in_dark):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.startswith('$'):
                    continue
                walk(v, in_dark or k == 'dark')
        elif isinstance(node, list):
            for v in node:
                walk(v, in_dark)
        else:
            sink[1 if in_dark else 0].add(norm(node))

    walk(tok, False)
    return sink


def semantic_families(tok):
    """The colour families DGA's published token set actually names."""
    return {k for k in tok['color'] if not k.startswith('$')}


def is_generic_palette(name, sem):
    """True for the UI-kit ramp DGA ships in CSS but does not publish as a DGA token.

    DGA's stylesheet carries the whole upstream Untitled-UI palette - blue, cyan, fuchsia,
    indigo, moss, orange, pink, purple, red, rose, teal, violet, yellow, and seven separate grey
    ramps. Those are not Platforms Code colours; the published system names eleven families.

    Prefix matching has to be exact on the family, with one exception: a step-like suffix
    (`primary-sa-flag-500-alpha-10`) is a sub-token of a semantic family and stays. Matching
    `gray-blue` as a variant of `gray` is the trap - it is a different ramp entirely, and a
    prefix rule without the step-like test classified six generic grey ramps as DGA's own.
    """
    m = re.fullmatch(r'--colors-(.+?)-(\d+|primary|white|black|alpha-\d+)', name)
    if not m:
        return False
    fam = m.group(1)
    for s in sem:
        if fam == s:
            return False
        if fam.startswith(s + '-') and re.fullmatch(r'[\d-]+|.*-\d+', fam[len(s) + 1:]):
            return False
    return True


def classify(css, table, carried, all_carried, scope):
    rows = []
    for n, v in sorted(table.items()):
        resolved = S._resolve(css, v)
        is_alias = bool(re.fullmatch(r'var\(\s*--[^,)\s]+\s*\)', v.strip()))
        nv = norm(resolved) if resolved else None
        rows.append({
            'scope': scope, 'name': n, 'declared': v, 'resolved': resolved,
            'kind': 'alias' if is_alias else ('composite' if 'var(' in v else 'literal'),
            'in_scope_set': bool(nv) and nv in carried,
            'in_any_set': bool(nv) and nv in all_carried,
        })
    return rows


def main():
    args = sys.argv[1:]
    tok = json.load(open(os.path.join(ROOT, 'skills/dga-design-system/assets/tokens.json'),
                         encoding='utf-8'))

    if '--css' in args:
        path = args[args.index('--css') + 1]
        css = open(path, 'rb').read()
        build = '(local %s)' % os.path.basename(path)
    else:
        css, build = get_css()

    decls = declarations(css)
    names = {n for _, n, _ in decls}

    light, dark, other = {}, {}, {}
    for sel, n, v in decls:
        target = dark if DARK_SEL in sel else (light if sel.endswith(':root') else other)
        target[n] = v

    lit_light, lit_dark = carried_values(tok)
    all_carried = lit_light | lit_dark

    rows = (classify(css, light, lit_light, all_carried, 'light')
            + classify(css, dark, lit_dark, all_carried, 'dark'))

    print('DGA stylesheet build %s' % build)
    print('%d distinct custom-property names, %d declarations' % (len(names), len(decls)))
    print('  :root (light)                %d' % len(light))
    print('  [data-theme=dark] :root      %d' % len(dark))
    print('  other selectors              %d' % len(other))
    print()
    print('tokens.json carries %d values + %d dark (%d / %d distinct after normalising)'
          % (tok['$meta']['carriedValues'], tok['$meta']['carriedDarkValues'],
             len(lit_light), len(lit_dark)))
    print()

    for scope in ('light', 'dark'):
        sub = [r for r in rows if r['scope'] == scope]
        covered = [r for r in sub if r['in_any_set']]
        gap = [r for r in sub if not r['in_any_set']]
        print('--- %s: %d declarations ---' % (scope, len(sub)))
        for k in ('alias', 'composite', 'literal'):
            print('  %-10s %5d' % (k, len([r for r in sub if r['kind'] == k])))
        print('  resolves to a value tokens.json already carries: %d/%d (%d%%)'
              % (len(covered), len(sub), 100 * len(covered) // max(len(sub), 1)))
        print('  NOT carried anywhere:                            %d' % len(gap))
        if gap:
            seen = {}
            for r in gap:
                key = norm(r['resolved']) if r['resolved'] else '<unresolved>'
                seen.setdefault(key, []).append(r['name'])
            print('  the values that would be lost:')
            for val, ns in sorted(seen.items(), key=lambda kv: -len(kv[1]))[:25]:
                print('    %-30s %3dx  e.g. %s' % (val[:30], len(ns), ns[0]))
            if len(seen) > 25:
                print('    ... and %d more distinct values' % (len(seen) - 25))
        print()

    gap_all = [r for r in rows if not r['in_any_set']]
    sem = semantic_families(tok)
    generic = [r for r in gap_all if is_generic_palette(r['name'], sem)]
    triage = [r for r in gap_all if not is_generic_palette(r['name'], sem)]
    print('CLAIM "the uncarried vars resolve to values already carried": %s'
          % ('HOLDS' if not gap_all
             else 'DOES NOT HOLD - %d declarations resolve to values tokens.json does not carry'
                  % len(gap_all)))
    print('  of those, generic UI-kit palette (defensible exclusion): %d' % len(generic))
    print('  genuinely missing DGA-namespaced values (triage):        %d' % len(triage))
    fam = {}
    for r in triage:
        fam.setdefault('--' + r['name'].lstrip('-').split('-')[0], []).append(r['name'])
    for f, ns in sorted(fam.items(), key=lambda kv: -len(kv[1])):
        print('    %-18s %4d   e.g. %s' % (f, len(ns), sorted(ns)[0]))

    if '--write' in args:
        write_report(build, names, light, dark, other, rows, tok)
    return 0


def write_report(build, names, light, dark, other, rows, tok):
    gap = [r for r in rows if not r['in_any_set']]
    sem = semantic_families(tok)
    generic = [r for r in gap if is_generic_palette(r['name'], sem)]
    triage = [r for r in gap if not is_generic_palette(r['name'], sem)]

    def block(scope):
        sub = [r for r in rows if r['scope'] == scope]
        return {k: len([r for r in sub if r['kind'] == k])
                for k in ('alias', 'composite', 'literal')}

    bl, bd = block('light'), block('dark')
    out = []
    add = out.append
    add('# Token reconciliation - what DGA declares vs what this kit ships\n')
    add('Generated by `harvest/reconcile-tokens.py` against DGA stylesheet build **%s**.' % build)
    add('Regenerate with `python3 harvest/reconcile-tokens.py --write`. Do not edit by hand.\n')
    add('`tokens.json` carries **%d** values plus **%d** dark, out of the custom properties'
        % (tok['$meta']['carriedValues'], tok['$meta']['carriedDarkValues']))
    add('counted below. For two releases the kit explained that difference away as aliasing.')
    add('This file is the reconciliation that disproved it, regenerated from the live')
    add('stylesheet.\n')
    add('**Matching is by resolved value, not by name.** A declaration resolving to a literal')
    add('already present in `tokens.json` carries no value the kit is missing. That is the claim')
    add('being tested. It does **not** establish that each dropped var is a semantic duplicate -')
    add('two unrelated roles can both be `8px`.\n')
    add('## What DGA declares\n')
    add('| Scope | Declarations |')
    add('|---|---|')
    add('| `:root` (light) | %d |' % len(light))
    add('| `[data-theme=dark] :root` | %d |' % len(dark))
    add('| other selectors | %d |' % len(other))
    add('| **distinct names** | **%d** |\n' % len(names))
    add('| Kind | light | dark |')
    add('|---|---|---|')
    add('| `var()` alias | %d | %d |' % (bl['alias'], bd['alias']))
    add('| composite (contains a `var()`) | %d | %d |' % (bl['composite'], bd['composite']))
    add('| literal | %d | %d |\n' % (bl['literal'], bd['literal']))
    add('## Verdict\n')
    add('**%d of %d** declarations resolve to a value `tokens.json` already carries. **%d** do'
        % (len(rows) - len(gap), len(rows), len(gap)))
    add('not, so the "all aliases" reading of the gap is **wrong** and is retracted.\n')
    add('| The %d that do not reconcile | Count |' % len(gap))
    add('|---|---|')
    add('| Generic UI-kit palette DGA ships but does not publish as a DGA token | %d |' % len(generic))
    add('| **DGA-namespaced values this kit simply does not hold** | **%d** |\n' % len(triage))
    add('The first group is a defensible exclusion — DGA\'s stylesheet carries the whole upstream')
    add('Untitled-UI ramp (blue, cyan, fuchsia, indigo, moss, orange, pink, purple, red, teal,')
    add('violet, yellow, and seven separate grey ramps) and the published system names %d families.'
        % len(sem))
    add('It was never *stated* as an exclusion, which is the actual defect. The second group is a')
    add('real coverage gap.\n')
    if triage:
        fam = {}
        for r in triage:
            fam.setdefault('--' + r['name'].lstrip('-').split('-')[0], []).append(r)
        add('### The %d to triage, by family\n' % len(triage))
        add('| Family | Count | Example | Resolves to |')
        add('|---|---|---|---|')
        for f, rs in sorted(fam.items(), key=lambda kv: -len(kv[1])):
            e = sorted(rs, key=lambda r: r['name'])[0]
            add('| `%s` | %d | `%s` | `%s` |' % (f, len(rs), e['name'], e['resolved']))
        add('')
        add('### Every one of them\n')
        add('| Scope | Custom property | Declared | Resolves to |')
        add('|---|---|---|---|')
        for r in sorted(triage, key=lambda r: (r['scope'], r['name'])):
            add('| %s | `%s` | `%s` | `%s` |'
                % (r['scope'], r['name'], r['declared'][:48], r['resolved']))
    else:
        add('Nothing outstanding: every declaration DGA publishes resolves to a value this kit')
        add('already carries.')
    p = os.path.join(ROOT, 'harvest', 'RECONCILIATION.md')
    open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\nwrote %s' % os.path.relpath(p, ROOT))


if __name__ == '__main__':
    sys.exit(main())
