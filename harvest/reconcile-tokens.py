#!/usr/bin/env python3
"""Reconciles every custom property DGA declares against the values tokens.json carries.

For two releases the kit explained the difference away as aliasing - "the rest are aliases and
per-component role vars resolving to values already carried" - and marked it unreconciled. This
settles it declaration by declaration, cascade- and scope-correct. It disproved that claim:
declarations resolving to values the kit does not hold are counted and split three ways -
evidenced generic ramp, real DGA gap, and unknown-family-left-for-review. Live figures are
in harvest/RECONCILIATION.md; none are hardcoded here.

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
  python3 harvest/reconcile-tokens.py --test      # offline self-check, no network
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


# The upstream Untitled-UI ramp DGA ships in its CSS but does not publish as a Platforms Code
# colour. EXPLICIT, not inferred: the first version of this used a "not in the semantic set"
# rule, which swept up --colors-border-primary, --colors-text-primary and
# --colors-alpha-alpha-white-20 as though they were decorative ramp steps. They are not. An
# exclusion list has to be evidenced name by name; anything not on it and not semantic is left
# for review rather than quietly dropped, because a wrong exclusion HIDES a real gap.
GENERIC_RAMPS = frozenset("""
    blue blue-dark blue-light cyan fuchsia green green-light indigo moss orange orange-dark
    pink purple red rose rosé teal violet yellow
    gray-blue gray-cool gray-iron gray-modern gray-neutral gray-true gray-warm
