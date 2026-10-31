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
