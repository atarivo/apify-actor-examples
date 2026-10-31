#!/usr/bin/env bash
# Printable Puzzle PDF Generator: 3 word searches (free: the first 3 puzzles of every run cost nothing).
# export APIFY_TOKEN=... ; ./printable-puzzle-pdf-generator.sh
set -euo pipefail
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~printable-puzzle-pdf-generator/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"puzzle": "wordsearch", "count": 3, "seed": 11}'
