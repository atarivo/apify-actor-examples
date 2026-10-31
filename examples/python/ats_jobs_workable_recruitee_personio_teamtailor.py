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
