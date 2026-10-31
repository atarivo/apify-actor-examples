#!/usr/bin/env bash
# Workable, Recruitee, Personio & Teamtailor Jobs API. export APIFY_TOKEN=... ; ./ats-jobs-api-workable-recruitee-personio-teamtailor.sh
set -euo pipefail
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~ats-jobs-api-workable-recruitee-personio-teamtailor/run-sync-get-dataset-items?maxTotalChargeUsd=0.05" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"boards": ["https://personio-gmbh.jobs.personio.de"], "maxJobsPerBoard": 3}'
