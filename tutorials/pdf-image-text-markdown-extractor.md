# Tutorial: PDF, Image & Word to Text and Markdown (OCR)

Store page: https://apify.com/atarivo/pdf-image-text-markdown-extractor

The Actor turns a PDF, a scanned image (PNG, JPEG, TIFF) or a .docx into one dataset row per page
(text, Markdown, tables, page facts and a legibility verdict), one `document` row, a whole-document
`document.md`, and `chunks.json`: RAG-ready chunks that carry the pages they span. OCR runs only on
pages that have no usable text layer. No AI model is called, so the same file gives the same output.

**Price:** $0.001 per page, plus $0.005 per page that needed OCR and $0.003 per table found. The first
page of every run is free, so the examples below cost nothing in events.

## Input

| Field | Meaning |
|---|---|
| `url` | A public link to the file (or upload it to a key-value store) |
| `outputs` | Any of `text`, `markdown`, `tables`, `chunks` |
| `chunkChars` | Target chunk size for `chunks.json` |

## Python

Python 3.11+, `pip install apify-client` (3.x).

```python
"""PDF, Image & Word to Text and Markdown (OCR): one dataset row per page + document.md + chunks.json.

    pip install apify-client      # 3.x, Python 3.11+
    export APIFY_TOKEN=...        # Apify Console -> Settings -> API & Integrations
    python pdf_image_text_markdown_extractor.py https://example.com/report.pdf
"""
import json
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/pdf-image-text-markdown-extractor").call(
    run_input={"url": url, "chunkChars": 1200},
    max_total_charge_usd=Decimal("0.10"),          # the run stops cleanly at this cap
)
rows = list(client.dataset(run.default_dataset_id).iterate_items())
pages = [r for r in rows if r.get("type") == "page"]
doc = next(r for r in rows if r.get("type") == "document")
print(f"pages: {doc['pages']}, tables: {doc['tables_found']}, truncated: {doc['truncated']}")
for p in pages:
    print(f"page {p['page']}: legible={p['legible']} ocr={p['ocr']} chars={p['facts']['chars']}")
    print(p["markdown"][:200])

kvs = client.key_value_store(run.default_key_value_store_id)
chunks = kvs.get_record("chunks.json")["value"]
if isinstance(chunks, (str, bytes)):
    chunks = json.loads(chunks)
print(f"chunks: {len(chunks['chunks'])}; first spans pages {chunks['chunks'][0]['page_start']}-{chunks['chunks'][0]['page_end']}")
```

Output (live run, 2026-10-31):

```text
pages: 1, tables: 0, truncated: False
page 1: legible=False ocr=False chars=14
Dummy PDF file
chunks: 1; first spans pages 1-1
```

`legible=False` is correct here: the sample PDF holds only 14 characters, below the 60-character floor.
Use your own file to see real pages and chunks.

## LangChain

`ApifyDatasetLoader` turns the page rows into LangChain `Document`s with the page number in the metadata,
so you can keep illegible pages out of your index.

```python
"""PDF pages -> LangChain Documents, one per legible page, with the page number in the metadata.

    pip install langchain-apify      # pulls apify-client 2.x (dict results), not 3.x
    export APIFY_TOKEN=...
    python langchain_pdf_loader.py https://example.com/report.pdf
"""
import os
import sys

from apify_client import ApifyClient
from langchain_apify import ApifyDatasetLoader
from langchain_core.documents import Document

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/pdf-image-text-markdown-extractor").call(
    run_input={"url": url, "outputs": ["text", "markdown"]}, max_total_charge_usd=0.10)

docs = ApifyDatasetLoader(
    dataset_id=run["defaultDatasetId"],
    dataset_mapping_function=lambda item: Document(
        page_content=item.get("markdown") or item.get("text") or "",
        metadata={"page": item.get("page"), "legible": item.get("legible"), "type": item.get("type")},
    ),
).load()
pages = [d for d in docs if d.metadata["type"] == "page"]
keep = [d for d in pages if d.metadata["legible"]]
print(f"{len(pages)} page document(s), {len(keep)} legible")
for d in pages:
    print(d.metadata, repr(d.page_content[:80]))
```

Output:

```text
1 page document(s), 0 legible
{'page': 1, 'legible': False, 'type': 'page'} 'Dummy PDF file'
```

## JavaScript

Node 18+, `npm install apify-client`.

```javascript
// PDF, Image & Word to Text and Markdown (OCR).
//   npm install apify-client && export APIFY_TOKEN=...
//   node pdf-image-text-markdown-extractor.mjs https://example.com/report.pdf
import { ApifyClient } from 'apify-client';

const url = process.argv[2] ?? 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('atarivo/pdf-image-text-markdown-extractor').call(
    { url }, { maxTotalChargeUsd: 0.1 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const doc = items.find((r) => r.type === 'document');
console.log(`pages: ${doc.pages}, tables: ${doc.tables_found}`);
for (const p of items.filter((r) => r.type === 'page')) {
    console.log(`page ${p.page}: legible=${p.legible} ocr=${p.ocr}`);
    console.log(p.markdown.slice(0, 200));
}
const rec = await client.keyValueStore(run.defaultKeyValueStoreId).getRecord('chunks.json');
const chunks = typeof rec.value === 'string' ? JSON.parse(rec.value) : rec.value;
console.log(`chunks: ${chunks.chunks.length}`);
```

Output:

```text
pages: 1, tables: 0
page 1: legible=false ocr=false
Dummy PDF file
chunks: 1
```

## curl

```bash
#!/usr/bin/env bash
# PDF, Image & Word to Text and Markdown (OCR): synchronous run, the dataset rows come back as JSON.
# export APIFY_TOKEN=... ; ./pdf-image-text-markdown-extractor.sh [PDF_URL]
set -euo pipefail
URL=${1:-https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf}
curl -sS -X POST "https://api.apify.com/v2/acts/atarivo~pdf-image-text-markdown-extractor/run-sync-get-dataset-items?maxTotalChargeUsd=0.1" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d "{\"url\": \"$URL\", \"outputs\": [\"text\", \"markdown\"]}"
```

Output (signed links shortened to `<signed-url>`):

```json
[{
  "type": "page",
  "page": 1,
  "text": "Dummy PDF file",
  "markdown": "Dummy PDF file",
  "tables": [],
  "facts": {
    "width_pt": 595,
    "height_pt": 842,
    "rotation": 0,
    "fonts": [
      "Arial-BoldMT"
    ],
    "images": 0,
    "ocr_attempted": false,
    "chars": 14,
    "text_source": "text-layer",
    "legibility_score": 1,
    "legibility_reason": "only 14 characters — below 60",
    "tables": 0
  },
  "ocr": false,
  "legible": false
},
{
  "type": "document",
  "page": null,
  "file_type": "pdf",
  "file_name": null,
  "bytes": 13264,
  "pages": 1,
  "pages_processed": 1,
  "pages_empty": 0,
  "pages_ocr": 0,
  "tables_found": 0,
  "chunks": 1,
  "markdown_url": "<signed-url>",
  "chunks_url": null,
  "truncated": false,
  "reason": null,
  "unit": "page",
  "chars": null,
  "elapsed_s": 0.41
}]
```

## Tips

- Filter on `legible` before you embed: an illegible page is better left out than indexed as noise.
- `document.md` and `chunks.json` live in the run's default key-value store; download what you keep.
- Set a cost cap on every run; the Actor stops cleanly at it and reports `truncated: true`.
