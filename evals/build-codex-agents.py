#!/usr/bin/env python3
"""Generate codex-agents/*.toml from agents/*.md; --check never writes.

Requires Python 3.11+ and PyYAML (the same dependency as validate-fixtures.py).
The Markdown agents remain the source of truth. Only the Codex runtime preamble
and read-only sandbox default are added; Claude tool names are not TOML fields.
"""
import argparse
import json
from pathlib import Path
import sys
import tomllib

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREAMBLE = """## Codex runtime

Use the matching installed dga-* skills before doing DGA work. Locate each skill
in Codex's available skills catalog and read its SKILL.md and required references.
If a required DGA skill is unavailable, stop and ask the user to install or enable
the dga-kit skills plugin; these agent definitions do not bundle the skills.

Paths below like ../skills/<skill>/..., <kit>/skills/<skill>/..., or
<skill>/references/... refer to the named installed skill. Resolve the suffix from
the directory containing that skill's SKILL.md, not from this agent file or the
project working directory. Plugin skills may live in Codex's plugin cache.

Use Codex's available tools to follow the instructions; do not assume Claude's
Skill tool exists. External skills such as design are optional: if unavailable,
state the limitation and use only the capabilities actually available. Never
install dependencies or skills without the user's authorization.

"""
CLAUDE_TOOLS = {'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob', 'WebFetch', 'Skill'}


def parse_source(path):
    text = path.read_text(encoding='utf-8')
    parts = text.split('---\n', 2)
    if len(parts) != 3 or parts[0]:
        raise ValueError(f'{path.name}: expected YAML front matter')
    meta = yaml.safe_load(parts[1])
    if not isinstance(meta, dict) or set(meta) != {'name', 'description', 'tools'}:
        raise ValueError(f'{path.name}: unsupported front matter; review the conversion')
    if meta['name'] != path.stem:
        raise ValueError(f'{path.name}: name must match filename')
    if any(not isinstance(meta[k], str) or not meta[k].strip() for k in meta):
        raise ValueError(f'{path.name}: front matter values must be nonempty strings')
    tool_names = {t.strip() for t in meta['tools'].split(',')}
    if not tool_names or not tool_names <= CLAUDE_TOOLS:
        raise ValueError(f'{path.name}: unsupported Claude tools: {tool_names - CLAUDE_TOOLS}')
    body = parts[2].lstrip('\n')
    if not body.strip():
        raise ValueError(f'{path.name}: empty instructions')
    return meta, body, not bool(tool_names & {'Write', 'Edit'})


def multiline_string(text):
    # Escape character by character: replacing '\\n' in a JSON string would also
    # corrupt literal backslash-n examples. TOML trims the opening newline only.
    escaped = ''.join('\n' if c == '\n' else json.dumps(c, ensure_ascii=False)[1:-1]
                      for c in text)
    return '"""\n' + escaped + '"""'


def render(path):
    meta, body, read_only = parse_source(path)
    fields = {'name': meta['name'], 'description': meta['description']}
    if read_only:
        fields['sandbox_mode'] = 'read-only'
    text = (f'# Generated from agents/{path.name}; DO NOT EDIT.\n'
            '# Regenerate: python evals/build-codex-agents.py\n'
            '# Schema: https://learn.chatgpt.com/docs/agent-configuration/subagents\n\n')
    text += ''.join(f'{k} = {json.dumps(v, ensure_ascii=False)}\n' for k, v in fields.items())
    instructions = PREAMBLE + body
    text += 'developer_instructions = ' + multiline_string(instructions) + '\n'
    if tomllib.loads(text) != {**fields, 'developer_instructions': instructions}:
        raise ValueError(f'{path.name}: TOML round trip changed the instructions')
    return text


def build(root=ROOT, check=False):
    sources = sorted((root / 'agents').glob('*.md'))
    if not sources:
        raise ValueError('No Markdown agent definitions found')
    expected = {p.with_suffix('.toml').name: render(p) for p in sources}
    output = root / 'codex-agents'
    extra = {p.name for p in output.glob('*.toml')} - set(expected)
    if extra:
        raise ValueError(f'Unexpected Codex agent files (not removed): {sorted(extra)}')
    stale = [name for name, text in expected.items()
             if not (output / name).is_file()
             or (output / name).read_text(encoding='utf-8') != text]
    if check:
        if stale:
            print('STALE Codex agents: ' + ', '.join(stale))
            print('Run: python evals/build-codex-agents.py')
            return 1
        print(f'Codex agents are current ({len(expected)} definitions)')
        return 0
    output.mkdir(exist_ok=True)
    for name, text in expected.items():
        (output / name).write_text(text, encoding='utf-8', newline='\n')
    print(f'Generated {len(expected)} Codex agents in {output}')
    return 0


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='fail on drift; write nothing')
    args = parser.parse_args()
    try:
        return build(check=args.check)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
