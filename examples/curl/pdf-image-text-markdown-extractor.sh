#!/usr/bin/env bash
# PDF, Image & Word to Text and Markdown (OCR): synchronous run, the dataset rows come back as JSON.
# export APIFY_TOKEN=... ; ./pdf-image-text-markdown-extractor.sh [PDF_URL]
set -euo pipefail
URL=${1:-https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf}
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~pdf-image-text-markdown-extractor/run-sync-get-dataset-items?maxTotalChargeUsd=0.1" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d "{\"url\": \"$URL\", \"outputs\": [\"text\", \"markdown\"]}"
