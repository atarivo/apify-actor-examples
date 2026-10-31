# Tutorial: ATS Jobs API: Greenhouse, Lever & Ashby

Store page: https://apify.com/atarivo/ats-jobs-api-greenhouse-lever-ashby

Give it a list of job boards (a company's board slug or its careers address) and it returns one row
per open job in one schema: `title`, `company`, `location`, `remote`, `department`, `posted_at`,
`apply_url`, `ats`, `board`, `job_id` and a stable `dedup_key` (`<ats>:<job_id>`). It reads the
vendors' public job-board APIs: no login, no browser.

**Price:** $0.002 per job saved + $0.001 per run. `maxJobsPerBoard` and a cost cap keep runs small.

The same schema is returned by the
[Workable, Recruitee, Personio & Teamtailor Jobs API](ats-jobs-api-workable-recruitee-personio-teamtailor.md),
so the two tables merge.

## Python: a daily "what's new" diff

```python
"""ATS Jobs API: Greenhouse, Lever & Ashby: one row per open job, one schema, a stable dedup_key.
Keeps seen.json so a daily run prints only the jobs that are new since the last run.

    pip install apify-client && export APIFY_TOKEN=...
    python ats_jobs_greenhouse_lever_ashby.py
"""
import json
import os
import pathlib
from decimal import Decimal

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/ats-jobs-api-greenhouse-lever-ashby").call(
    run_input={"boards": ["greenhouse", "https://jobs.lever.co/palantir", "https://jobs.ashbyhq.com/ashby"],
               "maxJobsPerBoard": 3},
    max_total_charge_usd=Decimal("0.05"),
)
jobs = [r for r in client.dataset(run.default_dataset_id).iterate_items() if not r.get("error")]
seen_file = pathlib.Path("seen.json")
seen = set(json.loads(seen_file.read_text())) if seen_file.exists() else set()
new = [j for j in jobs if j["dedup_key"] not in seen]
seen_file.write_text(json.dumps(sorted(seen | {j["dedup_key"] for j in jobs})))
print(f"{len(jobs)} jobs, {len(new)} new")
for j in new:
    print(j["ats"], j["company"], "|", j["title"], "|", j["location"], "|", j["posted_at"])
```

Output (live run, 2026-10-31; first run, so every job is new):

```text
9 jobs, 9 new
greenhouse Greenhouse | Commercial Counsel | Eastern Timezone | 2026-08-24T17:52:04Z
greenhouse Greenhouse | Enterprise Account Executive | London, United Kingdom | 2026-10-14T15:52:46Z
greenhouse Greenhouse | Enterprise Sales Development Representative | Anywhere in the United States | 2026-09-28T13:18:45Z
lever palantir | Administrative Business Partner | Singapore, Singapore | 2026-08-11T17:38:11Z
lever palantir | Administrative Business Partner - ShipOS | Washington, D.C. | 2026-06-18T08:34:20Z
lever palantir | Administrative Business Partner - ShipOS | New York, NY | 2026-06-18T08:33:52Z
ashby ashby | Engineering Manager - EU | Remote - European Union | 2024-03-04T14:29:08Z
ashby ashby | Mid Market Account Executive - EMEA (French Speaking) | France | 2026-09-08T16:27:26Z
ashby ashby | Senior Product Designer | Remote - US | 2025-12-05T22:43:22Z
```

Run it again tomorrow and only the jobs posted since show up as new.

## JavaScript

```javascript
// ATS Jobs API: Greenhouse, Lever & Ashby.
//   npm install apify-client && export APIFY_TOKEN=... && node ats-jobs-api-greenhouse-lever-ashby.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('atarivo/ats-jobs-api-greenhouse-lever-ashby').call(
    { boards: ['lever:palantir', 'ashby:ashby'], maxJobsPerBoard: 3 }, { maxTotalChargeUsd: 0.05 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const j of items.filter((r) => !r.error)) {
    console.log(`${j.ats} | ${j.title} | ${j.location} | ${j.dedup_key}`);
}
```

Output:

```text
lever | Administrative Business Partner | Singapore, Singapore | lever:6ed76ce8-4156-4b60-b120-403538bd66cd
lever | Administrative Business Partner - ShipOS | Washington, D.C. | lever:a237973c-cb29-41fe-9c80-416e6f42e087
lever | Administrative Business Partner - ShipOS | New York, NY | lever:a5f93bb6-4f13-4451-80a4-f63090830269
ashby | Engineering Manager - EU | Remote - European Union | ashby:7458d4e9-da2e-47bd-98cb-adfda43d42b2
ashby | Mid Market Account Executive - EMEA (French Speaking) | France | ashby:86a60834-ba64-484d-9658-afa1bc97a957
ashby | Senior Product Designer | Remote - US | ashby:f40ef345-82a8-4956-9150-193b4fdf8183
```

## curl

```bash
#!/usr/bin/env bash
# ATS Jobs API: Greenhouse, Lever & Ashby. export APIFY_TOKEN=... ; ./ats-jobs-api-greenhouse-lever-ashby.sh
set -euo pipefail
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~ats-jobs-api-greenhouse-lever-ashby/run-sync-get-dataset-items?maxTotalChargeUsd=0.05" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"boards": ["greenhouse"], "maxJobsPerBoard": 3}'
```

Output:

```json
[{
  "title": "Commercial Counsel",
  "company": "Greenhouse",
  "location": "Eastern Timezone",
  "remote": null,
  "department": "Legal Team",
  "posted_at": "2026-08-24T17:52:04Z",
  "apply_url": "https://job-boards.greenhouse.io/greenhouse/jobs/8126988?gh_jid=8126988",
  "ats": "greenhouse",
  "board": "greenhouse",
  "job_id": "8126988",
  "dedup_key": "greenhouse:8126988"
},
{
  "title": "Enterprise Account Executive",
  "company": "Greenhouse",
  "location": "London, United Kingdom",
  "remote": null,
  "department": "Account Executive",
  "posted_at": "2026-10-14T15:52:46Z",
  "apply_url": "https://job-boards.greenhouse.io/greenhouse/jobs/8279752?gh_jid=8279752",
  "ats": "greenhouse",
  "board": "greenhouse",
  "job_id": "8279752",
  "dedup_key": "greenhouse:8279752"
},
{
  "title": "Enterprise Sales Development Representative",
  "company": "Greenhouse",
  "location": "Anywhere in the United States",
  "remote": null,
  "department": "Sales Development",
  "posted_at": "2026-09-28T13:18:45Z",
  "apply_url": "https://job-boards.greenhouse.io/greenhouse/jobs/8234044?gh_jid=8234044",
  "ats": "greenhouse",
  "board": "greenhouse",
  "job_id": "8234044",
  "dedup_key": "greenhouse:8234044"
}]
```

## Tips

- Rows with an `error` field describe a board that could not be read (wrong slug, board gone); the
  rest of the run still completes, and each error row is billed as one job.
- Key your store on `dedup_key`, not on the title: titles repeat across locations.
- EU-hosted Greenhouse and Lever boards are not supported yet.
