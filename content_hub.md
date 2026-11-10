# Atarivo on Apify

Small, deterministic data tools: limited permissions, no "+usage" pricing, charged only for results that were
saved, and no AI model inside.

## Actors

- **[PDF, Image & Word to Text and Markdown (OCR)](https://apify.com/atarivo/pdf-image-text-markdown-extractor)**:
  PDF, scans, PNG/JPEG/TIFF and .docx to per-page text, Markdown, tables and a legibility verdict, plus RAG
  chunks with page spans. OCR only on pages that need it. $0.001 per page; the first page of every run is free.
- **[ATS Jobs API: Greenhouse, Lever & Ashby](https://apify.com/atarivo/ats-jobs-api-greenhouse-lever-ashby)**:
  every open job on the boards you list, in one schema with a stable dedup key. Public job-board APIs, no login.
  $0.002 per job.
- **[Workable, Recruitee, Personio & Teamtailor Jobs API](https://apify.com/atarivo/ats-jobs-api-workable-recruitee-personio-teamtailor)**:
  the same schema for four more ATS vendors. $0.002 per job.
- **[Printable Puzzle PDF Generator: word search, sudoku, maze](https://apify.com/atarivo/printable-puzzle-pdf-generator)**:
  word search, sudoku, maze and nonogram PDFs with answer keys, every puzzle solver-checked. The first 3 puzzles
  of every run are free, then $0.02 each.
- **[Remote Jobs API: Remote OK, We Work Remotely & Jobicy](https://apify.com/atarivo/remote-jobs-api-remoteok-weworkremotely-jobicy)**:
  remote jobs from three public boards in the same schema as the ATS Jobs APIs, each row with the board's
  credit line and link back. $0.002 per job; a board that could not be read is never charged.

## Code

- Examples (Python, JavaScript, curl) and tutorials: https://github.com/atarivo/apify-actor-examples
- Agent Skills (`SKILL.md` for Claude Code, Codex and other MCP clients): https://github.com/atarivo/apify-actor-examples/tree/main/skills

## Support

Open an issue on the Actor's **Issues** tab on Apify with the run ID. Issues are answered within 14 days.
