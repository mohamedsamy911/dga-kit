#!/usr/bin/env node
// One installer for both targets, in one runtime.
//
//   npx github:mohamedsamy911/dga-kit            Claude skills + agents, and Codex agents
//   npx github:mohamedsamy911/dga-kit --claude   Claude only
//   npx github:mohamedsamy911/dga-kit --codex    Codex agents only
//   ... --project PATH                           Codex agents into PATH/.codex/agents
//   ... --force                                  overwrite/adopt a dga-* path not in the manifest
//   ... --uninstall                              remove only what this installer recorded,
//                                                honouring the same --claude/--codex/--skills/--agents
//   ... --clean-legacy                           remove pre-0.5 paths, after typing DELETE
//   ... --dry-run                                print what would happen, write nothing
//   ... --test                                   offline self-check of the safety guards
//
// This replaced install-skills.sh, install-skills.ps1 and install-codex-agents.py. Three
// implementations of one behaviour is the drift this repo spends its CI preventing, and the
// shell pair had already diverged once (`xargs -r` worked on Linux and broke on macOS). Node is
// the runtime this kit's users - frontend developers - are guaranteed to have; the Python
// installer additionally needed 3.11+ for tomllib, and every path needed a git clone first.
//
// OWNERSHIP, carried over verbatim in intent. A path is deleted only if BOTH hold:
//   1. it is recorded in the manifest, and
//   2. it matches the fixed allowlist - skills/<SKILLS> or agents/<AGENTS>.md
// The manifest is editable text, so it is a record and NOT an authority; condition 2 is what
// makes a corrupted manifest harmless. Nothing is removed by name alone, and a path the
// manifest does not claim is treated as YOURS. --force is the only thing that touches an
// unclaimed path, it still only writes allowlisted dga-* names, and it announces each one.
import { existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, rmSync, cpSync,
         writeFileSync, appendFileSync, statSync, symlinkSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, join, resolve, isAbsolute, relative } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createInterface } from 'node:readline'
import { execFileSync } from 'node:child_process'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')

const SKILLS = ['dga-design-system', 'dga-design-review', 'dga-react', 'dga-ui-adapter',
  'dga-rtl-i18n', 'dga-handoff', 'dga-mockup', 'dga-a11y', 'dga-launch-gate',
  'dga-tokens-sync', 'dga-brand-overlay']
const AGENTS = ['dga-designer', 'dga-frontend-architect', 'dga-frontend-dev',
  'dga-code-reviewer', 'dga-compliance-auditor', 'dga-content-writer']
// Renamed or removed in 0.5.0. NEVER deleted automatically - see --clean-legacy.
const LEGACY_SKILLS = ['dga-chakra', 'rga-brand']
const LEGACY_AGENTS = ['designer', 'frontend-dev']
// Codex agents that must ship with a read-only sandbox: they report, they never edit.
const READ_ONLY = new Set(['dga-code-reviewer', 'dga-compliance-auditor', 'dga-frontend-architect'])

const USAGE = `dga-kit installer

  npx github:mohamedsamy911/dga-kit [flags]

With no flags it installs EVERYTHING it can, for every tool it finds on this machine:
Claude Code skills + agents, and Codex skills + agents.

  WHICH TOOL          --claude            Claude Code only
                      --codex             Codex only

  WHICH KIND          --skills            skills only
                      --agents            agents only

  Combine one of each to reach a single cell, e.g. --codex --skills.

  WHERE               --project PATH      Codex agents into PATH/.codex/agents, not your home
                                          (DGA_KIT_HOME and CODEX_HOME override the destinations)

  OTHER               --dry-run           print the plan, write nothing
                      --force             overwrite/adopt a dga-* path not in the manifest
                      --uninstall         remove only what this installer wrote; obeys the
                                          same tool/kind selectors as an install
                      --clean-legacy      remove pre-0.5 paths, after typing DELETE
                      --test              offline self-check of the safety guards
                      --help              this

Codex SKILLS go through \`codex plugin add\`, because Codex serves plugin skills from its own
cache plus config.toml rather than a directory anything else can write. Everything else is a
file copy. A file you edited is never overwritten unless you pass --force - and a differing
Codex agent is refused even then.`

let DRY = false
const out = []
const say = (s) => { out.push(s); console.log(s) }
const fail = (s) => { const e = new Error(s); e.expected = true; throw e }

// --- safety -------------------------------------------------------------------

/** Refuse symlinks and Windows reparse points, on the path AND every parent.
 *
 *  lstat is called WITHOUT an existsSync() precheck. That precheck was the bug: existsSync()
 *  follows the link, so a DANGLING symlink - one whose target does not exist yet - answered
 *  false, the lstat never ran, and the write then created the target through the link, outside
 *  the destination entirely. Reproduced: a link at .codex/agents/dga-designer.toml pointing at
 *  ../outside/planted.toml produced ../outside/planted.toml.
 *
 *  ENOENT means the entry genuinely is not there, which is normal and fine. Any other errno is
 *  a filesystem answering strangely and is treated as a refusal, not a shrug.
 */
function plainPath(p) {
  let cur = resolve(p)
  for (;;) {
    let st = null
    try {
      st = lstatSync(cur)
    } catch (e) {
      if (e.code !== 'ENOENT') fail(`Cannot inspect ${cur}: ${e.code || e.message}`)
    }
    // 0xa000 is S_IFLNK; on Windows a junction/reparse point surfaces the same way through lstat.
    if (st && (st.isSymbolicLink() || ((st.mode & 0xf000) === 0xa000))) {
      fail(`Refusing linked path: ${cur}`)
    }
    const up = dirname(cur)
    if (up === cur) return
    cur = up
  }
}

/** Is anything at this path - INCLUDING a link whose target is missing?
 *
 *  existsSync() follows links, so it answers false for a dangling one. Every "does this already
 *  exist" decision in the installer used it, and so treated a dangling link as an empty slot:
 *  a user's symlinked agent was silently replaced by a regular file with no --force, and a
 *  symlinked skill directory the same. lstat does not follow, so it sees the link itself.
 */
function present(p) {
  try {
    lstatSync(p)
    return true
  } catch (e) {
    if (e.code === 'ENOENT') return false
    return true                 // EACCES/EPERM: something is there and we cannot see it
  }
}

/** Create a file that must not already exist.
 *
 *  Exclusive creation ('wx') is the second half of the dangling-link fix: even if a link were
 *  planted between the guard above and this write, 'wx' refuses rather than following it.
 */
function write(p, data) {
  if (DRY) return
  plainPath(dirname(p))
  mkdirSync(dirname(p), { recursive: true })
  plainPath(p)
  try {
    writeFileSync(p, data, { flag: 'wx' })
  } catch (e) {
    if (e.code === 'EEXIST') fail(`Refusing to overwrite ${p} - it appeared after the preflight`)
    throw e
  }
}

/** The manifest, as a list of paths.
 *
 *  One reader, and it strips a BOM. Windows PowerShell 5.1 writes UTF-8 WITH a byte-order mark,
 *  so a manifest from the old install-skills.ps1 begins "\uFEFFC:\Users\...". Read raw, that
 *  first entry is a path nothing can match: it was refused as out-of-allowlist and its skill
 *  left orphaned on every uninstall.
 */
