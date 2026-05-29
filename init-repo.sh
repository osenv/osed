#!/usr/bin/env bash
#
# init-repo.sh — initialize OSED locally and create the "osed" repo on GitHub
#                using your existing GitHub CLI (gh) authentication.
#
# Usage:
#   ./init-repo.sh                 # creates a PRIVATE repo named "osed" and pushes
#   ./init-repo.sh --public        # creates a PUBLIC repo instead
#
set -euo pipefail

VISIBILITY="--private"
[ "${1:-}" = "--public" ] && VISIBILITY="--public"

# Must be run from the repo root.
if [ ! -f README.md ] || [ ! -d skills ]; then
  echo "Error: run this from the OSED repo root (README.md and skills/ expected)." >&2
  exit 1
fi

# Need gh, and need it authenticated.
if ! command -v gh >/dev/null 2>&1; then
  echo "Error: GitHub CLI (gh) not found. Install it: https://cli.github.com" >&2
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "Error: gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi

# Local git: init on main if needed, then commit the seed.
[ -d .git ] || git init -b main >/dev/null
git add .
if git diff --cached --quiet; then
  echo "Nothing new to commit."
else
  git commit -q -m "OSED seed: four-agent skill library, instrument templates, and connectors"
fi

# Create the GitHub repo named "osed" from this directory and push.
# Uses your existing gh auth; sets the remote to "origin".
echo "Creating GitHub repo 'osed' (${VISIBILITY#--}) and pushing..."
gh repo create osed --source=. --remote=origin --push "$VISIBILITY"

echo
echo "Done. 'osed' created and pushed."
gh repo view osed --web >/dev/null 2>&1 || true
echo "View it with:  gh repo view osed --web"
echo "Read DISCLAIMER.md first — these tools draft; a licensed attorney decides."
