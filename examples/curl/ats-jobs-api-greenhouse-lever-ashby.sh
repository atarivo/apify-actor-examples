#!/usr/bin/env bash
# ATS Jobs API: Greenhouse, Lever & Ashby. export APIFY_TOKEN=... ; ./ats-jobs-api-greenhouse-lever-ashby.sh
set -euo pipefail
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~ats-jobs-api-greenhouse-lever-ashby/run-sync-get-dataset-items?maxTotalChargeUsd=0.05" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"boards": ["greenhouse"], "maxJobsPerBoard": 3}'
