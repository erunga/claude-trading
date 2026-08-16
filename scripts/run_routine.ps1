# scripts/run_routine.ps1 — invoked by Windows Task Scheduler to run one of the
# trading agent's routines locally via headless Claude Code, with logging so
# failures are actually visible (the cloud triggers gave none).
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("morning-research", "trading-session", "eod-journal")]
    [string]$Routine
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

# Without this, *>> capturing claude's native stdout/stderr comes out with
# every character interleaved with a stray space (UTF-16 read as single-byte).
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$promptFile = Join-Path $repoRoot ".claude\local-routines\$Routine.md"
$prompt = Get-Content -Raw -Path $promptFile

$logDir = Join-Path $repoRoot "logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$stamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$logFile = Join-Path $logDir "$Routine-$stamp.log"

# Scoped to exactly what each routine needs: running the repo's own scripts and
# committing/pushing the result. Anything else Claude tries gets denied rather
# than hanging on a permission prompt with no one there to answer it.
$allowedTools = "Bash(python scripts/*.py *)", "Bash(git add *)", "Bash(git commit *)", "Bash(git push *)", "Read", "Write", "Edit", "Glob", "Grep"

"=== $Routine run started $stamp ===" | Out-File -FilePath $logFile -Encoding utf8

& claude -p $prompt --allowedTools $allowedTools --permission-mode dontAsk *>> $logFile

"=== $Routine run finished $(Get-Date -Format 'yyyy-MM-dd_HHmmss'), exit code $LASTEXITCODE ===" | Out-File -FilePath $logFile -Append -Encoding utf8
