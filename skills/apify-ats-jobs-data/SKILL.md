---
name: apify-ats-jobs-data
description: Get every open job from a company's public job board on Greenhouse, Lever, Ashby, Workable, Recruitee, Personio, Teamtailor or SmartRecruiters, or fresh remote jobs from Remote OK, We Work Remotely and Jobicy, as one normalized row per job (title, company, location, remote flag, department, posted date, apply URL, stable dedup key), using Atarivo's three jobs Actors on Apify through the Apify MCP server or apify-client. Use when a task needs current job postings from named employers or remote boards, a jobs dataset to diff over time, or hiring signals by company; never for candidate or recruiter contact data. Pay per job, no login.
license: MIT
metadata:
  author: atarivo
  version: "1.0"
  actors: atarivo/ats-jobs-api-greenhouse-lever-ashby, atarivo/ats-jobs-api-workable-recruitee-personio-teamtailor, atarivo/remote-jobs-api-remoteok-weworkremotely-jobicy
---

# Job-board data from applicant tracking systems (Apify Actors)

Three deterministic Actors, one job schema, so rows from eleven sources go into the same table
without mapping. No AI model inside: the same board gives the same rows. Each Actor calls only the
public job-board APIs or feeds of the systems it names, sends an honest User-Agent that names the
Actor, reads each host's `robots.txt` and obeys it (including `Crawl-delay`) everywhere except
`api.smartrecruiters.com`: that file allows only LinkedInBot (`Allow: /v1/companies/`) and disallows
every other agent (`User-agent: * / Disallow: /`); the Workable, Recruitee, Personio, Teamtailor and
SmartRecruiters Actor treats it as advisory for that one host only, because the same host publishes
and documents this API for exactly this use (listing a company's public jobs); it still fetches the
file on every run, records its verdict in the run summary (`robots_advisory_hosts`) and the log, and
keeps the same rate limit and honest User-Agent (see that Actor's README, "Is it legal?"). Each
Actor sends at most 2 requests per second (per host on the Greenhouse, Lever and Ashby Actor; per
vendor on the Workable one) and retries a failed request once.

**Our line, said plainly:** these tools never log in, never use a credential of yours, never read
behind a paywall or a bot wall, and never circumvent anything. They read the job postings an
employer publishes for anyone to see. They do not look for or extract recruiter or candidate
contact details. Workday, Indeed, LinkedIn, BambooHR and every aggregator are refused before
anything is fetched or charged, and so are EU-hosted Greenhouse and Lever boards.

## Which Actor

| You have | Actor (`owner/name`) | Sources |
|---|---|---|
| A company's board on Greenhouse, Lever or Ashby | `atarivo/ats-jobs-api-greenhouse-lever-ashby` | boards-api.greenhouse.io, api.lever.co, api.ashbyhq.com |
| A career site on Workable, Recruitee, Personio, Teamtailor or SmartRecruiters | `atarivo/ats-jobs-api-workable-recruitee-personio-teamtailor` | the vendor's public careers page or feed |
| No employer in mind: remote jobs by keyword | `atarivo/remote-jobs-api-remoteok-weworkremotely-jobicy` | Remote OK, We Work Remotely, Jobicy public feeds |

Store pages: https://apify.com/atarivo (each Actor also has an agent-readable `.md` page at its Store
URL plus `.md`).

## Setup: Apify MCP server (preferred for agents)

Load the Actor(s) you need as tools:

```text
https://mcp.apify.com?tools=atarivo/ats-jobs-api-greenhouse-lever-ashby,atarivo/ats-jobs-api-workable-recruitee-personio-teamtailor,atarivo/remote-jobs-api-remoteok-weworkremotely-jobicy
```

Authentication is OAuth on first connect, or the header `Authorization: Bearer <APIFY_TOKEN>`.
Claude Code:

```bash
claude mcp add apify "https://mcp.apify.com?tools=atarivo/ats-jobs-api-greenhouse-lever-ashby" -t http
```

Tool names replace `/` with `--`, for example `atarivo--ats-jobs-api-greenhouse-lever-ashby`.
Apify's run and dataset tools load alongside, which is how you read the rows.

## Setup: apify-client

```python
import os
from decimal import Decimal
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/ats-jobs-api-greenhouse-lever-ashby").call(
    run_input={"boards": ["https://job-boards.greenhouse.io/acme", "lever:acme"], "maxJobsPerBoard": 200},
    max_total_charge_usd=Decimal("1.00"),
)
jobs = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if "error" not in r]
```

Examples in Python, JavaScript and curl: `examples/`; tutorials in `tutorials/`.

## Input

Greenhouse / Lever / Ashby:

| Field | Meaning |
|---|---|
| `boards` (required, up to 200) | A board URL (`job-boards.greenhouse.io/acme`, `jobs.lever.co/acme`, `jobs.ashbyhq.com/acme`), `ats:slug` (`lever:acme`), or a bare slug tried on Greenhouse, then Lever, then Ashby. |
| `includeDescription` | Add `description_text` (the posting as plain text). Off by default; same price either way. |
| `maxJobsPerBoard` | Stop a board after this many jobs (1 to 10000, default 1000). Caps the cost per board. |

Workable / Recruitee / Personio / Teamtailor / SmartRecruiters: the same three fields; `boards`
takes a careers URL (`apply.workable.com/acme`, `acme.recruitee.com`, `acme.jobs.personio.de`,
`acme.teamtailor.com`, `jobs.smartrecruiters.com/Acme`), `ats:name`, or a bare name tried on
Workable, Recruitee, Personio, then Teamtailor (not SmartRecruiters).

Remote boards:

| Field | Meaning |
|---|---|
| `sources` | Any of `remoteok`, `weworkremotely`, `jobicy` (default all three). |
| `query` | Keep jobs whose title or tags contain every word (case-insensitive), e.g. `data engineer`. |
| `maxJobsPerSource` | 1 to 5000, default 500. |
| `postedSinceDays` | 1 to 90; jobs without a date are dropped when set. |
| `includeDescription` | As above. |

## Output: one row per job

```json
{"title": "Senior Data Engineer", "company": "acme", "location": "Berlin, Germany", "remote": true,
 "department": "Engineering", "posted_at": "2026-11-03T09:12:00Z",
 "apply_url": "https://jobs.lever.co/acme/8f1c...", "ats": "lever", "board": "acme",
 "job_id": "8f1c...", "dedup_key": "lever:8f1c..."}
```

- `dedup_key` is `ats:job_id` (remote boards: `source:job_id`): unique within a run and stable across
  runs, so two runs can be diffed for new and closed postings.
- `remote` is `null` when the system does not say; `location` is the employer's own text.
- Remote-board rows add `remote_region`, `salary_min` / `salary_max` / `salary_currency` /
  `salary_period` when the board gives them, `tags`, `source_url` and `attribution`. **Show the
  board's name and link wherever you display a remote job**; the boards ask for it.
- A board that could not be read gives one error row (`error`, `message`, `http_status`, `tried`,
  `charged`). `robots` and `bad_response` are never charged; on the remote Actor no error row is charged.

## Cost and budget

- `$0.002` per job delivered (`job-scraped`) plus a `$0.001` start fee per run. Platform usage is
  included.
- Cap every run: `max_total_charge_usd` in the client or **Max cost per run** in the Console; the
  Actor stops cleanly at the cap. Worked example from those two prices: a board with 300 open jobs
  is `300 x $0.002 = $0.60` in job events plus the `$0.001` start. Tell the user before reading many
  boards. Within a run the same board listed twice is charged once per job.
- **Error rows are billed on the two ATS Actors:** a board or career site that does not exist (HTTP
  404 on every ATS tried) or that did not answer after a retry costs one `job-scraped` event for its
  error row. A board skipped because of robots.txt, or a response the Actor could not read, is never
  charged. On the Remote Jobs Actor no error row is ever charged.
- Invalid input (an aggregator, Workday, an EU-hosted Greenhouse or Lever board, a malformed entry)
  fails before any fetch and costs nothing.

## Edge cases the agent should handle

- **Which ATS does the company use?** Open its careers page; the apply link's host names the system.
  A bare slug is tried across systems, but a URL is cheaper and exact.
- **Company name on Lever and Ashby** is the board slug (those APIs return no company name).
- **Hybrid roles** come back `remote: false`; read `location` too.
- **Rate limits:** the Actor already paces itself and retries once; do not run the same board in
  parallel.
- **Personal data:** none is collected. If a task asks for recruiter emails or candidate details,
  decline; these Actors do not and will not provide them.

## Related

- Document extraction skill in this repository: `skills/apify-pdf-to-markdown-ocr/SKILL.md`.
- Not affiliated with or endorsed by Greenhouse, Lever, Ashby, Workable, Recruitee, Personio,
  Teamtailor, SmartRecruiters, Remote OK, We Work Remotely or Jobicy.
