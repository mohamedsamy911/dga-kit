#!/usr/bin/env bash
# Installs dga-kit skills + agents into ~/.claude (macOS / Linux / WSL).
# Only needed if you are NOT installing via the plugin marketplace - see INSTALL.md.
#
#   ./install-skills.sh                install
#   ./install-skills.sh --force        overwrite an existing dga-* path, AND adopt one that is
#                                      not in the manifest (prints OVERWRITE for each)
#   ./install-skills.sh --uninstall    remove only what this kit installed
#   ./install-skills.sh --clean-legacy remove pre-0.5 paths, listing each and confirming first
#
# OWNERSHIP. A path is deleted only if BOTH hold:
#   1. it is recorded in the manifest ($MANIFEST), and
#   2. it matches the fixed allowlist - skills/<one of SKILLS> or agents/<one of AGENTS>.md
# The manifest is editable text, so it is treated as a record and not as an authority; condition
# 2 is what makes a corrupted manifest harmless. Nothing is ever removed by name alone, and a
# path the manifest does not claim is treated as YOURS.
#
# --force is the one place that touches an unclaimed path: it adopts it (that is how a pre-0.5.1
# install is upgraded). It still only ever writes to allowlisted dga-* names, and announces each
# one. It never deletes anything outside those names.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/skills"; ASRC="$ROOT/agents"
DEST="$HOME/.claude/skills"; ADEST="$HOME/.claude/agents"
MANIFEST="$HOME/.claude/.dga-kit-manifest"
VERSION="$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$ROOT/.claude-plugin/plugin.json" 2>/dev/null || true)"

SKILLS=(dga-design-system dga-design-review dga-react dga-ui-adapter dga-rtl-i18n
        dga-handoff dga-mockup dga-a11y dga-launch-gate dga-tokens-sync dga-brand-overlay)
# Every agent is dga- prefixed, so nothing here can collide with an agent of yours.
AGENTS=(dga-designer dga-frontend-architect dga-frontend-dev dga-code-reviewer
        dga-compliance-auditor dga-content-writer)
# Renamed or removed in 0.5.0. NEVER deleted automatically - see --clean-legacy.
LEGACY_SKILLS=(dga-chakra rga-brand)
LEGACY_AGENTS=(designer frontend-dev)

owns()  { [[ -f "$MANIFEST" ]] && grep -qxF "$1" "$MANIFEST"; }
claim() { mkdir -p "$(dirname "$MANIFEST")"; touch "$MANIFEST"
          grep -qxF "$1" "$MANIFEST" 2>/dev/null || printf '%s\n' "$1" >> "$MANIFEST"; }

legacy_notice() {
  local found=0
  for n in "${LEGACY_SKILLS[@]}"; do
    [[ -d "$DEST/$n" ]] && { echo "note      $DEST/$n is from dga-kit <=0.4 and is no longer used."; found=1; }
  done
  for a in "${LEGACY_AGENTS[@]}"; do
    if [[ -f "$ADEST/$a.md" ]] && grep -qF '_shared/dga.md' "$ADEST/$a.md" 2>/dev/null; then
      echo "note      $ADEST/$a.md looks like dga-kit <=0.4; superseded by dga-$a.md."; found=1
    fi
  done
  [[ -d "$ADEST/_shared" ]] && { echo "note      $ADEST/_shared/ is from dga-kit <=0.4."; found=1; }
  [[ $found -eq 1 ]] && echo "          Nothing was deleted. Review, then use --clean-legacy or remove by hand."
  return 0
}

