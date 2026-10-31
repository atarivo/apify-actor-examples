# Tutorial: Remote Jobs API: Remote OK, We Work Remotely & Jobicy

Store page: https://apify.com/atarivo/remote-jobs-api-remoteok-weworkremotely-jobicy

Remote jobs from three public boards, one row per job, in the same columns as
[ATS Jobs API: Greenhouse, Lever & Ashby](ats-jobs-api-greenhouse-lever-ashby.md) (`ats` becomes
`source`). Every row carries the board's credit line in `attribution` and a link back in
`source_url`.

**Price:** $0.002 per job saved + $0.001 per run. A board that could not be read gives one row with
`error` and is never charged.

**Inputs:** `sources` (`remoteok`, `weworkremotely`, `jobicy`; all three by default), `query` (every
word must appear in the title or tags), `maxJobsPerSource` (default 500), `includeDescription`,
`postedSinceDays` (1 to 90).

**Credit:** each board asks for credit and a link back wherever its jobs are shown. Keep
`attribution` and `source_url` next to every job you display.

## Python

```python
"""Remote Jobs API: Remote OK, We Work Remotely & Jobicy: remote jobs in the same schema as the ATS Jobs
APIs (`ats` becomes `source`), each row carrying the board's credit line (`attribution`, `source_url`).

    pip install apify-client && export APIFY_TOKEN=...
    python remote_jobs_api_remoteok_weworkremotely_jobicy.py
"""
import os
from decimal import Decimal

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/remote-jobs-api-remoteok-weworkremotely-jobicy").call(
    run_input={"sources": ["jobicy", "weworkremotely"], "maxJobsPerSource": 5},
    max_total_charge_usd=Decimal("0.05"),
)
rows = list(client.dataset(run.default_dataset_id).iterate_items())
jobs = [r for r in rows if not r.get("error")]
print(f"{len(jobs)} jobs; boards that failed: {len(rows) - len(jobs)}")
for j in jobs:
    pay = f"{j['salary_min']}-{j['salary_max']} {j['salary_currency'] or ''}".strip() if j.get("salary_min") else "no salary given"
    print(f"{j['source']} | {j['title']} | {j['company']} | {j['remote_region']} | {pay} | via {j['attribution']}")
```

Output (live run, 2026-10-31):

```text
10 jobs; boards that failed: 0
jobicy | Full-Stack Engineer, AI Platform | Thumbtack | USA | 151300-229900 USD | via Jobicy
jobicy | Commerical Account Executive | Kong Inc. | USA | 100000-250000 USD | via Jobicy
jobicy | Solutions Architect III | ExtraHop | USA | 150000-163000 USD | via Jobicy
jobicy | Executive Business Partner | Twilio | USA | 108720-142000 USD | via Jobicy
jobicy | Corporate FP&A Manager | Thumbtack | USA | 137700-209000 USD | via Jobicy
weworkremotely | Senior TA Operations Specialist | Anduril Industries | USA Only | no salary given | via We Work Remotely
weworkremotely | Application Database Administrator w/Secret Clearance | TekSynap | USA Only | no salary given | via We Work Remotely
weworkremotely | Sr Technical Support Representative | Axon | Canada Only | no salary given | via We Work Remotely
weworkremotely | Backend Product Software Engineer | Dropbox | Worldwide | no salary given | via We Work Remotely
weworkremotely | Client Service Analyst - P2P | Bybit | Worldwide | no salary given | via We Work Remotely
```

## JavaScript

```javascript
// Remote Jobs API: Remote OK, We Work Remotely & Jobicy.
//   npm install apify-client && export APIFY_TOKEN=... && node remote-jobs-api-remoteok-weworkremotely-jobicy.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('atarivo/remote-jobs-api-remoteok-weworkremotely-jobicy').call(
    { sources: ['weworkremotely', 'jobicy'], maxJobsPerSource: 5 }, { maxTotalChargeUsd: 0.05 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const j of items.filter((r) => !r.error)) {
    // keep the credit: each board asks for a link back wherever its jobs are shown
    console.log(`${j.source} | ${j.title} | ${j.remote_region} | ${j.source_url} (${j.attribution})`);
}
```

Output:

