<#
  Installs dga-kit skills + agents into %USERPROFILE%\.claude, making them available in every
  project. Only needed if you are NOT installing via the plugin marketplace - see INSTALL.md.

    powershell -ExecutionPolicy Bypass -File .\install-skills.ps1
    powershell -ExecutionPolicy Bypass -File .\install-skills.ps1 -ClaudeHome D:\scratch
    powershell -ExecutionPolicy Bypass -File .\install-skills.ps1 -Force
    powershell -ExecutionPolicy Bypass -File .\install-skills.ps1 -Uninstall
    powershell -ExecutionPolicy Bypass -File .\install-skills.ps1 -CleanLegacy

  -Force overwrites an existing dga-* path AND adopts one that is not in the manifest (it prints
  OVERWRITE for each). That is how a pre-0.5.1 install is upgraded. It only ever writes to
  allowlisted dga-* names.

  OWNERSHIP. A path is deleted only if BOTH hold:
    1. it is recorded in the manifest, and
    2. it matches the fixed allowlist - skills\<one of $skills> or agents\<one of $agents>.md
  The manifest is editable text, so it is treated as a record and not as an authority; condition
  2 is what makes a corrupted manifest harmless. Nothing is ever removed by name alone, and a
  path the manifest does not claim is treated as YOURS and left untouched.
#>
# -ClaudeHome exists so this script can be TESTED. It defaults to $HOME and you should not pass
# it by hand. PowerShell's $HOME is ReadOnly+AllScope, so a test harness cannot redirect the
# install by assigning it, and $env:USERPROFILE does not feed $HOME either - which meant CI had no
# way to run this script without writing into the real profile. A parameter is the honest fix: the
# destination becomes an input instead of an ambient fact.
param([switch]$Uninstall, [switch]$Force, [switch]$CleanLegacy,
      [string]$ClaudeHome = $HOME)

if ([string]::IsNullOrWhiteSpace($ClaudeHome)) { throw '-ClaudeHome cannot be empty' }

$ErrorActionPreference = 'Stop'
$src      = Join-Path $PSScriptRoot 'skills'
$dest     = Join-Path $ClaudeHome '.claude\skills'
$asrc     = Join-Path $PSScriptRoot 'agents'
$adest    = Join-Path $ClaudeHome '.claude\agents'
$manifest = Join-Path $ClaudeHome '.claude\.dga-kit-manifest'

$skills = @('dga-design-system','dga-design-review','dga-react','dga-ui-adapter','dga-rtl-i18n',
            'dga-handoff','dga-mockup','dga-a11y','dga-launch-gate','dga-tokens-sync',
            'dga-brand-overlay')
# Every agent is dga- prefixed, so nothing here can collide with an agent of yours.
$agents = @('dga-designer','dga-frontend-architect','dga-frontend-dev','dga-code-reviewer',
            'dga-compliance-auditor','dga-content-writer')
# Renamed or removed in 0.5.0. NEVER deleted automatically - see -CleanLegacy.
$legacySkills = @('dga-chakra','rga-brand')
$legacyAgents = @('designer','frontend-dev')

function Get-Owned {
    if (Test-Path -LiteralPath $manifest) { return @(Get-Content -LiteralPath $manifest) }
    return @()
}
function Test-Owned([string]$p) { return (Get-Owned) -contains $p }
function Add-Claim([string]$p) {
    if (-not (Test-Owned $p)) { Add-Content -LiteralPath $manifest -Value $p -Encoding utf8 }
}

function Show-LegacyNotice {
    $found = $false
    foreach ($n in $legacySkills) {
        $p = Join-Path $dest $n
        if (Test-Path -LiteralPath $p) {
            Write-Host "note      $p is from dga-kit <=0.4 and is no longer used."; $found = $true
        }
    }
    foreach ($a in $legacyAgents) {
        $p = Join-Path $adest "$a.md"
        if (Test-Path -LiteralPath $p) {
            $t = Get-Content -LiteralPath $p -Raw
            if (-not [string]::IsNullOrEmpty($t) -and $t -match '_shared/dga\.md') {
                Write-Host "note      $p looks like dga-kit <=0.4; superseded by dga-$a.md."; $found = $true
            }
        }
    }
    if (Test-Path -LiteralPath (Join-Path $adest '_shared')) {
        Write-Host "note      $adest\_shared\ is from dga-kit <=0.4."; $found = $true
    }
    if ($found) { Write-Host "          Nothing was deleted. Review, then use -CleanLegacy or remove by hand." }
}

