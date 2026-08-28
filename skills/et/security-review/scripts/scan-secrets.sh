#!/usr/bin/env bash
set -euo pipefail

# Scan for secrets in the current branch diff using gitleaks
# Requires: gitleaks (https://github.com/gitleaks/gitleaks)

if ! command -v gitleaks &>/dev/null; then
  echo "ERROR: gitleaks is not installed."
  echo "Install: brew install gitleaks (macOS)"
  echo "    or: winget install Gitleaks.Gitleaks (Windows)"
  echo "    or: go install github.com/gitleaks/gitleaks/v8@latest (any platform)"
  exit 1
fi

# Determine base branch for diff
BASE_BRANCH="${1:-main}"

echo "Scanning for secrets in diff against ${BASE_BRANCH}..."
echo "---"

# Run gitleaks on the diff between base branch and HEAD
# Exit code: 0 = no leaks, 1 = leaks found
EXIT_CODE=0
gitleaks detect \
  --source . \
  --log-opts "${BASE_BRANCH}..HEAD" \
  --no-banner \
  --verbose || EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "✅ No secrets detected."
else
  echo ""
  echo "🔴 Secrets detected! Review findings above."
  exit 1
fi
