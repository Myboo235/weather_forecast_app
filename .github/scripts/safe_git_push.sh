#!/bin/bash

# Usage: ./safe_git_push.sh <commit-message> <add-path>
# Example: ./safe_git_push.sh "auto-update" "model/dlinear"

COMMIT_MSG="$1"
ADD_PATH="${2:-.}"  # Default to adding everything

git config user.name "github-actions"
git config user.email "github-actions@github.com"

git pull || git pull --rebase
git add "$ADD_PATH"
git commit -m "$COMMIT_MSG - $(date '+%Y-%m-%d %H:%M')" || echo "No changes to commit"

MAX_RETRIES=3
COUNT=0
SUCCESS=0

while [ $COUNT -lt $MAX_RETRIES ]; do
  if git push; then
    echo "Push succeeded"
    SUCCESS=1
    break
  else
    echo "Push failed. Retrying in 30 seconds... (Attempt $((COUNT+1))/$MAX_RETRIES)"
    sleep 30
    git pull || git pull --rebase
    COUNT=$((COUNT+1))
  fi
done

if [ $SUCCESS -eq 0 ]; then
  echo "Push failed after $MAX_RETRIES attempts. Continuing workflow anyway."
fi
