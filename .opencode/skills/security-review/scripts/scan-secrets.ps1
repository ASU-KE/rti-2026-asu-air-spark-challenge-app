#Requires -Version 5.1
<#
.SYNOPSIS
    Scan for secrets in the current branch diff using gitleaks.
.PARAMETER BaseBranch
    The base branch to diff against. Defaults to 'main'.
#>
param(
    [string]$BaseBranch = "main"
)

if (-not (Get-Command gitleaks -ErrorAction SilentlyContinue)) {
    Write-Error "ERROR: gitleaks is not installed.`nInstall: winget install gitleaks`n    or: go install github.com/gitleaks/gitleaks/v8@latest"
    exit 1
}

Write-Host "Scanning for secrets in diff against ${BaseBranch}..."
Write-Host "---"

& gitleaks detect `
    --source . `
    --log-opts "${BaseBranch}..HEAD" `
    --no-banner `
    --verbose

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ No secrets detected." -ForegroundColor Green
} else {
    Write-Host "`n🔴 Secrets detected! Review findings above." -ForegroundColor Red
    exit 1
}
