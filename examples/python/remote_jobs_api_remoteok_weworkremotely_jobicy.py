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
