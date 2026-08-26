#!/usr/bin/env bash
# Installs dga-kit skills + agents into ~/.claude (macOS / Linux / WSL).
# Only needed if you are NOT installing via the plugin marketplace - see INSTALL.md.
#   ./install-skills.sh             install
#   ./install-skills.sh --force     overwrite existing
#   ./install-skills.sh --uninstall remove
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/skills"; ASRC="$ROOT/agents"
DEST="$HOME/.claude/skills"; ADEST="$HOME/.claude/agents"

SKILLS=(dga-design-system dga-design-review dga-react dga-ui-adapter dga-rtl-i18n
        dga-handoff dga-mockup dga-a11y dga-launch-gate dga-tokens-sync dga-brand-overlay)
# Every agent is dga- prefixed, so nothing here can collide with an agent of yours.
AGENTS=(dga-designer dga-frontend-architect dga-frontend-dev dga-code-reviewer
        dga-compliance-auditor dga-content-writer)
# Renamed/removed in 0.5.0. Cleared on install too, or the stale copy keeps firing.
LEGACY_SKILLS=(dga-chakra rga-brand)
LEGACY_AGENTS=(designer frontend-dev)

clear_legacy() {
  for n in "${LEGACY_SKILLS[@]}"; do
    [[ -d "$DEST/$n" ]] && rm -rf "$DEST/$n" && echo "removed   legacy skill $n"
  done
  # Never auto-remove these - the names are generic and the file may well be yours.
  for a in "${LEGACY_AGENTS[@]}"; do
    if [[ -f "$ADEST/$a.md" ]] && grep -qF '_shared/dga.md' "$ADEST/$a.md" 2>/dev/null; then
      echo "note      $ADEST/$a.md looks like dga-kit <=0.4 (references _shared/dga.md)."
      echo "          It is superseded by dga-$a.md - delete it by hand if it is not yours."
    fi
  done
  [[ -d "$ADEST/_shared" ]] && echo "note      $ADEST/_shared/ is from dga-kit <=0.4 and no longer used." 
}

if [[ "${1:-}" == "--uninstall" ]]; then
  clear_legacy
  for n in "${SKILLS[@]}"; do
    [[ -d "$DEST/$n" ]] && rm -rf "$DEST/$n" && echo "removed   skill $n"
  done
  for a in "${AGENTS[@]}"; do
    [[ -f "$ADEST/$a.md" ]] && rm -f "$ADEST/$a.md" && echo "removed   agent $a"
  done
  echo; echo "Uninstalled. Restart Claude Code."; exit 0
fi

[[ -d "$SRC" ]] || { echo "skills/ not found - run this from inside the dga-kit folder." >&2; exit 1; }
mkdir -p "$DEST" "$ADEST"
clear_legacy

ok=0
for n in "${SKILLS[@]}"; do
  if [[ ! -f "$SRC/$n/SKILL.md" ]]; then echo "skipped   $n (no SKILL.md)"; continue; fi
  if [[ -d "$DEST/$n" && "${1:-}" != "--force" ]]; then echo "exists    $n (use --force)"; continue; fi
  rm -rf "$DEST/$n"; cp -R "$SRC/$n" "$DEST/$n"
  ok=$((ok+1)); echo "installed skill $n"
done

aok=0
for a in "${AGENTS[@]}"; do
  if [[ ! -f "$ASRC/$a.md" ]]; then echo "skipped   $a (missing)"; continue; fi
  if [[ -f "$ADEST/$a.md" && "${1:-}" != "--force" ]]; then echo "exists    $a (use --force)"; continue; fi
  cp "$ASRC/$a.md" "$ADEST/$a.md"; aok=$((aok+1)); echo "installed agent $a"
done

# Skills reference each other as siblings (../dga-design-system/...), so the flat layout
# is required. Verify every relative link resolves where it landed. One grep pass - a
# per-file loop is painfully slow on Windows/Git Bash.
bad=0
while IFS= read -r line; do
  # split on the LAST colon - a Windows path can carry a drive-letter colon of its own
  f="${line%:*}"; ref="${line##*:}"
  [[ -e "${f%/*}/$ref" ]] || { echo "BROKEN    $f -> $ref"; bad=$((bad+1)); }
done < <(for n in "${SKILLS[@]}"; do [[ -d "$DEST/$n" ]] && echo "$DEST/$n"; done          | xargs -r grep -rHoE '\.\./[A-Za-z0-9_./-]+\.(md|json|css|mjs|js|ts)' --include='*.md'          | sort -u)

echo
echo "$ok skill(s), $aok agent(s) installed."
[[ $bad -eq 0 ]] && echo "cross-references OK" || echo "$bad broken cross-reference(s) - report this as a bug"
echo "Restart Claude Code, then run /skills to confirm."