function readManifest(home) {
  const m = manifestPath(home)
  // A SYMLINKED manifest is not ours to read or append to. Unguarded, `claim()` appended
  // installed paths into whatever the link pointed at - reproduced against an external
  // settings.json, which stopped being valid JSON.
  plainPath(m)
  if (!present(m)) return null
  return readFileSync(m, 'utf8').split(/\r?\n/)
    // U+FEFF is whitespace to .trim(), so either of these alone would do. Both are kept: the
    // explicit strip states the intent, and without it .trim() reads as cosmetic and invites
    // deletion - which is precisely how the BOM entry got orphaned before.
    .map((l) => l.replace(/^\uFEFF/, '').trim()).filter(Boolean)
}

// --- manifest -----------------------------------------------------------------

const manifestPath = (home) => join(home, '.claude', '.dga-kit-manifest')

function owns(home, p) {
  const entries = readManifest(home)
  return entries !== null && entries.includes(p)
}

function claim(home, p) {
  if (DRY) return
  const m = manifestPath(home)
  plainPath(dirname(m))
  mkdirSync(dirname(m), { recursive: true })
  plainPath(m)
  if (!present(m)) writeFileSync(m, '')
  if (!(readManifest(home) || []).includes(p)) appendFileSync(m, p + '\n')
}

// --- Codex agents -------------------------------------------------------------

/** Parse the flat `key = "..."` / `key = """..."""` subset these generated files use.
 *
 *  Deliberately NOT a general TOML parser. The six files are generated by this repo and
 *  validated below against an exact field set, so a permissive parser would only widen what
 *  can pass unnoticed. Anything it cannot read is an error, not a shrug.
 */