if [[ "${1:-}" == "--clean-legacy" ]]; then
  targets=()
  for n in "${LEGACY_SKILLS[@]}"; do [[ -d "$DEST/$n" ]] && targets+=("$DEST/$n"); done
  [[ -d "$ADEST/_shared" ]] && targets+=("$ADEST/_shared")
  if [[ ${#targets[@]} -eq 0 ]]; then echo "No pre-0.5 paths found."; exit 0; fi
  echo "These paths will be PERMANENTLY DELETED:"
  for p in "${targets[@]}"; do echo "  $p"; done
  echo
  echo "dga-kit cannot prove it created these - a skill of your own may share a name."
  read -r -p "Type DELETE to confirm: " reply < /dev/tty
  [[ "$reply" == "DELETE" ]] || { echo "Aborted. Nothing removed."; exit 1; }
  for p in "${targets[@]}"; do rm -rf "$p"; echo "removed   $p"; done
  echo "Legacy agent .md files were NOT touched - those names are generic. Remove by hand if yours."
  exit 0
fi

if [[ "${1:-}" == "--uninstall" ]]; then
  if [[ ! -f "$MANIFEST" ]]; then
    echo "No manifest at $MANIFEST - this installer has no record of installing anything." >&2
    echo "Refusing to delete by name. Remove paths by hand if you are sure they are ours." >&2
    exit 1
  fi
  # The manifest is a plain text file a user (or a bug) can edit. It is a record, NOT an
  # authority: every entry is checked against the fixed allowlist below before deletion, so a
  # corrupted manifest can at worst under-delete, never delete something unrelated.
  allowed=()
  for n in "${SKILLS[@]}"; do allowed+=("$DEST/$n"); done
  for a in "${AGENTS[@]}"; do allowed+=("$ADEST/$a.md"); done
  is_allowed() { local q="$1" x; for x in "${allowed[@]}"; do [[ "$x" == "$q" ]] && return 0; done; return 1; }

  removed=0; refused=0
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    if ! is_allowed "$p"; then
      echo "REFUSED   $p - in the manifest but not a path this kit can create. Left untouched."
      refused=$((refused+1)); continue
    fi
    [[ -e "$p" ]] && { rm -rf "$p"; echo "removed   $p"; removed=$((removed+1)); }
  done < "$MANIFEST"
  rm -f "$MANIFEST"
  echo; echo "$removed path(s) removed - only those this installer recorded AND could have created."
  [[ $refused -gt 0 ]] && echo "$refused manifest entry/entries refused as out-of-allowlist - remove them by hand if they are yours."
  echo "Restart Claude Code."
  exit 0
fi

[[ -d "$SRC" ]] || { echo "skills/ not found - run this from inside the dga-kit folder." >&2; exit 1; }
mkdir -p "$DEST" "$ADEST"
legacy_notice

ok=0
for n in "${SKILLS[@]}"; do
  d="$DEST/$n"
  if [[ ! -f "$SRC/$n/SKILL.md" ]]; then echo "skipped   $n (no SKILL.md)"; continue; fi
  if [[ -d "$d" ]] && ! owns "$d"; then
    # Not in the manifest. Either it is yours, or it predates manifests (dga-kit <= 0.5.0).
    # Default to leaving it alone; --force is the explicit override.
    if [[ "${1:-}" == "--force" ]]; then
      echo "OVERWRITE $n - not in manifest, --force given"
    else
      echo "SKIPPED   $n - exists and is not in our manifest. Left untouched."
      echo "          If it is an older dga-kit, re-run with --force to adopt it."; continue
    fi
  elif [[ -d "$d" && "${1:-}" != "--force" ]]; then
    echo "exists    $n (use --force)"; continue
  fi
  rm -rf "$d"; cp -R "$SRC/$n" "$d"; claim "$d"
  ok=$((ok+1)); echo "installed skill $n"
done

aok=0
for a in "${AGENTS[@]}"; do
  d="$ADEST/$a.md"
  if [[ ! -f "$ASRC/$a.md" ]]; then echo "skipped   $a (missing)"; continue; fi
  if [[ -f "$d" ]] && ! owns "$d"; then
    if [[ "${1:-}" == "--force" ]]; then
      echo "OVERWRITE $a - not in manifest, --force given"
    else
      echo "SKIPPED   $a - exists and is not in our manifest. Left untouched."
      echo "          If it is an older dga-kit, re-run with --force to adopt it."; continue
    fi
  elif [[ -f "$d" && "${1:-}" != "--force" ]]; then
    echo "exists    $a (use --force)"; continue
  fi
  cp "$ASRC/$a.md" "$d"; claim "$d"; aok=$((aok+1)); echo "installed agent $a"
done

# Skills reference each other as siblings (../dga-design-system/...), so the flat layout
# is required. Verify every relative link resolves where it landed. One grep pass - a
# Run a command over the installed skill directories, or not at all when none exist.
#
# This replaced `... | xargs -r`. `-r` (do not run on empty input) is a GNU extension: BSD xargs
# on macOS rejects it outright, so on the platform this script advertises support for, both
# cross-reference checks died with a usage error - and `set -euo pipefail` turned that into a
# silent skip rather than a visible failure. Passing the paths as arguments removes the need for
# either flag.
scan_dirs() {
  local cmd=("$@") dirs=() n
  for n in "${SKILLS[@]}"; do [[ -d "$DEST/$n" ]] && dirs+=("$DEST/$n"); done
  (( ${#dirs[@]} )) || return 0
  "${cmd[@]}" "${dirs[@]}"
}

# per-file loop is painfully slow on Windows/Git Bash.
bad=0
while IFS= read -r line; do
  # split on the LAST colon - a Windows path can carry a drive-letter colon of its own
  f="${line%:*}"; ref="${line##*:}"
  [[ -e "${f%/*}/$ref" ]] || { echo "BROKEN    $f -> $ref"; bad=$((bad+1)); }
done < <(scan_dirs grep -rHoE '\.\./[A-Za-z0-9_./-]+\.(md|json|css|mjs|js|ts)' --include='*.md' \
         | sort -u)

# Repo-root paths are the other way a reference dies on install. harvest/, evals/, COVERAGE.md
# and friends are NOT copied to ~/.claude, so a skill naming one reads fine in the repo and is a
# dead end for every installed user. Full GitHub URLs are exempt - they resolve from anywhere.
while IFS= read -r line; do
  f="${line%:*}"; ref="${line##*:}"
  # Count, do not just test: a file may carry one correct GitHub URL AND a bare mention of the
  # same path. Only two forms are exempt - a canonical GitHub blob URL and a raw.githubusercontent
  # URL. Exempting anything merely preceded by "/" would wave through a dead /harvest/... path.
  #
  # Shell commands in fenced code blocks are not references, so the fences are stripped first;
  # a maintainer running `python3 evals/...` from a clone is not a broken link.
  #
  # `|| x=0` is load-bearing: this script runs under `set -euo pipefail`, and a grep that matches
  # nothing exits 1, which pipefail propagates through `| wc -l` and set -e turns into a silent
  # death mid-verify. That is exactly what happened when this check was first written.
  body=$(awk '/^```/{fence=!fence; next} !fence' "$f")
  total=$(printf '%s\n' "$body" | grep -oF "$ref" | wc -l) || total=0
  linked=0
  # $ref lands inside an ERE, so its dots would match any character: a malformed URL like
  # ".../blob/master/COVERAGEXmd" would then exempt a genuinely dead COVERAGE.md reference.
  # Refs are drawn from [A-Za-z0-9_./-]+, so "." is the only ERE metacharacter they can contain.
  ref_re=${ref//./\\.}
  for pre in "https://github.com/mohamedsamy911/dga-kit/blob/" \
             "https://raw.githubusercontent.com/mohamedsamy911/dga-kit/"; do
    n=$(printf '%s\n' "$body" | grep -oE "${pre//./\\.}[A-Za-z0-9._-]+/$ref_re" | wc -l) || n=0
    linked=$((linked + n))
  done
  bare=$((total - linked))
  [[ $bare -le 0 ]] && continue
  echo "UNSHIPPED $f -> $ref x$bare (not installed; use a full GitHub URL)"; bad=$((bad+1))
done < <(scan_dirs grep -rHoE '(harvest|evals)/[A-Za-z0-9_./-]+|COVERAGE\.md|README\.md|AGENTS\.md|CHANGELOG\.md' --include='*.md' --include='*.json' \
         | sort -u)

echo
echo "$ok skill(s), $aok agent(s) installed.${VERSION:+ dga-kit $VERSION}"
echo "manifest: $MANIFEST - uninstall removes only what is listed there"
echo "Restart Claude Code, then run /skills to confirm."

# Exit non-zero when the installed tree has dangling references. It used to print the warning and
# exit 0, so only a caller grepping the log could tell - a person installing by hand, or any
# automation checking the exit status, read a broken layout as success.
if [[ $bad -eq 0 ]]; then
  echo "cross-references OK"
else
  echo "$bad unresolvable reference(s) - report this as a bug"
  exit 1
fi
