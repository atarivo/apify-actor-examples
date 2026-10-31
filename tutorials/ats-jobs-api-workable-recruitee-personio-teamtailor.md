# Tutorial: Workable, Recruitee, Personio & Teamtailor Jobs API

Store page: https://apify.com/atarivo/ats-jobs-api-workable-recruitee-personio-teamtailor

The same one-row-per-job schema as
[ATS Jobs API: Greenhouse, Lever & Ashby](ats-jobs-api-greenhouse-lever-ashby.md), for four more
applicant-tracking systems that are common with European employers. Give it careers addresses; it
works out the vendor from the address.

**Price:** $0.002 per job saved + $0.001 per run.

## Python

```python
"""Workable, Recruitee, Personio & Teamtailor Jobs API: the same schema as the Greenhouse/Lever/Ashby
Actor, so the two tables merge.

    pip install apify-client && export APIFY_TOKEN=...
    python ats_jobs_workable_recruitee_personio_teamtailor.py
"""
import os
from collections import Counter
from decimal import Decimal

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/ats-jobs-api-workable-recruitee-personio-teamtailor").call(
    run_input={"boards": ["https://personio-gmbh.jobs.personio.de", "https://career.teamtailor.com"],
               "maxJobsPerBoard": 5},
    max_total_charge_usd=Decimal("0.05"),
)
rows = list(client.dataset(run.default_dataset_id).iterate_items())
errors = [r for r in rows if r.get("error")]
jobs = [r for r in rows if not r.get("error")]
print(f"{len(jobs)} jobs by ATS: {dict(Counter(j['ats'] for j in jobs))}; boards that failed: {len(errors)}")
for j in jobs:
    print(j["ats"], "|", j["title"], "|", j["location"], "| remote:", j["remote"])
```

Output (live run, 2026-10-31):

```text
8 jobs by ATS: {'personio': 3, 'teamtailor': 5}; boards that failed: 0
personio | Initiativbewerbung (Festanstellung) | Remote | remote: True
personio | SEO Marketing Manager | München | remote: None
personio | Social Media (Werkstudent) | München | remote: None
teamtailor | Solution Architect (Bilingual French/English) | Stockholm, SE; Paris, FR | remote: None
teamtailor | Head of Marketing - North America | Chicago, US | remote: None
teamtailor | Strategic Partnerships Manager - Chicago | Chicago, US | remote: None
teamtailor | Account Executive - Bogota | Bogotá, CO | remote: None
teamtailor | Senior Revenue Systems Administrator | Stockholm, SE | remote: None
```

## JavaScript

```javascript
// Workable, Recruitee, Personio & Teamtailor Jobs API.
//   npm install apify-client && export APIFY_TOKEN=... && node ats-jobs-api-workable-recruitee-personio-teamtailor.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('atarivo/ats-jobs-api-workable-recruitee-personio-teamtailor').call(
    { boards: ['https://career.teamtailor.com'], maxJobsPerBoard: 5 }, { maxTotalChargeUsd: 0.05 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const j of items.filter((r) => !r.error)) {
    console.log(`${j.ats} | ${j.title} | ${j.location} | remote: ${j.remote}`);
}
```

Output:

```text
teamtailor | Solution Architect (Bilingual French/English) | Stockholm, SE; Paris, FR | remote: null
teamtailor | Head of Marketing - North America | Chicago, US | remote: null
teamtailor | Strategic Partnerships Manager - Chicago | Chicago, US | remote: null
teamtailor | Account Executive - Bogota | Bogotá, CO | remote: null
teamtailor | Senior Revenue Systems Administrator | Stockholm, SE | remote: null
```

## curl

```bash
#!/usr/bin/env bash
# Workable, Recruitee, Personio & Teamtailor Jobs API. export APIFY_TOKEN=... ; ./ats-jobs-api-workable-recruitee-personio-teamtailor.sh
set -euo pipefail
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~ats-jobs-api-workable-recruitee-personio-teamtailor/run-sync-get-dataset-items?maxTotalChargeUsd=0.05" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"boards": ["https://personio-gmbh.jobs.personio.de"], "maxJobsPerBoard": 3}'
```

Output:

```json
[{
  "title": "Initiativbewerbung (Festanstellung)",
  "company": "personio-gmbh",
  "location": "Remote",
  "remote": true,
  "department": null,
  "posted_at": "2018-07-31T09:25:04Z",
  "apply_url": "https://personio-gmbh.jobs.personio.de/job/1676226",
  "ats": "personio",
  "board": "personio-gmbh",
  "job_id": "1676226",
  "dedup_key": "personio:1676226"
},
{
  "title": "SEO Marketing Manager",
  "company": "personio-gmbh",
  "location": "München",
  "remote": null,
  "department": null,
  "posted_at": "2016-10-10T11:33:38Z",
  "apply_url": "https://personio-gmbh.jobs.personio.de/job/1676223",
  "ats": "personio",
  "board": "personio-gmbh",
  "job_id": "1676223",
  "dedup_key": "personio:1676223"
},
{
  "title": "Social Media (Werkstudent)",
  "company": "personio-gmbh",
  "location": "München",
  "remote": null,
  "department": null,
  "posted_at": "2016-10-31T20:03:06Z",
  "apply_url": "https://personio-gmbh.jobs.personio.de/job/1676224",
  "ats": "personio",
  "board": "personio-gmbh",
  "job_id": "1676224",
  "dedup_key": "personio:1676224"
}]
```

## Tips

- A Teamtailor site must be given as `<company>.teamtailor.com` (a custom domain is not detected).
- `remote` is `true` only when the board says so; `null` means the board did not say.
- A site that could not be read gives one row with `error` instead (billed as one job).
- Merge with the Greenhouse/Lever/Ashby table on `dedup_key`.