if ($CleanLegacy) {
    $targets = @()
    foreach ($n in $legacySkills) {
        $p = Join-Path $dest $n
        if (Test-Path -LiteralPath $p) { $targets += $p }
    }
    $sharedDir = Join-Path $adest '_shared'
    if (Test-Path -LiteralPath $sharedDir) { $targets += $sharedDir }
    if ($targets.Count -eq 0) { Write-Host 'No pre-0.5 paths found.'; exit 0 }
    Write-Host 'These paths will be PERMANENTLY DELETED:'
    foreach ($p in $targets) { Write-Host "  $p" }
    Write-Host ''
    Write-Host 'dga-kit cannot prove it created these - a skill of your own may share a name.'
    $reply = Read-Host 'Type DELETE to confirm'
    if ($reply -ne 'DELETE') { Write-Host 'Aborted. Nothing removed.'; exit 1 }
    foreach ($p in $targets) { Remove-Item -LiteralPath $p -Recurse -Force; Write-Host "removed   $p" }
    Write-Host 'Legacy agent .md files were NOT touched - those names are generic. Remove by hand if yours.'
    exit 0
}

if ($Uninstall) {
    if (-not (Test-Path -LiteralPath $manifest)) {
        Write-Host "No manifest at $manifest - this installer has no record of installing anything." -ForegroundColor Yellow
        Write-Host 'Refusing to delete by name. Remove paths by hand if you are sure they are ours.' -ForegroundColor Yellow
        exit 1
    }
    # The manifest is a plain text file a user (or a bug) can edit. It is a record, NOT an
    # authority: every entry is checked against the fixed allowlist below before deletion, so a
    # corrupted manifest can at worst under-delete, never delete something unrelated.
    $allowed = @()
    foreach ($n in $skills) { $allowed += (Join-Path $dest $n) }
    foreach ($a in $agents) { $allowed += (Join-Path $adest "$a.md") }

    $removed = 0; $refused = 0
    foreach ($p in (Get-Owned)) {
        if ([string]::IsNullOrWhiteSpace($p)) { continue }
        if ($allowed -notcontains $p) {
            Write-Host "REFUSED   $p - in the manifest but not a path this kit can create. Left untouched." -ForegroundColor Yellow
            $refused++; continue
        }
        if (Test-Path -LiteralPath $p) {
            Remove-Item -LiteralPath $p -Recurse -Force; Write-Host "removed   $p"; $removed++
        }
    }
    Remove-Item -LiteralPath $manifest -Force
    Write-Host "`n$removed path(s) removed - only those this installer recorded AND could have created." -ForegroundColor Green
    if ($refused -gt 0) {
        Write-Host "$refused manifest entry/entries refused as out-of-allowlist - remove them by hand if they are yours." -ForegroundColor Yellow
    }
    Write-Host 'Restart Claude Code.'
    exit 0
}

if (-not (Test-Path -LiteralPath $src)) {
    Write-Error 'skills\ not found - run this from inside the dga-kit folder.'; exit 1
}
New-Item -ItemType Directory -Force -Path $dest, $adest | Out-Null
Show-LegacyNotice

$ok = 0
foreach ($n in $skills) {
    $s = Join-Path $src $n
    $d = Join-Path $dest $n
    if (-not (Test-Path -LiteralPath (Join-Path $s 'SKILL.md'))) { Write-Host "skipped   $n (no SKILL.md)"; continue }
    if ((Test-Path -LiteralPath $d) -and -not (Test-Owned $d)) {
        # Not in the manifest. Either it is yours, or it predates manifests (dga-kit <= 0.5.0).
        if ($Force) { Write-Host "OVERWRITE $n - not in manifest, -Force given" }
        else {
            Write-Host "SKIPPED   $n - exists and is not in our manifest. Left untouched."
            Write-Host '          If it is an older dga-kit, re-run with -Force to adopt it.'
            continue
        }
    }
    elseif ((Test-Path -LiteralPath $d) -and -not $Force) { Write-Host "exists    $n (use -Force)"; continue }
    if (Test-Path -LiteralPath $d) { Remove-Item -LiteralPath $d -Recurse -Force }
    Copy-Item -LiteralPath $s -Destination $d -Recurse
    Add-Claim $d
    $ok++; Write-Host "installed skill $n"
}

