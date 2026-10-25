#!/usr/bin/env bash
# Restore local working data from the committed archives. Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p data/raw
for a in data/archive/raw-*.tar.gz; do
  tar -xzf "$a" -C data/raw
done
latest_text=$(ls data/archive/raw_local-*.sqlite.gz | sort | tail -1)
gunzip -c "$latest_text" > data/db/raw_local.sqlite
gunzip -c data/db/git_history.sqlite.gz > data/db/git_history.sqlite
echo "restored: data/raw, raw_local.sqlite ($latest_text), git_history.sqlite"
