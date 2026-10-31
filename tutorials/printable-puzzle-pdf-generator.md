# Tutorial: Printable Puzzle PDF Generator: word search, sudoku, maze

Store page: https://apify.com/atarivo/printable-puzzle-pdf-generator

One run makes one print-ready PDF: the puzzles, then an answer key. Every puzzle is checked by a
solver before it is saved (a sudoku has exactly one solution; a maze has a path). The dataset has one
row per puzzle with its page, its answer page and the seed, so a run can be reproduced exactly.

**Price:** the first 3 puzzles of every run are free, then $0.02 per puzzle. The examples below make
3 puzzles each, so they cost nothing in events.

## Python: sudoku

```python
"""Printable Puzzle PDF Generator: one PDF (puzzles + answer key), one dataset row per puzzle.
The first 3 puzzles of every run are free, so this example costs nothing in events.

    pip install apify-client && export APIFY_TOKEN=...
    python printable_puzzle_pdf_generator.py      # writes sudoku.pdf
"""
import os
import pathlib

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/printable-puzzle-pdf-generator").call(
    run_input={"puzzle": "sudoku", "count": 3, "difficulty": "hard", "seed": 42},
)
rows = list(client.dataset(run.default_dataset_id).iterate_items())
for r in rows:
    print(r["title"], "| page", r["page"], "| answer page", r["answer_page"])
rec = client.key_value_store(run.default_key_value_store_id).get_record(rows[0]["pdf_key"])
pathlib.Path("sudoku.pdf").write_bytes(rec["value"])
print(f"sudoku.pdf: {rows[0]['pdf_pages']} pages, {pathlib.Path('sudoku.pdf').stat().st_size} bytes")
```

Output (live run, 2026-10-31):

```text
Sudoku 1 of 3 | page 1 | answer page 4
Sudoku 2 of 3 | page 2 | answer page 5
Sudoku 3 of 3 | page 3 | answer page 6
sudoku.pdf: 6 pages, 8966 bytes
```

## JavaScript: maze

```javascript
// Printable Puzzle PDF Generator: 3 mazes (the first 3 puzzles of every run are free).
//   npm install apify-client && export APIFY_TOKEN=... && node printable-puzzle-pdf-generator.mjs
import { writeFile } from 'node:fs/promises';
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('atarivo/printable-puzzle-pdf-generator').call({ puzzle: 'maze', count: 3, seed: 7 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const r of items) console.log(`${r.title} | page ${r.page} | answer page ${r.answer_page}`);
const rec = await client.keyValueStore(run.defaultKeyValueStoreId).getRecord(items[0].pdf_key, { buffer: true });
await writeFile('maze.pdf', rec.value);
console.log(`maze.pdf: ${items[0].pdf_pages} pages`);
```

Output:

```text
Maze 1 of 3 | page 1 | answer page 4
Maze 2 of 3 | page 2 | answer page 5
Maze 3 of 3 | page 3 | answer page 6
maze.pdf: 6 pages
```

## curl: word search

```bash
#!/usr/bin/env bash
# Printable Puzzle PDF Generator: 3 word searches (free: the first 3 puzzles of every run cost nothing).
# export APIFY_TOKEN=... ; ./printable-puzzle-pdf-generator.sh
set -euo pipefail
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~printable-puzzle-pdf-generator/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"puzzle": "wordsearch", "count": 3, "seed": 11}'
```

Output (first row; signed links shortened to `<signed-url>`):

```json
{
  "index": 1,
  "puzzle": "wordsearch",
  "difficulty": "medium",
  "title": "Word search 1 of 3",
  "page": 1,
  "answer_page": 4,
  "seed": 11,
  "pdf_url": "<signed-url>",
  "pdf_key": "puzzles.pdf",
  "pdf_pages": 6,
  "page_size": "letter",
  "details": {
    "theme": "Geography",
    "grid": "15x15",
    "words": [
      "BASIN",
      "CAPE",
      "CAVE",
      "CHANNEL",
      "CLIFF",
      "ESTUARY",
      "HILL",
      "ISLAND",
      "LAGOON",
      "MARSH",
      "MOUNTAIN",
      "OASIS",
      "PENINSULA",
      "PRAIRIE",
      "REEF",
      "RIVER",
      "STRAIT",
      "SWAMP",
      "VOLCANO",
      "WATERFALL"
    ]
  }
}
```

## Tips

- Keep the `seed` to make the same puzzles again.
- Set the `pageSize` input to `letter` (default) or `a4`.
- The PDF is in the run's default key-value store under `pdf_key`; download it, since unnamed stores expire.
