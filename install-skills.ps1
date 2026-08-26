<#
  Installs dga-kit skills + agents into %USERPROFILE%\.claude, making them available in every
  project. Only needed if you are NOT installing via the plugin marketplace - see INSTALL.md.

    powershell -ExecutionPolicy Bypass -File .\install-skills.ps1
    powershell -ExecutionPolicy Bypass -File .\install-skills.ps1 -Force
    powershell -ExecutionPolicy Bypass -File .\install-skills.ps1 -Uninstall
#>
param([switch]$Uninstall, [switch]$Force)

$ErrorActionPreference = 'Stop'
$src   = Join-Path $PSScriptRoot 'skills'
$dest  = Join-Path $HOME '.claude\skills'
$asrc  = Join-Path $PSScriptRoot 'agents'
$adest = Join-Path $HOME '.claude\agents'

$skills = @('dga-design-system','dga-design-review','dga-react','dga-ui-adapter','dga-rtl-i18n',
            'dga-handoff','dga-mockup','dga-a11y','dga-launch-gate','dga-tokens-sync',
            'dga-brand-overlay')
# Every agent is dga- prefixed, so nothing here can collide with an agent of yours.
$agents = @('dga-designer','dga-frontend-architect','dga-frontend-dev','dga-code-reviewer',
            'dga-compliance-auditor','dga-content-writer')
# Renamed/removed in 0.5.0. Cleared on install too, or the stale copy keeps firing.
$legacySkills = @('dga-chakra','rga-brand')
$legacyAgents = @('designer','frontend-dev')

function Clear-Legacy {
    foreach ($n in $legacySkills) {
        $p = Join-Path $dest $n
        if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Recurse -Force; Write-Host "removed   legacy skill $n" }
    }
    # Never auto-remove these - the names are generic and the file may well be yours.
    foreach ($a in $legacyAgents) {
        $p = Join-Path $adest "$a.md"
        if (Test-Path -LiteralPath $p) {
            $t = Get-Content -LiteralPath $p -Raw
            if (-not [string]::IsNullOrEmpty($t) -and $t -match '_shared/dga\.md') {
                Write-Host "note      $p looks like dga-kit <=0.4 (references _shared/dga.md)."
                Write-Host "          It is superseded by dga-$a.md - delete it by hand if it is not yours."
            }
        }
    }
    if (Test-Path -LiteralPath (Join-Path $adest '_shared')) {
        Write-Host "note      $adest\_shared\ is from dga-kit <=0.4 and no longer used."
    }
}

if ($Uninstall) {
    Clear-Legacy
    foreach ($n in $skills) {
        $p = Join-Path $dest $n
        if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Recurse -Force; Write-Host "removed   skill $n" }
    }
    foreach ($a in $agents) {
        $p = Join-Path $adest "$a.md"
        if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Force; Write-Host "removed   agent $a" }
    }
    Write-Host "`nUninstalled. Restart Claude Code." -ForegroundColor Green
    exit 0
}

if (-not (Test-Path -LiteralPath $src)) {
    Write-Error 'skills\ not found - run this from inside the dga-kit folder.'; exit 1
}
New-Item -ItemType Directory -Force -Path $dest, $adest | Out-Null
Clear-Legacy

$ok = 0
foreach ($n in $skills) {
    $s = Join-Path $src $n
    $d = Join-Path $dest $n
    if (-not (Test-Path -LiteralPath (Join-Path $s 'SKILL.md'))) { Write-Host "skipped   $n (no SKILL.md)"; continue }
    if ((Test-Path -LiteralPath $d) -and -not $Force) { Write-Host "exists    $n (use -Force)"; continue }
    if (Test-Path -LiteralPath $d) { Remove-Item -LiteralPath $d -Recurse -Force }
    Copy-Item -LiteralPath $s -Destination $d -Recurse
    $ok++; Write-Host "installed skill $n"
}

$aok = 0
foreach ($a in $agents) {
    $s = Join-Path $asrc "$a.md"
    $d = Join-Path $adest "$a.md"
    if (-not (Test-Path -LiteralPath $s)) { Write-Host "skipped   $a (missing)"; continue }
    if ((Test-Path -LiteralPath $d) -and -not $Force) { Write-Host "exists    $a (use -Force)"; continue }
    Copy-Item -LiteralPath $s -Destination $d -Force
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

Write-Host "`n$ok skill(s), $aok agent(s) installed."
if ($bad -eq 0) { Write-Host 'cross-references OK' -ForegroundColor Green }
else { Write-Host "$bad broken cross-reference(s) - report this as a bug" -ForegroundColor Yellow }
Write-Host 'Restart Claude Code, then run /skills to confirm.'