function parseAgentToml(text) {
  const doc = {}
  let i = 0
  const src = text.replace(/\r\n/g, '\n')
  while (i < src.length) {
    const rest = src.slice(i)
    const blank = rest.match(/^([ \t]*(#[^\n]*)?\n)/)
    if (blank) { i += blank[0].length; continue }
    const m = rest.match(/^([A-Za-z_][A-Za-z0-9_]*)[ \t]*=[ \t]*/)
    if (!m) fail(`Unparseable line in agent TOML: ${rest.slice(0, 60)}`)
    i += m[0].length
    const key = m[1]
    if (src.startsWith('"""', i)) {
      const end = src.indexOf('"""', i + 3)
      if (end < 0) fail(`Unterminated """ block for key ${key}`)
      let v = src.slice(i + 3, end)
      if (v.startsWith('\n')) v = v.slice(1)   // TOML trims one leading newline
      doc[key] = v
      i = end + 3
    } else if (src[i] === '"') {
      const line = src.slice(i).match(/^"((?:[^"\\]|\\.)*)"/)
      if (!line) fail(`Unterminated string for key ${key}`)
      doc[key] = line[1].replace(/\\"/g, '"').replace(/\\\\/g, '\\')
      i += line[0].length
    } else {
      fail(`Key ${key} is not a string; this installer ships only string fields`)
    }
    const tail = src.slice(i).match(/^[ \t]*(#[^\n]*)?(\n|$)/)
    if (!tail) fail(`Trailing content after key ${key}`)
    i += tail[0].length
  }
  return doc
}

/** Read and validate the six generated agents. Throws rather than installing something odd. */
function codexPayloads() {
  const src = join(ROOT, 'codex-agents')
  if (!existsSync(src)) fail(`codex-agents/ not found at ${src}`)
  const found = readdirSync(src).filter((f) => f.endsWith('.toml')).sort()
  const want = AGENTS.map((n) => n + '.toml').sort()
  if (found.join(',') !== want.join(',')) {
    fail(`Expected exactly the ${AGENTS.length} generated codex-agents/*.toml files, found: ${found.join(', ')}`)
  }
  const files = new Map()
  for (const name of AGENTS) {
    const p = join(src, name + '.toml')
    plainPath(p)
    const data = readFileSync(p)
    const doc = parseAgentToml(data.toString('utf8'))
    const required = ['name', 'description', 'developer_instructions']
    const expected = new Set(required.concat(READ_ONLY.has(name) ? ['sandbox_mode'] : []))
    const got = new Set(Object.keys(doc))
    if (got.size !== expected.size || [...got].some((k) => !expected.has(k))) {
      fail(`${name}.toml: unexpected field set [${[...got].join(', ')}], expected [${[...expected].join(', ')}]`)
    }
    if (doc.name !== name) fail(`${name}.toml: name field is "${doc.name}"`)
    for (const k of required) {
      if (typeof doc[k] !== 'string' || !doc[k].trim()) fail(`${name}.toml: empty or invalid ${k}`)
    }
    if (READ_ONLY.has(name) && doc.sandbox_mode !== 'read-only') {
      fail(`${name}.toml: must declare sandbox_mode = "read-only"`)
    }
    files.set(name + '.toml', data)
  }
  return files
}

function codexTarget({ project }) {
  if (project != null) {
    const root = resolve(project)
    plainPath(root)
    if (!existsSync(root) || !statSync(root).isDirectory()) fail(`Project directory does not exist: ${root}`)
    return join(root, '.codex', 'agents')
  }
  const configured = process.env.CODEX_HOME
  if (configured) {
    // isAbsolute on the RAW value. The old test called resolve() first, which always returns
    // an absolute path, so it could never fire - and a relative CODEX_HOME was silently
    // resolved against the current directory, installing agents wherever npx happened to run.
    if (!isAbsolute(configured)) {
      fail(`CODEX_HOME must be an absolute path, got: ${configured}`)
    }
    const root = resolve(configured)
    plainPath(root)
    return join(root, 'agents')
  }
  return join(homedir(), '.codex', 'agents')
}

function installCodex(opts) {
  const target = codexTarget(opts)
  plainPath(target)
  if (existsSync(target) && !statSync(target).isDirectory()) fail(`Not a directory: ${target}`)
  const files = codexPayloads()

  // Preflight everything before writing anything: a half-installed agent set is worse than a
  // refusal, because Codex will happily load the half.
  const pending = []
  const conflicts = []
  for (const [name, data] of files) {
    const p = join(target, name)
    plainPath(p)
    if (existsSync(p)) {
      if (!statSync(p).isFile() || !readFileSync(p).equals(data)) conflicts.push(p)
    } else {
      pending.push([p, data])
    }
  }
  if (conflicts.length) {
    // A dry run REPORTS the conflict; it must never fail because of the state it is describing.
    // Reporting the plan is the whole job, and exiting non-zero made --dry-run useless as a
    // check on any machine that already had agents installed - including the author's.
    if (DRY) {
      for (const c of conflicts) say(`WOULD REFUSE ${c} - exists and differs; a real run stops here`)
    } else {
      fail('Existing Codex agents differ; nothing installed. Move these aside and retry:\n  '
        + conflicts.join('\n  '))
    }
  }
  for (const [p, data] of pending) {
    write(p, data)
    say(`${DRY ? 'would install' : 'installed'} codex agent ${relative(target, p)}`)
  }
  // Count conflicts separately: they are neither copied NOR identical, and folding them into
  // "already identical" told a dry run that a file it had just refused was fine.
  const identical = files.size - pending.length - conflicts.length
  say(`Codex agents: ${files.size} total (${pending.length} ${DRY ? 'to copy' : 'copied'}, `
    + `${identical} already identical`
    + (conflicts.length ? `, ${conflicts.length} refused` : '') + `) in ${target}`)
  return pending.length
}

// --- Claude skills + agents ---------------------------------------------------

function legacyNotice(home) {
  const dest = join(home, '.claude', 'skills')
  const adest = join(home, '.claude', 'agents')
  let found = false
  for (const n of LEGACY_SKILLS) {
    if (existsSync(join(dest, n))) { say(`note      ${join(dest, n)} is from dga-kit <=0.4 and is no longer used.`); found = true }
  }
  for (const a of LEGACY_AGENTS) {
    const p = join(adest, a + '.md')
    if (existsSync(p) && readFileSync(p, 'utf8').includes('_shared/dga.md')) {
      say(`note      ${p} looks like dga-kit <=0.4; superseded by dga-${a}.md.`); found = true
    }
  }
  if (existsSync(join(adest, '_shared'))) { say(`note      ${join(adest, '_shared')}/ is from dga-kit <=0.4.`); found = true }
  if (found) say('          Nothing was deleted. Review, then use --clean-legacy or remove by hand.')
}

function installClaude(home, { force, skills = true, agents = true }) {
  const src = join(ROOT, 'skills')
  const asrc = join(ROOT, 'agents')
  if (!existsSync(src)) fail(`skills/ not found at ${src}`)
  const dest = join(home, '.claude', 'skills')
  const adest = join(home, '.claude', 'agents')
  plainPath(dest); plainPath(adest)
  // PREFLIGHT the manifest before copying anything. claim() runs after each copy, so a
  // symlinked or unwritable manifest used to abort mid-install with files already on disk and
  // nothing recording them - untracked, and invisible to --uninstall forever.
  plainPath(manifestPath(home))
  if (!DRY) { mkdirSync(dest, { recursive: true }); mkdirSync(adest, { recursive: true }) }
  legacyNotice(home)

  let ok = 0
  for (const n of (skills ? SKILLS : [])) {
    const d = join(dest, n)
    if (!existsSync(join(src, n, 'SKILL.md'))) { say(`skipped   ${n} (no SKILL.md)`); continue }
    if (present(d) && !owns(home, d)) {
      if (force) say(`OVERWRITE ${n} - not in manifest, --force given`)
      else {
        say(`SKIPPED   ${n} - exists and is not in our manifest. Left untouched.`)
        say('          If it is an older dga-kit, re-run with --force to adopt it.')
        continue
      }
    } else if (present(d) && !force) { say(`exists    ${n} (use --force)`); continue }
    // Guard the LEAF too: the parents were checked, this is the one that gets replaced.
    plainPath(d)
    if (!DRY) { rmSync(d, { recursive: true, force: true }); cpSync(join(src, n), d, { recursive: true }) }
    claim(home, d); ok++; say(`${DRY ? 'would install' : 'installed'} skill ${n}`)
  }

  let aok = 0
  for (const a of (agents ? AGENTS : [])) {
    const d = join(adest, a + '.md')
    if (!existsSync(join(asrc, a + '.md'))) { say(`skipped   ${a} (missing)`); continue }
    if (present(d) && !owns(home, d)) {
      if (force) say(`OVERWRITE ${a} - not in manifest, --force given`)
      else {
        say(`SKIPPED   ${a} - exists and is not in our manifest. Left untouched.`)
        say('          If it is an older dga-kit, re-run with --force to adopt it.')
        continue
      }
    } else if (present(d) && !force) { say(`exists    ${a} (use --force)`); continue }
    plainPath(d)
    if (!DRY) cpSync(join(asrc, a + '.md'), d)
    claim(home, d); aok++; say(`${DRY ? 'would install' : 'installed'} agent ${a}`)
  }
  return { ok, aok, dest }
}

// --- what is actually on this machine ---------------------------------------

/** Run a CLI, portably.
 *
 *  On Windows an npm-installed CLI is a `codex.cmd` shim, and execFileSync CANNOT launch a batch
 *  file directly: bare `codex` gives ENOENT and even an explicit `codex.cmd` gives EINVAL. Only
 *  a shell can. So `shell: true` on win32 only - POSIX keeps the direct exec, which is the safer
 *  of the two and needs no quoting.
 *
 *  This is why every argument below is a HARDCODED CONSTANT. Nothing user-supplied is ever
 *  passed here: under `shell: true` an argument is shell syntax, so a path or a name from the
 *  command line would be an injection surface. If that ever has to change, quote explicitly or
 *  drop back to a direct exec with the resolved shim path.
 */
function runCli(bin, args, opts = {}) {
  const CONST = /^[A-Za-z0-9@/._-]+$/
  for (const a of args) {
    if (!CONST.test(a)) fail(`Refusing to shell-execute a non-constant argument: ${a}`)
  }
  return execFileSync(bin, args, { shell: process.platform === 'win32', ...opts })
}

/** Is a CLI callable? Probed by running it, not by searching PATH - `which`/`where` is a
 *  platform binary and this installer deliberately depends on none. */
function hasCli(bin) {
  try {
    runCli(bin, ['--version'], { stdio: 'ignore', timeout: 15000 })
    return true
  } catch { return false }
}

/** Detect the targets. A tool counts as present if its home exists OR its CLI answers, because
 *  a fresh Codex install may have a CLI and no ~/.codex yet, and a machine restored from backup
 *  may have ~/.claude and no CLI on PATH. */
function detect(home) {
  return {
    claude: existsSync(join(home, '.claude')) || hasCli('claude'),
    codexHome: existsSync(process.env.CODEX_HOME || join(home, '.codex')),
    codexCli: hasCli('codex'),
  }
}

// --- Codex skills, through Codex's own CLI ------------------------------------

/** Codex does NOT serve skills from a directory we could copy into.
 *
 *  A plugin lives in ~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/ as a git clone AND
 *  is registered in ~/.codex/config.toml under [plugins."name@marketplace"]. Hand-writing that
 *  config would mean reimplementing Codex's own installer against an undocumented layout, and
 *  getting it wrong corrupts the user's tool configuration. So the skills go in the supported
 *  way: by invoking `codex`. Its absence is reported, never worked around.
 *
 *  Returns 'done' | 'planned' | 'failed'. The caller propagates 'failed' into the exit code.
 *  It used to swallow BOTH subprocess failures as "it may already be added" and return 'done'
 *  regardless - so a genuinely failed `plugin add` reported success and the user was told to
 *  restart Codex and expect skills that were never installed.
 */
function installCodexSkills({ dryRun }) {
  const MARKETPLACE = ['plugin', 'marketplace', 'add', 'mohamedsamy911/dga-kit']
  const ADD = ['plugin', 'add', 'dga-kit@dga-kit']
  if (dryRun) {
    for (const a of [MARKETPLACE, ADD]) say(`would run: codex ${a.join(' ')}`)
    return 'planned'
  }

  // `marketplace add` failing because it is ALREADY added is the one tolerable failure, and it
  // is only tolerable when the output says so. Anything else is a real failure.
  const ALREADY = /already (added|exists|registered)|duplicate|exists already/i
  say(`running: codex ${MARKETPLACE.join(' ')}`)
  try {
    runCli('codex', MARKETPLACE, { stdio: 'pipe', timeout: 300000 })
  } catch (e) {
    const text = `${e.stdout || ''}${e.stderr || ''}`
    if (ALREADY.test(text)) {
      say('note      marketplace already registered - continuing')
    } else {
      say(`ERROR     codex ${MARKETPLACE.join(' ')} failed:`)
      say(`          ${text.trim().split('\n').slice(-3).join('\n          ') || e.message}`)
      return 'failed'
    }
  }

  say(`running: codex ${ADD.join(' ')}`)
  try {
    runCli('codex', ADD, { stdio: 'inherit', timeout: 300000 })
  } catch (e) {
    // No tolerance here at all: this IS the install. If it did not succeed, nothing did.
    say(`ERROR     codex ${ADD.join(' ')} failed - the Codex skills are NOT installed.`)
    say(`          ${e.message}`)
    return 'failed'
  }
  return 'done'
}

// --- cross-reference verification ---------------------------------------------

function walk(dir, out = []) {
  if (!existsSync(dir)) return out
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name)
    if (e.isDirectory()) walk(p, out)
    else out.push(p)
  }
  return out
}

const UNSHIPPED = /(harvest|evals)\/[A-Za-z0-9_./-]+|COVERAGE\.md|README\.md|AGENTS\.md|CHANGELOG\.md/g
const SIBLING = /\.\.\/[A-Za-z0-9_./-]+\.(?:md|json|css|mjs|js|ts)/g

/** Two ways a reference dies on install, both checked against the tree that actually landed. */
function verify(dest) {
  let bad = 0
  const files = SKILLS.flatMap((n) => walk(join(dest, n)))

  // 1. Sibling refs. Skills reach each other as ../dga-design-system/..., so the flat layout is
  //    required and every relative link must resolve where it landed.
  for (const f of files.filter((f) => f.endsWith('.md'))) {
    const text = readFileSync(f, 'utf8')
    for (const ref of new Set(text.match(SIBLING) || [])) {
      if (!existsSync(resolve(dirname(f), ref))) { say(`BROKEN    ${f} -> ${ref}`); bad++ }
    }
  }

  // 2. Repo-root refs. harvest/, evals/, COVERAGE.md and friends are NOT copied here, so a skill
  //    naming one reads fine in the repo and is a dead end for every installed user. Only a
  //    canonical GitHub URL exempts an occurrence - and it is COUNTED, not merely tested, because
  //    a file may carry one correct URL and a bare mention of the same path.
  for (const f of files.filter((f) => f.endsWith('.md') || f.endsWith('.json'))) {
    // Fenced blocks are commands a maintainer runs from a clone, not references.
    let fenced = false
    const body = readFileSync(f, 'utf8').split(/\r?\n/)
      .filter((l) => { if (l.startsWith('```')) { fenced = !fenced; return false } return !fenced })
      .join('\n')
    for (const ref of new Set(body.match(UNSHIPPED) || [])) {
      const lit = ref.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      const total = (body.match(new RegExp(lit, 'g')) || []).length
      let linked = 0
      for (const pre of ['https://github\\.com/mohamedsamy911/dga-kit/blob/',
                         'https://raw\\.githubusercontent\\.com/mohamedsamy911/dga-kit/']) {
        linked += (body.match(new RegExp(pre + '[A-Za-z0-9._-]+/' + lit, 'g')) || []).length
      }
      const bare = total - linked
      if (bare > 0) { say(`UNSHIPPED ${f} -> ${ref} x${bare} (not installed; use a full GitHub URL)`); bad++ }
    }
  }
  return bad
}

// --- uninstall / clean-legacy -------------------------------------------------

/** Remove what this installer wrote, honouring the SAME selectors as an install.
 *
 *  Two defects this shape exists to prevent, both found in review:
 *
 *  1. `--claude --uninstall` used to delete Codex agents as well, because uninstall was
 *     dispatched before the selector flags were parsed and then ignored them. Removal is now
 *     scoped by exactly the plan an install would use, and manifest entries outside that scope
 *     are PRESERVED - the manifest is rewritten with what was kept, never blanket-deleted, so a
 *     scoped uninstall does not orphan the paths it deliberately left behind.
 *  2. Removal did not validate path ancestry the way installation does. A Windows junction on
 *     the destination let a delete follow the link and remove a file in an unrelated directory:
 *     the allowlist compared STRINGS, and the string was fine - the directory was not.
 *     plainPath() now guards every removal, so a linked ancestor refuses instead of following.
 */
function uninstall(home, opts, want) {
  const m = manifestPath(home)
  const dest = join(home, '.claude', 'skills')
  const adest = join(home, '.claude', 'agents')

  /** Delete only after re-checking the path is not, and is not under, a link. */
  const removeGuarded = (p) => {
    try {
      plainPath(p)
    } catch (e) {
      say(`REFUSED   ${p} - ${e.message}. Left untouched.`)
      return false
    }
    if (!DRY) rmSync(p, { recursive: true, force: true })
    say(`${DRY ? 'would remove' : 'removed  '} ${p}`)
    return true
  }

  // Codex agents are content-addressed: only a byte-identical file is ours to remove, so an
  // edited copy always survives.
  let codexRemoved = 0
  if (want.codex && want.agents) {
    try {
      const target = codexTarget(opts)
      if (existsSync(target)) {
        for (const [name, data] of codexPayloads()) {
          const p = join(target, name)
          if (!existsSync(p)) continue
          if (statSync(p).isFile() && readFileSync(p).equals(data)) {
            if (removeGuarded(p)) codexRemoved++
          } else {
            say(`KEPT      ${p} - differs from what this installer wrote. Left untouched.`)
          }
        }
      }
    } catch (e) { if (!e.expected) throw e; say(`note      Codex agents not removed: ${e.message}`) }
  }

  if (want.codex && want.skills) {
    say('note      Codex SKILLS are a plugin; remove them with `codex plugin remove dga-kit@dga-kit`.')
  }

  let removed = 0, refused = 0, kept = 0
  if (want.claude && readManifest(home)) {
    // In scope for THIS run - not merely "a path this kit could create".
    const inScope = new Set([
      ...(want.skills ? SKILLS.map((n) => join(dest, n)) : []),
      ...(want.agents ? AGENTS.map((a) => join(adest, a + '.md')) : []),
    ])
    const everOurs = new Set([...SKILLS.map((n) => join(dest, n)),
                              ...AGENTS.map((a) => join(adest, a + '.md'))])
    const survivors = []
    for (const p of readManifest(home)) {
      if (!everOurs.has(p)) {
        say(`REFUSED   ${p} - in the manifest but not a path this kit can create. Left untouched.`)
        refused++; survivors.push(p); continue
      }
      if (!inScope.has(p)) { kept++; survivors.push(p); continue }
      if (!existsSync(p)) continue
      if (removeGuarded(p)) removed++
      else survivors.push(p)          // a refusal keeps its record; we still own it
    }
    if (!DRY) {
      if (survivors.length) writeFileSync(m, survivors.join('\n') + '\n')
      else rmSync(m, { force: true })
    }
  } else if (want.claude) {
    say(`No manifest at ${m} - this installer has no record of installing Claude files.`)
    say('Refusing to delete by name. Remove paths by hand if you are sure they are ours.')
    if (codexRemoved === 0) return 1
  }

  say('')
  say(`${removed} Claude path(s) and ${codexRemoved} Codex agent(s) removed - only those this `
    + 'installer recorded AND could have created.')
  if (kept) say(`${kept} recorded path(s) left in place, outside the selectors you passed.`)
  if (refused) say(`${refused} manifest entry/entries refused as out-of-allowlist - remove them by hand if they are yours.`)
  say(DRY ? 'Dry run - nothing was removed.' : 'Restart Claude Code and Codex.')
  return 0
}

async function cleanLegacy(home) {
  const dest = join(home, '.claude', 'skills')
  const adest = join(home, '.claude', 'agents')
  const targets = [...LEGACY_SKILLS.map((n) => join(dest, n)), join(adest, '_shared')].filter(existsSync)
  if (!targets.length) { say('No pre-0.5 paths found.'); return 0 }
  say('These paths will be PERMANENTLY DELETED:')
  targets.forEach((p) => say(`  ${p}`))
  say('')
  say('dga-kit cannot prove it created these - a skill of your own may share a name.')
  const rl = createInterface({ input: process.stdin, output: process.stdout })
  const reply = await new Promise((r) => rl.question('Type DELETE to confirm: ', (a) => { rl.close(); r(a) }))
  if (reply.trim() !== 'DELETE') { say('Aborted. Nothing removed.'); return 1 }
  for (const p of targets) {
    // Guard the deletion the same way uninstall does: a linked legacy directory would
    // otherwise be followed and something outside it removed.
    try {
      plainPath(p)
    } catch (e) {
      say(`REFUSED   ${p} - ${e.message}. Left untouched.`)
      continue
    }
    if (!DRY) rmSync(p, { recursive: true, force: true })
    say(`${DRY ? 'would remove' : 'removed  '} ${p}`)
  }
  say('Legacy agent .md files were NOT touched - those names are generic. Remove by hand if yours.')
  return 0
}

// --- self-check ---------------------------------------------------------------

/** A private scratch directory this process CREATED, never one it merely found.
 *
 *  The self-check used five fixed names under the temp directory and `rm -rf`'d each before
 *  taking ownership. Anything a user or a concurrent run had left at one of those paths was
 *  destroyed - silently, while the check reported success - and two runs in parallel would
 *  delete each other's fixtures mid-assertion. mkdirSync without `recursive` throws EEXIST, so
 *  the directory returned here is provably new.
 */
let _scratchSeq = 0
function scratchDir(label) {
  const base = process.env.RUNNER_TEMP || process.env.TMPDIR || process.env.TEMP || '.'
  for (let attempt = 0; attempt < 1000; attempt++) {
    // No Math.random(): the pid plus a counter is unique per process and reproducible in a log.
    const p = join(base, `dga-kit-selftest-${process.pid}-${_scratchSeq++}-${label}`)
    try {
      mkdirSync(p)          // NOT recursive: throws EEXIST rather than adopting someone's dir
      _scratch.push(p)
      return p
    } catch (e) {
      if (e.code !== 'EEXIST') throw e
    }
  }
  fail('could not create a private scratch directory')
}
const _scratch = []
function cleanScratch() {
  for (const p of _scratch.splice(0)) rmSync(p, { recursive: true, force: true })
}

/** Offline assertions for the safety properties, no filesystem writes outside a temp dir.
 *
 *  These moved here from the Python installer's unittest suite when three installers became
 *  one. The end-to-end behaviour (install, idempotence, refusal, uninstall scoping, no leak into
 *  the real profile) is exercised by CI on macOS, Linux and Windows; what CI cannot easily reach
 *  is symlink refusal and the agent-payload validation, so those are pinned here.
 */
function selfTest() {
  try {
    return runSelfTest()
  } finally {
    cleanScratch()
  }
}

function runSelfTest() {
  const assert = (cond, msg) => { if (!cond) throw new Error('SELF-CHECK: ' + msg) }
  const throws = (fn, msg) => {
    try { fn() } catch { return }
    throw new Error('SELF-CHECK: expected a refusal - ' + msg)
  }

  // 1. The real agents parse, and carry exactly the documented field set.
  const files = codexPayloads()
  assert(files.size === AGENTS.length, `parsed ${files.size} agents, expected ${AGENTS.length}`)
  for (const [name, data] of files) {
    const doc = parseAgentToml(data.toString('utf8'))
    assert(doc.name === name.replace(/\.toml$/, ''), `${name}: name mismatch`)
    assert(doc.developer_instructions.length > 200, `${name}: body looks truncated`)
    if (READ_ONLY.has(doc.name)) {
      assert(doc.sandbox_mode === 'read-only', `${doc.name}: lost its read-only sandbox`)
    } else {
      assert(!('sandbox_mode' in doc), `${doc.name}: unexpected sandbox_mode`)
    }
    // A model pin would override the user's session choice - the same decision taken for the
    // Claude agents, and it has to hold on the Codex side too.
    for (const k of ['model', 'model_reasoning_effort', 'tools']) {
      assert(!(k in doc), `${doc.name}: must not pin ${k}`)
    }
  }

  // 2. The TOML reader is strict. A permissive parser is how a malformed agent installs quietly.
  assert(parseAgentToml('a = "x"\n').a === 'x', 'basic string')
  assert(parseAgentToml('a = """\nline\n"""\n').a === 'line\n', 'multiline trims one newline')
  assert(parseAgentToml('# c\n\na = "x"\n').a === 'x', 'comments and blanks')
  assert(parseAgentToml('a = "he said \\"hi\\""\n').a === 'he said "hi"', 'escaped quotes')
  throws(() => parseAgentToml('a = 1\n'), 'a non-string value')
  throws(() => parseAgentToml('a = """unterminated\n'), 'an unterminated block')
  throws(() => parseAgentToml('not a key\n'), 'a junk line')

  // 4. A dry run reports conflicts; it never fails because of the state it is describing.
  //    This regressed once: --dry-run exited 1 on any machine that already had differing agents
  //    installed, which is every machine the feature is useful on.
  const tmp2 = scratchDir('dry')
  mkdirSync(join(tmp2, '.codex', 'agents'), { recursive: true })
  writeFileSync(join(tmp2, '.codex', 'agents', AGENTS[0] + '.toml'), 'name = "conflict"\n')
  const wasDry = DRY
  DRY = true
  const before = out.length
  const realLog = console.log
  console.log = () => {}   // exercising, not installing
  installCodex({ project: tmp2 })                     // must not throw
  assert(out.slice(before).some((l) => l.startsWith('WOULD REFUSE')),
    'a dry run did not report the conflicting agent it found')
  DRY = false
  throws(() => installCodex({ project: tmp2 }), 'a real run over a differing agent')
  console.log = realLog
  DRY = wasDry
  rmSync(tmp2, { recursive: true, force: true })

  // 5. Symlink refusal, on the path and on a parent. This is the property that stops a crafted
  //    ~/.codex/agents link from redirecting writes somewhere else.
  const tmp = scratchDir('links')
  mkdirSync(join(tmp, 'real'), { recursive: true })
  plainPath(join(tmp, 'real'))                       // a plain path is accepted
  let linked = false        // directory links (junctions) - unprivileged on Windows
  let fileLinked = false    // FILE symlinks - need Developer Mode or admin on Windows
  try {
    symlinkSync(join(tmp, 'real'), join(tmp, 'link'), 'junction')
    linked = true
  } catch { /* this platform will not create a directory link; those cases are skipped */ }
  try {
    symlinkSync(join(tmp, 'real', 'nope.txt'), join(tmp, 'flink'), 'file')
    fileLinked = true
  } catch { /* file symlinks are a SEPARATE privilege on Windows - do not assume the junction */ }
  if (linked) {
    throws(() => plainPath(join(tmp, 'link')), 'a symlinked directory')
    throws(() => plainPath(join(tmp, 'link', 'child.toml')), 'a symlinked PARENT')
  }
  rmSync(tmp, { recursive: true, force: true })

  // 6. The flag matrix. Two independent axes, each defaulting to "all" when its own flags are
  //    absent - so a bare run is everything, and one flag from each axis reaches a single cell.
  //    Pinned because an inverted default here silently installs nothing, or installs into a
  //    tool the user explicitly excluded.
  const eq = (a, b) => a.claude === b[0] && a.codex === b[1] && a.skills === b[2] && a.agents === b[3]
  const CASES = [
    [[], [true, true, true, true]],
    [['--claude'], [true, false, true, true]],
    [['--codex'], [false, true, true, true]],
    [['--skills'], [true, true, true, false]],
    [['--agents'], [true, true, false, true]],
    [['--claude', '--skills'], [true, false, true, false]],
    [['--codex', '--agents'], [false, true, false, true]],
    [['--claude', '--agents'], [true, false, false, true]],
    [['--codex', '--skills'], [false, true, true, false]],
  ]
  for (const [flags, want] of CASES) {
    assert(eq(plan(flags), want),
      `flags [${flags.join(' ')}] planned ${JSON.stringify(plan(flags))}, expected `
      + `claude=${want[0]} codex=${want[1]} skills=${want[2]} agents=${want[3]}`)
  }
  // A bare run must reach all four cells, or "one command installs everything" is a lie.
  const bare = plan([])
  assert(bare.claude && bare.codex && bare.skills && bare.agents,
    'the no-flag default no longer installs everything')

  // 7. Uninstall honours the SAME selectors as an install, and preserves what it excluded.
  //    `--claude --uninstall` used to delete Codex agents too, because uninstall was dispatched
  //    before the flags were parsed.
  const tmp3 = scratchDir('uninstall')
  const uHome = join(tmp3, 'home')
  const uSkills = join(uHome, '.claude', 'skills')
  const uAgents = join(uHome, '.claude', 'agents')
  mkdirSync(join(uSkills, SKILLS[0]), { recursive: true })
  mkdirSync(uAgents, { recursive: true })
  writeFileSync(join(uSkills, SKILLS[0], 'SKILL.md'), 'x')
  writeFileSync(join(uAgents, AGENTS[0] + '.md'), 'x')
  writeFileSync(manifestPath(uHome),
    [join(uSkills, SKILLS[0]), join(uAgents, AGENTS[0] + '.md')].join('\n') + '\n')

  const quiet = console.log
  console.log = () => {}
  uninstall(uHome, { project: join(tmp3, 'noproject') },
            { claude: true, codex: false, skills: true, agents: false })
  console.log = quiet
  assert(!existsSync(join(uSkills, SKILLS[0])), '--skills uninstall did not remove the skill')
  assert(existsSync(join(uAgents, AGENTS[0] + '.md')),
    '--skills uninstall removed an AGENT it was told to leave alone')
  const left = readFileSync(manifestPath(uHome), 'utf8')
  assert(left.includes(AGENTS[0] + '.md'), 'the excluded manifest entry was not preserved')
  assert(!left.includes(join(uSkills, SKILLS[0])), 'the removed path is still recorded')

  // ...and the TOOL selector, which needs Codex agents that actually exist: a fixture whose
  // Codex target is missing makes the branch unreachable and the assertion vacuous. That is
  // exactly how the first version of this case passed while the selector was ignored.
  const uProj = join(tmp3, 'proj')
  mkdirSync(join(uProj, '.codex', 'agents'), { recursive: true })
  for (const [n, d] of codexPayloads()) writeFileSync(join(uProj, '.codex', 'agents', n), d)
  console.log = () => {}
  uninstall(uHome, { project: uProj }, { claude: true, codex: false, skills: true, agents: true })
  console.log = quiet
  assert(existsSync(join(uProj, '.codex', 'agents', AGENTS[0] + '.toml')),
    '--claude uninstall deleted CODEX agents it was told to leave alone')
  console.log = () => {}
  uninstall(uHome, { project: uProj }, { claude: false, codex: true, skills: false, agents: true })
  console.log = quiet
  assert(!existsSync(join(uProj, '.codex', 'agents', AGENTS[0] + '.toml')),
    '--codex uninstall did not remove the Codex agents')

  // 8. Removal validates path ancestry the way installation does. A junction on the destination
  //    let a delete follow the link into an unrelated directory: the allowlist compared STRINGS,
  //    and the string was fine.
  if (linked) {
    const ext = join(tmp3, 'external')
    mkdirSync(join(ext, SKILLS[1]), { recursive: true })
    writeFileSync(join(ext, SKILLS[1], 'SKILL.md'), 'outsider')
    const jHome = join(tmp3, 'jhome')
    mkdirSync(join(jHome, '.claude'), { recursive: true })
    symlinkSync(ext, join(jHome, '.claude', 'skills'), 'junction')
    writeFileSync(manifestPath(jHome), join(jHome, '.claude', 'skills', SKILLS[1]) + '\n')
    console.log = () => {}
    uninstall(jHome, { project: join(tmp3, 'noproject') },
              { claude: true, codex: false, skills: true, agents: true })
    console.log = quiet
    assert(existsSync(join(ext, SKILLS[1], 'SKILL.md')),
      'uninstall deleted through a junction, outside the installation location')
  }
  rmSync(tmp3, { recursive: true, force: true })

  // 9. An explicit selector overrides detection. The skip message tells the user to "pass
  //    --claude to install anyway", and for one round passing it changed nothing: detection ran
  //    first and skipped regardless, so the installer printed advice it did not honour.
  const skipMsg = out.filter((l) => typeof l === 'string')
  assert(USAGE.includes('--claude') && USAGE.includes('--codex'), 'usage lost its selectors')
  const src = readFileSync(fileURLToPath(import.meta.url), 'utf8')
  assert(/!found\.claude && !has\('--claude'\)/.test(src),
    'the Claude skip no longer honours an explicit --claude')
  assert(/!opts\.project && !has\('--codex'\)/.test(src),
    'the Codex skip no longer honours an explicit --codex')
  void skipMsg

  // 10. A DANGLING symlink must be refused. existsSync() follows the link, so a link whose
  //     target does not exist yet answered false, the lstat never ran, and the write created the
  //     target THROUGH the link - outside the destination entirely.
  const tmp4 = scratchDir('dangling')
  mkdirSync(join(tmp4, 'agents'), { recursive: true })
  let dangled = false
  try {
    symlinkSync(join(tmp4, 'outside', 'planted.toml'), join(tmp4, 'agents', 'x.toml'), 'file')
    dangled = true
  } catch { /* unprivileged Windows cannot create a file symlink */ }
  if (dangled) {
    assert(!existsSync(join(tmp4, 'agents', 'x.toml')),
      'fixture is wrong - the link is not dangling')
    throws(() => plainPath(join(tmp4, 'agents', 'x.toml')), 'a DANGLING symlink')
    throws(() => write(join(tmp4, 'agents', 'x.toml'), Buffer.from('x')),
      'a write through a dangling symlink')
    assert(!existsSync(join(tmp4, 'outside', 'planted.toml')),
      'the write escaped through the dangling link')
  }
  rmSync(tmp4, { recursive: true, force: true })

  // 11. The manifest reader strips a BOM. Windows PowerShell 5.1 wrote UTF-8 WITH a mark, so a
  //     manifest from the old install-skills.ps1 began "\uFEFFC:\..." - an entry nothing could
  //     match, refused as out-of-allowlist and its skill left orphaned on every uninstall.
  const tmp5 = scratchDir('bom')
  mkdirSync(join(tmp5, '.claude'), { recursive: true })
  const bomEntry = join(tmp5, '.claude', 'skills', SKILLS[0])
  const bomSecond = join(tmp5, '.claude', 'agents', AGENTS[0] + '.md')
  // A mark on the file AND one that reached a later line: the reader strips in two places, so
  // asserting only the first entry let either strip be deleted with the test still passing.
  writeFileSync(manifestPath(tmp5),
                '\uFEFF' + bomEntry + '\r\n' + '\uFEFF' + bomSecond + '\r\n')
  const parsed = readManifest(tmp5)
  assert(parsed.length === 2, `BOM manifest parsed to ${parsed.length} entries`)
  assert(parsed[0] === bomEntry, `BOM survived into the path: ${JSON.stringify(parsed[0])}`)
  assert(parsed[1] === bomSecond, `BOM survived on a later line: ${JSON.stringify(parsed[1])}`)
  assert(owns(tmp5, bomEntry), 'a BOM manifest entry is not recognised as ours')
  rmSync(tmp5, { recursive: true, force: true })

  // 12. Shell execution is win32-only, and only constants may cross it.
  let refusal = null
  try { runCli('codex', ['plugin', 'add', 'x; rm -rf /']) } catch (e) { refusal = e }
  assert(refusal && /Refusing to shell-execute/.test(refusal.message),
    'a non-constant argument was not refused before reaching a shell (got: '
    + (refusal ? refusal.message : 'no error') + ')')

  // 13. Unknown arguments are refused BEFORE anything is written. Ignoring them meant a typo -
  //     or a PowerShell-style -CleanLegacy that INSTALL.md still documented - fell through to a
  //     full default install, the opposite of what was asked for.
  for (const bad of [['-CleanLegacy'], ['-Force'], ['--typo-flag'], ['--claude', '--nope']]) {
    let e = null
    try { validateArgs(bad) } catch (err) { e = err }
    assert(e && /Unknown argument/.test(e.message), `${bad.join(' ')} was not refused`)
  }
  validateArgs([])                                    // must not throw
  validateArgs(['--claude', '--skills', '--dry-run'])
  validateArgs(['--codex', '--project', 'C:\some\path'])   // the value is not an argument

  // 14. A dangling link is SOMETHING, not an empty slot. present() must see it where
  //     existsSync() could not - that gap silently replaced a user's symlinked agent.
  if (fileLinked) {
    const tmp6 = scratchDir('present')
    symlinkSync(join(tmp6, 'no-such-target'), join(tmp6, 'link'), 'file')
    assert(!existsSync(join(tmp6, 'link')), 'fixture wrong - the link is not dangling')
    assert(present(join(tmp6, 'link')), 'present() missed a dangling link')
    assert(!present(join(tmp6, 'genuinely-absent')), 'present() invented a file')
  }

  // 15. The manifest is guarded like any other destination: a SYMLINKED manifest used to be
  //     appended to, writing installed paths into whatever it pointed at.
  if (fileLinked) {
    const tmp7 = scratchDir('manifest')
    mkdirSync(join(tmp7, '.claude'), { recursive: true })
    writeFileSync(join(tmp7, 'external.json'), '{"important":"config"}')
    symlinkSync(join(tmp7, 'external.json'), manifestPath(tmp7), 'file')
    throws(() => claim(tmp7, join(tmp7, '.claude', 'skills', SKILLS[0])),
      'appending to a symlinked manifest')
    throws(() => readManifest(tmp7), 'reading a symlinked manifest')
    assert(readFileSync(join(tmp7, 'external.json'), 'utf8') === '{"important":"config"}',
      'the external file the manifest linked to was modified')
  }

  // 16. scratchDir must CREATE, never adopt. The self-check used five fixed names and rm -rf'd
  //     each before taking ownership, destroying whatever a user or a concurrent run had left
  //     there - silently, while reporting success. The names are deterministic per process, so
  //     the next one can be pre-created and the refusal observed.
  const s1 = scratchDir('collide')
  const seq = Number((s1.match(/-(\d+)-collide$/) || [])[1])
  assert(Number.isInteger(seq), `scratch name is not sequenced: ${s1}`)
  const wouldBe = s1.replace(`-${seq}-collide`, `-${seq + 1}-collide2`)
  // Create the decoy EXCLUSIVELY, and only clean up what this call actually made. The first
  // version used mkdirSync(recursive) then rmSync - so if anything already sat at that path,
  // this test adopted and then deleted it. That is the very bug it exists to catch.
  let decoy = false
  try {
    mkdirSync(wouldBe)
    decoy = true
  } catch (e) {
    if (e.code !== 'EEXIST') throw e
  }
  if (decoy) {
    writeFileSync(join(wouldBe, 'USER-FILE.txt'), 'precious')
    const s2 = scratchDir('collide2')
    assert(s2 !== wouldBe, 'scratchDir adopted a directory it did not create')
    assert(existsSync(join(wouldBe, 'USER-FILE.txt')),
      'scratchDir destroyed a pre-existing directory')
    assert(readdirSync(s2).length === 0, 'scratchDir returned a directory that was not empty')
    rmSync(wouldBe, { recursive: true, force: true })
  }

  // 17. CODEX_HOME must be absolute, tested on the RAW value. The old check called resolve()
  //     first - which always returns an absolute path - so it could never fire, and a relative
  //     value was silently resolved against wherever npx happened to run.
  const prevHome = process.env.CODEX_HOME
  try {
    for (const rel of ['relative-dir', './x', '..', 'a/b']) {
      process.env.CODEX_HOME = rel
      let e = null
      try { codexTarget({ project: null }) } catch (err) { e = err }
      assert(e && /must be an absolute path/.test(e.message),
        `relative CODEX_HOME ${JSON.stringify(rel)} was accepted`)
    }
    process.env.CODEX_HOME = scratchDir('codexhome')
    assert(codexTarget({ project: null }).endsWith('agents'), 'an absolute CODEX_HOME was refused')
  } finally {
    if (prevHome === undefined) delete process.env.CODEX_HOME
    else process.env.CODEX_HOME = prevHome
  }

  // 18. Claude preflights the manifest BEFORE copying. It used to copy, then claim() - so a
  //     symlinked manifest aborted mid-install with files on disk and nothing recording them:
  //     untracked, and invisible to --uninstall forever.
  if (fileLinked) {
    const tmp8 = scratchDir('preflight')
    mkdirSync(join(tmp8, '.claude'), { recursive: true })
    writeFileSync(join(tmp8, 'external.json'), '{"a":1}')
    symlinkSync(join(tmp8, 'external.json'), manifestPath(tmp8), 'file')
    throws(() => installClaude(tmp8, { force: false, skills: true, agents: true }),
      'installing with a symlinked manifest')
    assert(!present(join(tmp8, '.claude', 'skills', SKILLS[0])),
      'a skill was copied before the manifest was validated - it is now untracked')
    assert(readFileSync(join(tmp8, 'external.json'), 'utf8') === '{"a":1}',
      'the linked-to file was modified')
  }

  const skips = [linked ? null : 'directory links', fileLinked ? null : 'file symlinks']
    .filter(Boolean)
  console.log('installer self-check passed'
    + (skips.length ? ` (skipped: this platform would not create ${skips.join(' or ')})` : ''))
  return 0
}

const FLAGS = new Set(['--claude', '--codex', '--skills', '--agents', '--project', '--force',
  '--uninstall', '--clean-legacy', '--dry-run', '--test', '--help', '-h'])

/** Reject anything unrecognised BEFORE a single byte is written.
 *
 *  Unknown arguments used to be ignored, so a typo - or a PowerShell-style `-CleanLegacy` and
 *  `-Force` that INSTALL.md still documented from the installer this replaced - fell straight
 *  through to a full default install. Someone asking to clean legacy paths got an install
 *  instead, which is the opposite of a no-op.
 */
function validateArgs(argv) {
  const pi = argv.indexOf('--project')
  const unknown = argv.filter((a, i) => {
    if (pi >= 0 && i === pi + 1) return false        // the value of --project
    return !FLAGS.has(a)
  })
  if (!unknown.length) return
  const hint = unknown.some((a) => /^-[A-Z]/.test(a))
    ? '\n  PowerShell-style flags (-Force, -Uninstall, -CleanLegacy, -ClaudeHome) belonged to'
      + '\n  install-skills.ps1, which this replaced. Use the double-dash forms below.'
    : ''
  fail(`Unknown argument(s): ${unknown.join(' ')}${hint}\n`
    + `  Valid flags: ${[...FLAGS].join(' ')}\n`
    + '  Nothing was installed. Run with --help for the full list.')
}

/** Two independent axes, each defaulting to "all" when its own flags are absent.
 *
 *  So a bare run is everything, --claude is both kinds for Claude, and one flag from each axis
 *  reaches a single cell. Defined once and shared with the self-check: a copy in the test would
 *  assert the copy, which is the drift this repo's CI exists to catch.
 */
function plan(argv) {
  const has = (f) => argv.includes(f)
  return {
    claude: has('--claude') || !has('--codex'),
    codex: has('--codex') || !has('--claude'),
    skills: has('--skills') || !has('--agents'),
    agents: has('--agents') || !has('--skills'),
  }
}

// --- entry --------------------------------------------------------------------

async function main(argv) {
  validateArgs(argv)   // before ANY mutation
  const has = (f) => argv.includes(f)
  DRY = has('--dry-run')
  const pi = argv.indexOf('--project')
  const opts = { project: pi >= 0 ? argv[pi + 1] : null, force: has('--force') }
  if (pi >= 0 && (!opts.project || opts.project.startsWith('--'))) fail('--project needs a path')
  const home = process.env.DGA_KIT_HOME || homedir()

  if (has('--help') || has('-h')) { console.log(USAGE); return 0 }
  if (has('--test')) return selfTest()
  if (has('--clean-legacy')) return cleanLegacy(home)
  // Selectors are parsed BEFORE this dispatch: uninstall honours exactly the same plan an
  // install would, and used to ignore them entirely.
  if (has('--uninstall')) return uninstall(home, opts, plan(argv))

  // Two independent axes, each defaulting to "all" when its own flags are absent. So bare
  // `npx ...` is everything, `--claude` is both kinds for Claude, `--codex --skills` is one cell.
  const { claude: wantClaude, codex: wantCodex,
          skills: wantSkills, agents: wantAgents } = plan(argv)

  const found = detect(home)
  say(`Detected: Claude Code ${found.claude ? 'yes' : 'no'} · `
    + `Codex ${found.codexHome || found.codexCli ? 'yes' : 'no'}`
    + `${found.codexCli ? '' : ' (CLI not callable)'}`)
  say('')

  let version = ''
  try {
    version = JSON.parse(readFileSync(join(ROOT, '.claude-plugin', 'plugin.json'), 'utf8')).version || ''
  } catch { /* version is a nicety, never a reason to fail an install */ }

  const skipped = []
  let bad = 0, did = 0, codexSkillsFailed = false

  // An EXPLICIT selector overrides detection. Detection decides what a bare run does; a flag is
  // the user saying "yes, this one" - and the skip message promised exactly that while the code
  // ignored it, so `--claude` on a machine with no ~/.claude yet installed nothing and told the
  // user to pass the flag they had just passed.
  if (wantClaude && !found.claude && !has('--claude')) {
    skipped.push('Claude Code - no ~/.claude and no `claude` on PATH. Pass --claude to install anyway.')
  } else if (wantClaude) {
    const { ok, aok, dest } = installClaude(home, { ...opts, skills: wantSkills, agents: wantAgents })
    did += ok + aok
    say('')
    say(`Claude Code: ${ok} skill(s), ${aok} agent(s).${version ? ` dga-kit ${version}` : ''}`)
    say(`manifest: ${manifestPath(home)} - uninstall removes only what is listed there`)
    if (DRY) say('cross-references not checked (dry run installs nothing to check)')
    else if (wantSkills) {
      bad = verify(dest)
      say(bad === 0 ? 'cross-references OK' : `${bad} unresolvable reference(s) - report this as a bug`)
    }
  }

  if (wantCodex && wantAgents) {
    if (!found.codexHome && !found.codexCli && !opts.project && !has('--codex')) {
      skipped.push('Codex agents - no ~/.codex and no `codex` on PATH. Pass --codex to install anyway.')
    } else {
      say('')
      did += installCodex(opts)
    }
  }

  if (wantCodex && wantSkills) {
    say('')
    if (!found.codexCli) {
      skipped.push('Codex skills - the `codex` CLI is not callable, and Codex serves plugin '
        + 'skills from its own cache + config.toml, not from a directory. Install the CLI, then:\n'
        + '    codex plugin marketplace add mohamedsamy911/dga-kit\n'
        + '    codex plugin add dga-kit@dga-kit')
    } else if (installCodexSkills({ dryRun: DRY }) === 'failed') {
      codexSkillsFailed = true
    }
  }

  if (skipped.length) {
    say('')
    say('Skipped:')
    for (const s of skipped) say(`  - ${s}`)
  }
  say('')
  // Never say "Done" over a failure. The closing line is the only thing most people read.
  if (DRY) say('Dry run - nothing was written.')
  else if (codexSkillsFailed || bad) say('FINISHED WITH ERRORS - see above. Some of this kit is NOT installed.')
  else say('Done. Restart Claude Code, and start a new Codex session.')
  // A failed Codex plugin install is a failed run. It used to exit 0.
  return (bad === 0 && !codexSkillsFailed) ? 0 : 1
}

main(process.argv.slice(2))
  .then((c) => { process.exitCode = c })
  .catch((e) => {
    console.error(`ERROR: ${e.expected ? e.message : e.stack}`)
    process.exitCode = 1
  })
