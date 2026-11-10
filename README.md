# Atarivo Apify Actor examples

[![Apify Store](https://img.shields.io/badge/Apify%20Store-atarivo-1f6feb)](https://apify.com/atarivo)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776ab)](https://docs.apify.com/api/client/python/docs)
[![apify-client](https://img.shields.io/badge/apify--client-3.x-555)](https://pypi.org/project/apify-client/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Copy-paste examples in Python, JavaScript and curl for Atarivo's pay-per-event Actors on Apify:
document text extraction for RAG, job-board data from eight applicant-tracking systems, and printable
puzzle PDFs. Every snippet here was run against the live Actor before it was committed; the outputs in
the tutorials are from those runs (2026-10-31).

## The Actors

| Actor | What it returns | Price (pay per event) |
|---|---|---|
| [PDF, Image & Word to Text and Markdown (OCR)](https://apify.com/atarivo/pdf-image-text-markdown-extractor) | Per-page text, Markdown, tables, page facts and a legibility verdict; `document.md`; RAG `chunks.json` with page spans | $0.001 per page; +$0.005 per OCR page; +$0.003 per table; the first page of every run is free |
| [ATS Jobs API: Greenhouse, Lever & Ashby](https://apify.com/atarivo/ats-jobs-api-greenhouse-lever-ashby) | One row per open job in one schema, with a stable `dedup_key` | $0.002 per job + $0.001 per run |
| [Workable, Recruitee, Personio & Teamtailor Jobs API](https://apify.com/atarivo/ats-jobs-api-workable-recruitee-personio-teamtailor) | The same job schema for four more ATS vendors, so the tables merge | $0.002 per job + $0.001 per run |
| [Printable Puzzle PDF Generator: word search, sudoku, maze](https://apify.com/atarivo/printable-puzzle-pdf-generator) | One PDF of solver-verified puzzles + answer key; one row per puzzle | $0.02 per puzzle; the first 3 of every run are free |
| [Remote Jobs API: Remote OK, We Work Remotely & Jobicy](https://apify.com/atarivo/remote-jobs-api-remoteok-weworkremotely-jobicy) | Remote jobs from three public boards in the same job schema, with each board's attribution and link back | $0.002 per job + $0.001 per run; failed boards are never charged |

What they have in common: none of them calls an AI model (the same input gives the same output),
platform usage is included in the event price (no "+usage"), you pay only for results that were
saved, and every Actor stops cleanly at the cost cap you set.

## Quick start

```bash
pip install apify-client          # Python 3.11+, apify-client 3.x
npm install apify-client          # for the JavaScript examples (Node 18+)
export APIFY_TOKEN=...            # Apify Console -> Settings -> API & Integrations
```

An Apify account is required; the free plan includes monthly platform credit and needs no card.
Every Actor follows one pattern: send JSON input, then read the run's default dataset (and, for
files, its default key-value store).

```python
import os
from decimal import Decimal
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/ats-jobs-api-greenhouse-lever-ashby").call(
    run_input={"boards": ["greenhouse"], "maxJobsPerBoard": 3},
    max_total_charge_usd=Decimal("0.05"),
)
for job in client.dataset(run.default_dataset_id).iterate_items():
    print(job["title"], "|", job["location"], "|", job["apply_url"])
```

## Agent Skills (Claude Code, Codex and other MCP clients)

Two `SKILL.md` files teach a coding agent when and how to call these Actors through the
[Apify MCP server](https://mcp.apify.com) (`https://mcp.apify.com?tools=atarivo/<actor>`), with the input
fields, the output shape, the cost per result and the edge cases spelled out. Copy a folder into your
agent's skills directory, or point the agent at the file:

| Skill | Covers | File |
|---|---|---|
| `apify-pdf-to-markdown-ocr` | PDF, scanned image and Word files to per-page text, Markdown, tables and RAG chunks | [skills/apify-pdf-to-markdown-ocr/SKILL.md](skills/apify-pdf-to-markdown-ocr/SKILL.md) |
| `apify-ats-jobs-data` | Open jobs from Greenhouse, Lever, Ashby, Workable, Recruitee, Personio, Teamtailor, SmartRecruiters and three remote job boards, one schema | [skills/apify-ats-jobs-data/SKILL.md](skills/apify-ats-jobs-data/SKILL.md) |

Both say our line plainly: no login, no credential of yours, no circumvention. The Actors read what is
public or what you hand them, and nothing else.

## Tutorials and examples

| Actor | Tutorial | Python | JavaScript | curl |
|---|---|---|---|---|
| PDF, Image & Word to Text and Markdown (OCR) | [tutorial](tutorials/pdf-image-text-markdown-extractor.md) | [py](examples/python/pdf_image_text_markdown_extractor.py) · [LangChain](examples/python/langchain_pdf_loader.py) | [mjs](examples/javascript/pdf-image-text-markdown-extractor.mjs) | [sh](examples/curl/pdf-image-text-markdown-extractor.sh) |
| ATS Jobs API: Greenhouse, Lever & Ashby | [tutorial](tutorials/ats-jobs-api-greenhouse-lever-ashby.md) | [py](examples/python/ats_jobs_greenhouse_lever_ashby.py) | [mjs](examples/javascript/ats-jobs-api-greenhouse-lever-ashby.mjs) | [sh](examples/curl/ats-jobs-api-greenhouse-lever-ashby.sh) |
| Workable, Recruitee, Personio & Teamtailor Jobs API | [tutorial](tutorials/ats-jobs-api-workable-recruitee-personio-teamtailor.md) | [py](examples/python/ats_jobs_workable_recruitee_personio_teamtailor.py) | [mjs](examples/javascript/ats-jobs-api-workable-recruitee-personio-teamtailor.mjs) | [sh](examples/curl/ats-jobs-api-workable-recruitee-personio-teamtailor.sh) |
| Printable Puzzle PDF Generator | [tutorial](tutorials/printable-puzzle-pdf-generator.md) | [py](examples/python/printable_puzzle_pdf_generator.py) | [mjs](examples/javascript/printable-puzzle-pdf-generator.mjs) | [sh](examples/curl/printable-puzzle-pdf-generator.sh) |
| Remote Jobs API: Remote OK, We Work Remotely & Jobicy | [tutorial](tutorials/remote-jobs-api-remoteok-weworkremotely-jobicy.md) | [py](examples/python/remote_jobs_api_remoteok_weworkremotely_jobicy.py) | [mjs](examples/javascript/remote-jobs-api-remoteok-weworkremotely-jobicy.mjs) | [sh](examples/curl/remote-jobs-api-remoteok-weworkremotely-jobicy.sh) |

## Use cases

- **RAG ingestion** of PDFs, scans and .docx with page-cited chunks, keeping illegible pages out of the index.
- **Table extraction** from ruled PDF tables into rows.
- **Job aggregation and hiring signals:** daily diffs of open roles at the companies you list, across
  Greenhouse, Lever, Ashby, Workable, Recruitee, Personio and Teamtailor in one table.
- **Remote job boards** (Remote OK, We Work Remotely, Jobicy) merged into the same table, keeping each
  board's credit line and link back.
- **Printable worksheets and puzzle pages** with answer keys, reproducible by seed.

## Common questions

- **How do I cap the cost?** `max_total_charge_usd` (Python), `maxTotalChargeUsd` (JavaScript call
  options) or the `maxTotalChargeUsd` query parameter (REST). Each Actor stops cleanly at the cap.
- **`run.default_dataset_id` or `run["defaultDatasetId"]`?** apify-client 3.x returns typed models
  (attribute access); 2.x returns dicts. `langchain-apify` still installs 2.x, so the LangChain example uses dicts.
- **PDF extractor: `legible: false`?** The page's final text is empty, too short, or mostly not real words.
  The sample PDF in the examples has 14 characters, so it is reported as not legible: try your own file.
- **Jobs APIs: board "not found"?** Check the slug or name in the careers address. EU-hosted Greenhouse and
  Lever boards are not supported yet; a Teamtailor site must be given as `<company>.teamtailor.com`.
- **Where do my files go?** Into the run's default key-value store, kept for your plan's retention period
  (7 days for unnamed storages on most plans). Download what you keep.

## Links

- Atarivo on the Apify Store: https://apify.com/atarivo
- Agent-readable Actor pages: append `.md` to a Store URL, e.g. https://apify.com/atarivo/pdf-image-text-markdown-extractor.md
- Apify API client docs: [Python](https://docs.apify.com/api/client/python/docs) · [JavaScript](https://docs.apify.com/api/client/js/docs)
- LangChain and LlamaIndex loaders for Apify datasets: [langchain-apify](https://docs.apify.com/integrations/langchain) · [llama-index-readers-apify](https://docs.apify.com/integrations/llama-index)
- Apify MCP server: https://docs.apify.com/mcp
- Support: the **Issues** tab on each Actor's Store page (answered within 14 days)
- [`go/`](go/): one landing page per channel we post on; see [PAGES.md](PAGES.md)

## Contributing

Issues and pull requests that fix or add examples are welcome. Do not commit API tokens: read
`APIFY_TOKEN` from the environment. Bugs in the Actors themselves belong on the Actor's Issues tab on
Apify, with the run ID.

## License

MIT for the example code in this repository (see [LICENSE](LICENSE)). The Actors are provided under
Apify's Standard Actor Contract. The Actors are not affiliated with or endorsed by the vendors whose
public job feeds or file formats they read.