""".split())


def palette_class(name, sem):
    """'generic' (evidenced exclusion), 'semantic' (a DGA family), or 'review' (unknown)."""
    m = re.fullmatch(r'--colors-(.+?)-(\d+|primary|white|black|alpha-\d+)', name)
    if not m:
        return 'semantic'
    fam = m.group(1)
    # Case-insensitive: DGA declares `--colors-Teal-*` with a capital while every other ramp is
    # lower-case, and an exact-case set left 12 Teal steps sitting in the review bucket.
    if fam.lower() in GENERIC_RAMPS:
        return 'generic'
    for s in sem:
        # exact family, or a step-like sub-token of one (primary-sa-flag-500-alpha-10)
        if fam == s or (fam.startswith(s + '-')
                        and re.fullmatch(r'[\d-]+|.*-\d+', fam[len(s) + 1:])):
            return 'semantic'
    return 'review'


def scope_maps(decls):
    """Per-scope name -> declared value, LAST declaration winning.

    The cascade, not the first regex hit. DGA redeclares 393 light names - `--colors-base-black`
    is `#000000` in one :root block and `#161616` in a later one - so resolving through the first
    match reports the wrong value and invents gaps that are not there. Dark is kept separate:
    a dark alias must resolve through dark's own redefinitions before falling back to light.
    """
    light, dark, other = {}, {}, {}
    for sel, n, v in decls:
        (dark if DARK_SEL in sel else light if sel.endswith(':root') else other)[n] = v
    return light, dark, other


def _split_var(inner):
    """`--name, fallback` -> ('--name', 'fallback'), splitting at the first TOP-LEVEL comma."""
    depth = 0
    for i, ch in enumerate(inner):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif ch == ',' and depth == 0:
            return inner[:i].strip(), inner[i + 1:].strip()
    return inner.strip(), None


def _sub_vars(value, light, dark, scope):
    """Substitute EVERY var() occurrence in a value, not just a whole-value one.

    A fullmatch-only resolver leaves composites untouched -
    `linear-gradient(90deg, var(--colors-brand-600) 0%, ...)` came back verbatim and was then
    compared against a set of plain literals, so 13 gradients and one hsla() were reported as
    confirmed-missing values when their components are all carried. Paren matching is balanced
    rather than regex, because fallbacks nest: var(--a, var(--b)).
    """
    out, i = [], 0
    while True:
        j = value.find('var(', i)
        if j < 0:
            out.append(value[i:])
            return ''.join(out)
        out.append(value[i:j])
        depth, k = 0, j + 3
        while k < len(value):
            if value[k] == '(':
                depth += 1
            elif value[k] == ')':
                depth -= 1
                if depth == 0:
                    break
            k += 1
        if k >= len(value):                       # unbalanced - leave the rest alone
            out.append(value[j:])
            return ''.join(out)
        name, fallback = _split_var(value[j + 4:k])
        repl = (dark.get(name) if scope == 'dark' else None) or light.get(name)
        if repl is None:
            # Undeclared: fall back if one is given, else leave the var() in place so the caller
            # can see it never resolved rather than silently treating it as a literal.
            repl = fallback if fallback is not None else value[j:k + 1]
        out.append(repl)
        i = k + 1


def resolve(value, light, dark, scope, depth=8):
    """Resolve a declared value within the correct scope, composites included."""
    if not value:
        return value
    for _ in range(depth):
        nxt = _sub_vars(value, light, dark, scope)
        if nxt == value:                          # stable: fully resolved, or genuinely stuck
            break
        value = nxt
    return value


def classify(table, light, dark, carried, all_carried, scope):
    rows = []
    for n, v in sorted(table.items()):
        resolved = resolve(v, light, dark, scope)
        is_alias = bool(re.fullmatch(r'var\(\s*--[^,)\s]+\s*\)', v.strip()))
        # A value still holding a var() after resolution points at something DGA never declares.
        # It is NOT evidence that the kit is missing a value, so it is counted separately rather
        # than swelling the missing total with expressions nobody has resolved.
        unresolved = bool(resolved) and 'var(' in str(resolved)
        nv = norm(resolved) if resolved and not unresolved else None
        # A composite - linear-gradient(...), hsla(...) - is not a single value, so asking
        # "is this string in the carried set" always answers no and reads as a missing value.
        # The honest question is whether its COMPONENTS are carried: all twelve DGA gradients
        # resolve entirely to brand and gray steps tokens.json already holds. What the kit
        # lacks there is the gradient DEFINITION, not any value, and the two are not the same
        # finding. `None` where there is nothing to extract - never claim cover without it.
        comps = re.findall(r'#[0-9a-fA-F]{3,8}', str(resolved or ''))
        is_composite = bool(re.search(r'[a-z-]+\(', str(resolved or ''))) and not unresolved
        comps_carried = (all(norm(c) in all_carried for c in comps)
                         if is_composite and comps else None)
        rows.append({
            'scope': scope, 'name': n, 'declared': v, 'resolved': resolved,
            'kind': 'alias' if is_alias else ('composite' if 'var(' in v else 'literal'),
            'unresolved': unresolved,
            'components': comps,
            'components_carried': comps_carried,
            'in_scope_set': bool(nv) and nv in carried,
            'in_any_set': bool(nv) and nv in all_carried,
        })
    return rows


def gap_class(row, sem):
    """Why a declaration failed to match a carried value.

    Ordered: the reasons that are NOT evidence of a missing value come first, so a gradient of
    carried colours or an expression nothing resolves can never be reported as a gap.
    """
    if row['unresolved']:
        return 'unresolved'
    if row['components_carried']:
        return 'composite-covered'
    return palette_class(row['name'], sem)


def bucket(gap, sem):
    """Split the unmatched declarations into their five categories.

    Keyed by (scope, name), NEVER by name alone. The same custom property is declared in both
    :root and the dark block, so a name-keyed dict collapses the two and the last one written
    wins for both: a genuinely missing light value inherits its dark counterpart's
    'composite-covered' and disappears from the gap. Today's stylesheet happens to have no
    light/dark pair that is unmatched on both sides, which is exactly why this had to be fixed
    on the structure rather than left to the data.
    """
    cls = {(r['scope'], r['name']): gap_class(r, sem) for r in gap}
    def of(*kinds):
        return [r for r in gap if cls[(r['scope'], r['name'])] in kinds]
    return {
        'generic': of('generic'),
        'semantic': of('semantic'),
        'review': of('review'),
        'unresolved': of('unresolved'),
        'composite': of('composite-covered'),
        'triage': of('semantic', 'review'),
    }


def closing_note(triage, unresolved):
    """What the report says when the triage bucket is empty.

    Split out so it is assertable: "Nothing outstanding" must NEVER appear while an unresolved
    expression remains. An expression nobody could resolve is an unanswered question about DGA's
    stylesheet, not a clean bill of health, and a report that calls it clean is the one failure
    this file exists to prevent.
    """
    if triage:
        return []
    if unresolved:
        return ['Nothing is in the triage bucket, but %d expression(s) below could not be'
                % len(unresolved),
                'resolved. Read those before treating this as complete.']
    return ['Nothing outstanding: every declaration DGA publishes resolves to a value this kit',
            'already carries.']


def _row(scope, name, **kw):
    r = {'scope': scope, 'name': name, 'declared': '#abcdef', 'resolved': '#abcdef',
         'kind': 'literal', 'unresolved': False, 'components': [], 'components_carried': None,
         'in_scope_set': False, 'in_any_set': False}
    r.update(kw)
    return r


def self_test():
    """Offline assertions for the three defects review found in this file. No network."""
    sem = {'brand', 'gray', 'error'}
    light = {'--a': '#111111', '--g': 'linear-gradient(90deg, var(--a) 0%, var(--a) 100%)',
             '--miss': 'var(--never-declared)', '--fb': 'var(--never-declared, #222222)'}
    dark = {'--a': '#333333'}

    # 1. Scope-correct resolution, composites included.
    assert resolve(light['--g'], light, dark, 'light') == \
        'linear-gradient(90deg, #111111 0%, #111111 100%)', 'composite did not resolve'
    assert resolve('var(--a)', light, dark, 'dark') == '#333333', 'dark did not win in dark scope'
    assert resolve('var(--a)', light, dark, 'light') == '#111111', 'light scope leaked dark'
    assert resolve(light['--fb'], light, dark, 'light') == '#222222', 'fallback ignored'
    assert 'var(' in resolve(light['--miss'], light, dark, 'light'), 'undeclared var vanished'

    # 2. Classification must key on (scope, name). A name-keyed dict lets a dark row's verdict
    #    overwrite the light row's, hiding a genuinely missing light value as 'covered'.
    collide = [
        _row('light', '--tag-x'),
        _row('dark', '--tag-x', kind='composite', components=['#1b8354'],
             components_carried=True, resolved='linear-gradient(90deg, #1b8354 0%)'),
    ]
    b = bucket(collide, sem)
    assert collide[0] in b['semantic'], 'light row lost its own classification to the dark row'
    assert collide[1] in b['composite'], 'dark row misclassified'
    assert len(b['semantic']) + len(b['composite']) == 2, 'a row was double-counted or dropped'

    # 3. Buckets partition the gap exactly - no row in two, none missing.
    everything = collide + [_row('light', '--colors-blue-500'),
                            _row('light', '--u', unresolved=True, resolved='var(--nope)')]
    b2 = bucket(everything, sem)
    counted = sum(len(b2[k]) for k in ('generic', 'semantic', 'review', 'unresolved', 'composite'))
    assert counted == len(everything), f'buckets cover {counted} of {len(everything)}'
    assert len(b2['triage']) == len(b2['semantic']) + len(b2['review']), 'triage is not the sum'

    # 4. An unresolved expression is never reported as a confirmed missing value.
    assert b2['unresolved'] and everything[3] not in b2['semantic'], \
        'unresolved expression counted as a missing DGA value'

    # 5. "Nothing outstanding" must never appear while anything is unresolved.
    assert closing_note([], []) and 'Nothing outstanding' in closing_note([], [])[0],         'a genuinely clean run should say so'
    assert not any('Nothing outstanding' in l for l in closing_note([], [_row('light', '--u')])),         'reported "Nothing outstanding" while an unresolved expression remained'
    assert closing_note([_row('light', '--t')], []) == [],         'closing note emitted while the triage table is being printed'

    print('reconcile self-check passed')
    return 0


def main():
    args = sys.argv[1:]
    if '--test' in args:
        return self_test()
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

    light, dark, other = scope_maps(decls)

    lit_light, lit_dark = carried_values(tok)
    all_carried = lit_light | lit_dark

    rows = (classify(light, light, dark, lit_light, all_carried, 'light')
            + classify(dark, light, dark, lit_dark, all_carried, 'dark'))

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
    _b = bucket(gap_all, sem)
    generic, review, unresolved = _b['generic'], _b['review'], _b['unresolved']
    composite, triage = _b['composite'], _b['triage']
    print('CLAIM "the uncarried vars resolve to values already carried": %s'
          % ('HOLDS' if not gap_all
             else 'DOES NOT HOLD - %d declarations resolve to values tokens.json does not carry'
                  % len(gap_all)))
    print('  composite of values already carried:       %d  (not a missing value)'
          % len(composite))
    print('  unresolved expression:                     %d  (not a missing value)'
          % len(unresolved))
    print('  generic UI-kit ramp, evidenced exclusion:  %d' % len(generic))
    print('  DGA-namespaced, a real gap:                %d' % len(_b['semantic']))
    print('  unknown family, left for review:           %d' % len(review))
    print('  -> to triage (real gap + review):          %d' % len(triage))
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
    _b = bucket(gap, sem)
    generic, review, unresolved = _b['generic'], _b['review'], _b['unresolved']
    composite, triage = _b['composite'], _b['triage']

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
    # Every row of this table, summed, must equal the header total. An earlier version listed
    # only three of the five categories, so it showed 246 + 129 + 25 = 400 under a heading that
    # said 412: the twelve composites simply vanished, and unresolved entries would have too.
    # A reader cannot tell an omitted category from a category that is empty, so the assertion
    # below fails the run rather than publishing a table that does not add up.
    _TABLE = [
        ('Generic UI-kit ramp DGA ships but does not publish as a DGA token', generic, False),
        ('Composite of values already carried — the gradient set. Not a missing value: '
         'what is absent is the gradient *definition*', composite, False),
        ('Unresolved expression — still holds a `var()` nothing declares. Not evidence of a '
         'missing value', unresolved, False),
        ('**DGA-namespaced values this kit does not hold**', _b['semantic'], True),
        ('Unknown family, left for review rather than excluded', review, False),
    ]
    _sum = sum(len(rs) for _, rs, _ in _TABLE)
    if _sum != len(gap):
        raise AssertionError('report categories total %d but %d declarations did not reconcile - '
                             'a category is missing from _TABLE' % (_sum, len(gap)))
    add('| The %d that do not reconcile | Count |' % len(gap))
    add('|---|---|')
    for _label, _rs, _bold in _TABLE:
        add('| %s | %s |' % (_label, ('**%d**' % len(_rs)) if _bold else len(_rs)))
    add('| **To triage (the last two together)** | **%d** |\n' % len(triage))
    add('The first group is a defensible exclusion — DGA\'s stylesheet carries the whole upstream')
    add('Untitled-UI ramp (blue, cyan, fuchsia, indigo, moss, orange, pink, purple, red, teal,')
    add('violet, yellow, and seven separate grey ramps) and the published system names %d families.'
        % len(sem))
    add('It was never *stated* as an exclusion, which is the actual defect.\n')
    add('That exclusion list is **explicit, not inferred**. An earlier "anything not in the')
    add('semantic set" rule swept up `--colors-border-primary`, `--colors-text-primary` and the')
    add('`--colors-alpha-*` primitives as though they were ramp steps — and a wrong exclusion')
    add('**hides** a real gap. Anything neither evidenced-generic nor a known DGA family is left')
    add('for review and counted in the triage total, never dropped silently.\n')
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
        for _l in closing_note(triage, unresolved):
            add(_l)

    if composite:
        add('')
        add('### The %d composites of already-carried values\n' % len(composite))
        add('Not missing values. Every colour in each of these is already in `tokens.json`; what')
        add('the kit does not carry is the composite definition itself — the angle and the stops.')
        add('Listed so that is a decision someone makes, not an omission nobody sees.\n')
        add('| Scope | Custom property | Resolves to | Components carried |')
        add('|---|---|---|---|')
        for r in sorted(composite, key=lambda r: (r['scope'], r['name'])):
            add('| %s | `%s` | `%s` | %d/%d |'
                % (r['scope'], r['name'], str(r['resolved'])[:64],
                   len(r['components']), len(r['components'])))

    if unresolved:
        add('')
        add('### The %d unresolved expressions\n' % len(unresolved))
        add('⚠️ These still contain a `var()` after substitution — they reference something DGA')
        add('never declares in the scope they are used in. They are **not** counted as missing')
        add('values, because an expression nobody can resolve is not evidence this kit is short a')
        add('value. They are an open question about DGA\'s own stylesheet.\n')
        add('| Scope | Custom property | Declared | Left unresolved as |')
        add('|---|---|---|---|')
        for r in sorted(unresolved, key=lambda r: (r['scope'], r['name'])):
            add('| %s | `%s` | `%s` | `%s` |'
                % (r['scope'], r['name'], r['declared'][:44], str(r['resolved'])[:44]))
    p = os.path.join(ROOT, 'harvest', 'RECONCILIATION.md')
    open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\nwrote %s' % os.path.relpath(p, ROOT))


if __name__ == '__main__':
    sys.exit(main())