$aok = 0
foreach ($a in $agents) {
    $s = Join-Path $asrc "$a.md"
    $d = Join-Path $adest "$a.md"
    if (-not (Test-Path -LiteralPath $s)) { Write-Host "skipped   $a (missing)"; continue }
    if ((Test-Path -LiteralPath $d) -and -not (Test-Owned $d)) {
        if ($Force) { Write-Host "OVERWRITE $a - not in manifest, -Force given" }
        else {
            Write-Host "SKIPPED   $a - exists and is not in our manifest. Left untouched."
            Write-Host '          If it is an older dga-kit, re-run with -Force to adopt it.'
            continue
        }
    }
    elseif ((Test-Path -LiteralPath $d) -and -not $Force) { Write-Host "exists    $a (use -Force)"; continue }
    Copy-Item -LiteralPath $s -Destination $d -Force
    Add-Claim $d
    $aok++; Write-Host "installed agent $a"
}

# Skills reference each other as siblings (../dga-design-system/...), so the flat layout is
# required. Verify every relative link resolves where it landed.
$bad = 0
$installed = $skills | ForEach-Object { Join-Path $dest $_ } | Where-Object { Test-Path -LiteralPath $_ }
foreach ($f in ($installed | Get-ChildItem -Recurse -Filter *.md -File)) {
    $text = Get-Content -LiteralPath $f.FullName -Raw
    if ([string]::IsNullOrEmpty($text)) { continue }
    foreach ($m in [regex]::Matches($text, '\.\./[A-Za-z0-9_./-]+\.(md|json|css|mjs|js|ts)')) {
        $target = Join-Path $f.DirectoryName $m.Value
        if (-not (Test-Path -LiteralPath $target)) {
            Write-Host "BROKEN    $($f.FullName) -> $($m.Value)" -ForegroundColor Yellow
            $bad++
        }
    }
}

# Repo-root paths die on install too - harvest\, evals\, COVERAGE.md are not copied to
# ~/.claude. A full GitHub URL is exempt; it resolves from anywhere.
foreach ($f in ($installed | Get-ChildItem -Recurse -Include *.md, *.json -File)) {
    $text = Get-Content -LiteralPath $f.FullName -Raw
    if ([string]::IsNullOrEmpty($text)) { continue }
    # Validate each match locally. Only a canonical GitHub blob URL or a raw.githubusercontent
    # URL exempts an occurrence; exempting anything preceded by "/" would wave through a dead
    # /harvest/... path. Fenced code blocks are stripped first - a shell command is not a link.
    $text = ($text -split "`n" | ForEach-Object -Begin { $fence = $false } -Process {
        if ($_ -match '^```') { $fence = -not $fence } elseif (-not $fence) { $_ }
    }) -join "`n"
    $okUrl = '(?:https://github\.com/mohamedsamy911/dga-kit/blob/[A-Za-z0-9._-]+/|https://raw\.githubusercontent\.com/mohamedsamy911/dga-kit/[A-Za-z0-9._-]+/)$'
    foreach ($m in [regex]::Matches($text, '(?:harvest|evals)/[A-Za-z0-9_./-]+|COVERAGE\.md|README\.md|AGENTS\.md')) {
        if ($text.Substring(0, $m.Index) -match $okUrl) { continue }
        Write-Host "UNSHIPPED $($f.FullName) -> $($m.Value) (not installed; use a full GitHub URL)" -ForegroundColor Yellow
        $bad++
    }
}

Write-Host "`n$ok skill(s), $aok agent(s) installed."
Write-Host "manifest: $manifest - uninstall removes only what is listed there"
if ($bad -eq 0) { Write-Host 'cross-references OK' -ForegroundColor Green }
else { Write-Host "$bad unresolvable reference(s) - report this as a bug" -ForegroundColor Yellow }
Write-Host 'Restart Claude Code, then run /skills to confirm.'
