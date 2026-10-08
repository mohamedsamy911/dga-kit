#!/usr/bin/env python3
"""Runtime discovery test: install this working tree into a throwaway Codex profile and check
which skills Codex actually sees.

Codex's `validate_plugin.py` no longer ships with Codex (gone by codex-cli 0.160.1), so this is
NOT a manifest validator and must not be described as one. It tests what a user gets: `codex
plugin add`, then `codex debug prompt-input`, which renders what the model would be shown without
a model call or a login. Passes when the set of discovered `dga-kit:<skill>` names equals the
directories under skills/.

What it catches (break-tested): a plugin.json that does not parse, a name that does not match
the marketplace entry, and an in-root skills path that does not exist. What it cannot catch,
because Codex 0.160.1 accepts them: unknown manifest keys, a missing `interface`, and an
out-of-root skills path (ignored - Codex falls back to skills/). validate-fixtures.py still pins
those against the schema the removed validator enforced.

Never touches the real ~/.codex: CODEX_HOME is a temp dir, deleted afterwards. With no `codex` on
PATH it FAILS. The step it replaces printed SKIPPED and passed on every CI run for as long as the
validator it looked for existed nowhere; a gate that cannot run must say so by failing. CI installs
the pinned CLI; locally, `npm install -g @openai/codex@0.160.1`.
"""
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
NAME = 'dga-kit'
PINNED = '0.160.1'   # keep in step with the npm install in .github/workflows/ci.yml


def run(args, env, cwd):
    p = subprocess.run(args, env=env, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True,
                       text=True, encoding='utf-8', errors='replace', timeout=300)
    if p.returncode:
        sys.exit(f'FAIL: {" ".join(args[1:])} exited {p.returncode}\n{p.stderr.strip()[-1500:]}')
    return p.stdout


def main():
    codex = shutil.which('codex')
    if not codex:
        print('FAIL: codex is not on PATH, so Codex skill discovery was not tested.')
        print('  npm install -g @openai/codex@0.160.1')
        return 1
    expected = {d.name for d in (ROOT / 'skills').iterdir() if (d / 'SKILL.md').is_file()}
    tmp = Path(tempfile.mkdtemp(prefix='dga-codex-smoke-')).resolve()
    try:
        src, home = tmp / 'plugin', tmp / 'home'   # home must sit OUTSIDE src, or the install
        home.mkdir()                              # copies the plugin into itself forever
        files = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True,
                               check=True).stdout.decode('utf-8').split('\0')
        for rel in filter(None, files):
            if (ROOT / rel).is_file():           # tracked but deleted in the working tree
                (src / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, src / rel)
        # The published marketplace installs from GitHub master; point it at this copy instead.
        mp = src / '.agents/plugins/marketplace.json'
        m = json.loads(mp.read_text(encoding='utf-8'))
        m['plugins'][0]['source'] = {'source': 'local', 'path': './'}
        mp.write_text(json.dumps(m, indent=2), encoding='utf-8')

        env = dict(os.environ, CODEX_HOME=str(home))
        version = run([codex, '--version'], env, tmp).strip()
        if PINNED not in version.split():
            print(f'FAIL: {version} is not the pinned codex-cli {PINNED}; discovery behaviour is '
                  f'version-specific (0.160.1 falls back silently on an out-of-root skills path).')
            return 1
        run([codex, 'plugin', 'marketplace', 'add', str(src)], env, tmp)
        run([codex, 'plugin', 'add', f'{NAME}@{NAME}'], env, tmp)
        seen = set(re.findall(NAME + r':(dga-[a-z0-9-]+)', run([codex, 'debug', 'prompt-input'],
                                                                 env, tmp)))
    finally:
        shutil.rmtree(tmp, onerror=lambda f, p, _: (os.chmod(p, stat.S_IWRITE), f(p)))
    if seen != expected:
        print(f'FAIL ({version}): Codex discovered {len(seen)} of {len(expected)} skills\n'
              f'  missing: {sorted(expected - seen)}\n  unexpected: {sorted(seen - expected)}')
        return 1
    print(f'codex discovery test passed: {len(seen)} skills discovered ({version})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
