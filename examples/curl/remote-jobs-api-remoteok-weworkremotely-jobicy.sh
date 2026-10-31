#!/usr/bin/env bash
# Remote Jobs API: Remote OK, We Work Remotely & Jobicy. export APIFY_TOKEN=... ; ./remote-jobs-api-remoteok-weworkremotely-jobicy.sh
set -euo pipefail
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~remote-jobs-api-remoteok-weworkremotely-jobicy/run-sync-get-dataset-items?maxTotalChargeUsd=0.05" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"sources": ["jobicy"], "maxJobsPerSource": 3}'
