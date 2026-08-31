import { readFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';

const root = fileURLToPath(new URL('../', import.meta.url));
const generated = 'src/styles/dga-tokens.css';
const theme = 'src/styles/theme.css';
// dga-kit 0.7.2; original generated content, normalized only for checkout line endings.
const tokenHash = 'ce1463638dc1f6be2b278360aad5f0109d34929a0d3d35266bf3a679bf5973a3';

function findings(source, file) {
  const clean = source.replace(/\/\*[\s\S]*?\*\//g, '');
  const errors = [];
  if (/var\(\s*--dga-text-secondary\s*[,)]/.test(clean)) errors.push('unsafe gold text role');
  if (file !== theme && /#[\da-f]{3,8}\b|\b(?:rgb|rgba|hsl|hsla)\s*\(/i.test(clean)) errors.push('color literal outside theme');
  if (file !== theme && /var\(\s*--dga-color-/.test(clean)) errors.push('primitive color outside theme');
  if (/(?:margin|padding|border)-(?:left|right)\s*:|(?:^|[;{\s])(?:left|right)\s*:|text-align\s*:\s*(?:left|right)/m.test(clean)) errors.push('physical directional CSS');
  return errors;
}

// Break tests: each defect must be detected independently, while a semantic declaration passes.
assert.deepEqual(findings('.x { color: var(--color-text); margin-inline-start: 1rem; }', 'src/styles/app.css'), []);
assert.deepEqual(findings('.x { color: var(--dga-text-secondary); }', 'src/styles/app.css'), ['unsafe gold text role']);
assert.deepEqual(findings('.x { color: #fff; }', 'src/styles/app.css'), ['color literal outside theme']);
assert.deepEqual(findings('.x { color: var(--dga-color-brand-600); }', 'src/styles/app.css'), ['primitive color outside theme']);
assert.deepEqual(findings('.x { margin-left: 1rem; }', 'src/styles/app.css'), ['physical directional CSS']);

function files(directory) {
  return readdirSync(path.join(root, directory), { withFileTypes: true }).flatMap(entry => {
    const next = `${directory}/${entry.name}`;
    return entry.isDirectory() ? files(next) : [next];
  });
}

const sources = files('src').filter(file => /\.(?:css|tsx)$/.test(file) && file !== generated);
assert(sources.includes(theme), 'Theme layer must exist');
assert(sources.includes('src/styles/app.css'), 'Application stylesheet must exist');
const original = readFileSync(path.join(root, generated), 'utf8').replaceAll('\r\n', '\n');
assert.equal(createHash('sha256').update(original).digest('hex'), tokenHash, 'Generated DGA tokens changed; update through a reviewed kit upgrade');

const errors = sources.flatMap(file => findings(readFileSync(path.join(root, file), 'utf8'), file).map(error => `${file}: ${error}`));
const css = [generated, ...sources.filter(file => file.endsWith('.css'))].map(file => readFileSync(path.join(root, file), 'utf8')).join('\n').replace(/\/\*[\s\S]*?\*\//g, '');
const declared = new Set([...css.matchAll(/(--[\w-]+)\s*:/g)].map(match => match[1]));
const referenced = new Set([...css.matchAll(/var\(\s*(--[\w-]+)/g)].map(match => match[1]));
for (const name of referenced) if (!declared.has(name)) errors.push(`Undefined CSS variable: ${name}`);
if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}
console.log(`Theme guard passed (${sources.length} source files, ${referenced.size} CSS references). Break tests passed; generated tokens are unchanged.`);
