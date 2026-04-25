#!/bin/bash
SOURCE="${SOURCE:-$(dirname "$0")}"
DEST="${DEST:-$HOME/.agents/skills}"

for dir in "$SOURCE"/*/; do
  skill=$(basename "$dir")
  [[ "$skill" == ".git" ]] && continue
  tmp=$(mktemp -d)
  cp -r "$dir" "$tmp/$skill"
  rm -rf "$DEST/$skill"
  mv "$tmp/$skill" "$DEST/$skill" && echo "Synced: $skill"
  rm -rf "$tmp"
done

if command -v oxfmt &>/dev/null; then
  oxfmt --write "$DEST"/**/*.md
else
  echo "oxfmt not installed, skipping format"
fi