```text
weworkremotely | Senior TA Operations Specialist | USA Only | https://weworkremotely.com/remote-jobs/anduril-industries-senior-ta-operations-specialist (We Work Remotely)
weworkremotely | Application Database Administrator w/Secret Clearance | USA Only | https://weworkremotely.com/remote-jobs/teksynap-application-database-administrator-w-secret-clearance (We Work Remotely)
weworkremotely | Sr Technical Support Representative | Canada Only | https://weworkremotely.com/remote-jobs/axon-sr-technical-support-representative (We Work Remotely)
weworkremotely | Backend Product Software Engineer | Worldwide | https://weworkremotely.com/remote-jobs/dropbox-backend-product-software-engineer-1 (We Work Remotely)
weworkremotely | Client Service Analyst - P2P | Worldwide | https://weworkremotely.com/remote-jobs/bybit-client-service-analyst-p2p (We Work Remotely)
jobicy | Full-Stack Engineer, AI Platform | USA | https://jobicy.com/jobs/158260-full-stack-engineer-ai-platform (Jobicy)
jobicy | Commerical Account Executive | USA | https://jobicy.com/jobs/158259-commerical-account-executive (Jobicy)
jobicy | Solutions Architect III | USA | https://jobicy.com/jobs/158258-solutions-architect-iii (Jobicy)
jobicy | Executive Business Partner | USA | https://jobicy.com/jobs/158257-executive-business-partner (Jobicy)
jobicy | Corporate FP&A Manager | USA | https://jobicy.com/jobs/158254-corporate-fpa-manager (Jobicy)
```

## curl

```bash
#!/usr/bin/env bash
# Remote Jobs API: Remote OK, We Work Remotely & Jobicy. export APIFY_TOKEN=... ; ./remote-jobs-api-remoteok-weworkremotely-jobicy.sh
set -euo pipefail
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~remote-jobs-api-remoteok-weworkremotely-jobicy/run-sync-get-dataset-items?maxTotalChargeUsd=0.05" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"sources": ["jobicy"], "maxJobsPerSource": 3}'
```

Output:

```json
[{
  "title": "Full-Stack Engineer, AI Platform",
  "company": "Thumbtack",
  "location": "USA",
  "remote": true,
  "remote_region": "USA",
  "department": "Software Engineering",
  "posted_at": "2026-10-31T17:05:04Z",
  "apply_url": "https://jobicy.com/jobs/158260-full-stack-engineer-ai-platform",
  "source": "jobicy",
  "job_id": "158260",
  "dedup_key": "jobicy:158260",
  "source_url": "https://jobicy.com/jobs/158260-full-stack-engineer-ai-platform",
  "attribution": "Jobicy",
  "salary_min": 151300,
  "salary_max": 229900,
  "salary_currency": "USD",
  "salary_period": "yearly",
  "tags": []
},
{
  "title": "Commerical Account Executive",
  "company": "Kong Inc.",
  "location": "USA",
  "remote": true,
  "remote_region": "USA",
  "department": "Sales",
  "posted_at": "2026-10-31T17:05:02Z",
  "apply_url": "https://jobicy.com/jobs/158259-commerical-account-executive",
  "source": "jobicy",
  "job_id": "158259",
  "dedup_key": "jobicy:158259",
  "source_url": "https://jobicy.com/jobs/158259-commerical-account-executive",
  "attribution": "Jobicy",
  "salary_min": 100000,
  "salary_max": 250000,
  "salary_currency": "USD",
  "salary_period": "yearly",
  "tags": []
},
{
  "title": "Solutions Architect III",
  "company": "ExtraHop",
  "location": "USA",
  "remote": true,
  "remote_region": "USA",
  "department": "Cybersecurity",
  "posted_at": "2026-10-31T17:04:44Z",
  "apply_url": "https://jobicy.com/jobs/158258-solutions-architect-iii",
  "source": "jobicy",
  "job_id": "158258",
  "dedup_key": "jobicy:158258",
  "source_url": "https://jobicy.com/jobs/158258-solutions-architect-iii",
  "attribution": "Jobicy",
  "salary_min": 150000,
  "salary_max": 163000,
  "salary_currency": "USD",
  "salary_period": "yearly",
  "tags": []
}]
```

## Tips

- `remote` is always `true`; `remote_region` says where the job can be done from ("USA Only",
  "Worldwide").
- Salary columns are filled only when the board gives a figure (Jobicy usually does).
- Merge with the ATS Jobs APIs on `dedup_key` (`source:job_id`).
- This Actor is not affiliated with or endorsed by Remote OK, We Work Remotely or Jobicy.
