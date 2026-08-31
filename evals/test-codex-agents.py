#!/usr/bin/env python3
"""Offline conversion and installer regressions; all installs use scratch folders."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load('build_codex_agents', ROOT / 'evals/build-codex-agents.py')


class CodexAgentsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='dga-codex-test-')
        self.addCleanup(self.temp.cleanup)
        # macOS's system temp path may itself contain /var -> /private/var.
        self.root = Path(self.temp.name).resolve()
        self.output = io.StringIO()
        self.redirect = contextlib.redirect_stdout(self.output)
        self.redirect.__enter__()
        self.addCleanup(self.redirect.__exit__, None, None, None)

    def clone(self):
        for folder in ('agents', 'codex-agents'):
            shutil.copytree(ROOT / folder, self.root / folder)
        return self.root

    def test_all_six_match_source_and_round_trip(self):
        self.assertEqual(builder.build(check=True), 0)
        sources = {p.stem for p in (ROOT / 'agents').glob('*.md')}
        self.assertEqual(sources, {p.stem for p in (ROOT / 'codex-agents').glob('*.toml')})
        self.assertEqual(len(sources), 6)
        payloads = {f.name: f.read_bytes() for f in (ROOT / 'codex-agents').glob('*.toml')}
        for name in sources:
            meta, body, read_only = builder.parse_source(ROOT / 'agents' / (name + '.md'))
            doc = tomllib.loads(payloads[name + '.toml'].decode('utf-8'))
            self.assertEqual(doc['description'], meta['description'])
            self.assertEqual(doc['developer_instructions'], builder.PREAMBLE + body)
            self.assertEqual(read_only, doc.get('sandbox_mode') == 'read-only')
            self.assertNotIn('model', doc)
            self.assertNotIn('model_reasoning_effort', doc)
            self.assertNotIn('tools', doc)

    def test_toml_escaping_preserves_arabic_quotes_backslashes_and_newlines(self):
        text = 'العربية """ \'\'\' C:\\temp\\name literal \\n\nactual newline\t\x01'
        self.assertEqual(tomllib.loads('value = ' + builder.multiline_string(text))['value'], text)

    def test_guard_rejects_generated_drift_without_repairing(self):
        root = self.clone()
        path = root / 'codex-agents/dga-designer.toml'
        altered = path.read_text(encoding='utf-8').replace('Principal-level', 'Altered', 1)
        path.write_text(altered, encoding='utf-8')
        self.assertEqual(builder.build(root, check=True), 1)
        self.assertEqual(path.read_text(encoding='utf-8'), altered)

    def test_guard_rejects_changed_source_and_missing_or_extra_agent(self):
        root = self.clone()
        source = root / 'agents/dga-designer.md'
        source.write_text(source.read_text(encoding='utf-8') + '\nNew instruction.\n',
                          encoding='utf-8')
        self.assertEqual(builder.build(root, check=True), 1)
        builder.build(root)
        self.assertEqual(builder.build(root, check=True), 0)
        (root / 'codex-agents/dga-designer.toml').unlink()
        self.assertEqual(builder.build(root, check=True), 1)
        builder.build(root)
        (root / 'codex-agents/unexpected.toml').write_text('name="unexpected"')
        with self.assertRaisesRegex(ValueError, 'Unexpected'):
            builder.build(root, check=True)
        # The installer's own refusal on a wrong file set is asserted by
        # `node bin/dga-kit.mjs --test`; here we only pin the builder's guard.

    def test_front_matter_is_parsed_not_scraped(self):
        source = self.root / 'dga-test.md'
        source.write_text('---\nname: dga-test\ndescription: bad: yaml\ntools: Read\n---\nBody')
        with self.assertRaises(builder.yaml.YAMLError):
            builder.render(source)

if __name__ == '__main__':
    unittest.main(verbosity=2)
