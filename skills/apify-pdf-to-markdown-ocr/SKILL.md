---
name: apify-pdf-to-markdown-ocr
description: Turn a PDF, scanned image (PNG, JPEG, TIFF) or Word .docx into per-page text, Markdown, tables and RAG chunks with page spans, using the Atarivo "PDF to Markdown & Text Extractor with OCR" Actor on Apify through the Apify MCP server or the apify-client library. Use when a task needs the text of a document the agent cannot read directly, when a PDF is scanned and needs OCR, when tables must come out as rows, or when a document must be chunked for retrieval. Pay per page, first page of every run free, no AI model inside, no login to anything.
license: MIT
metadata:
  author: atarivo
  version: "1.0"
  actor: atarivo/pdf-image-text-markdown-extractor
  store: https://apify.com/atarivo/pdf-image-text-markdown-extractor
---

# PDF, image and Word to Markdown with OCR (Apify Actor)

One Actor, deterministic: it reads the text layer first and runs Tesseract OCR only on pages that
have no usable text. The same file gives the same output every time. It calls no AI model and
makes no network request except to fetch the URL you give it.

**Our line, said plainly:** this tool never logs in anywhere, never uses a credential of yours, and
never circumvents anything. It fetches a file you can already reach without an account, or the
bytes you hand it. If the document sits behind a login, download it yourself first and pass the
bytes as `base64`, or upload it to your own Apify key-value store and pass that record URL.

## When to use it

- The agent must read a PDF, scan or Word file it cannot open itself.
- The PDF is scanned (image-only) and needs OCR.
- Tables must come back as rows, not as flattened text.
- The document must be split into retrieval chunks that remember which pages they came from.

Do not use it for HTML pages (use a web fetch tool), for spreadsheets, or for files over 50 MB.

## Setup: Apify MCP server (preferred for agents)

Point your MCP client at the hosted server and load this Actor as a tool:

```text
https://mcp.apify.com?tools=atarivo/pdf-image-text-markdown-extractor
```

Authentication is OAuth on first connect, or the header `Authorization: Bearer <APIFY_TOKEN>`
(Apify Console -> Settings -> API & Integrations). Claude Code:

```bash
claude mcp add apify "https://mcp.apify.com?tools=atarivo/pdf-image-text-markdown-extractor" -t http
```

The tool is named `atarivo--pdf-image-text-markdown-extractor` (Apify turns `/` into `--`).
Listing one Actor also loads Apify's run and storage tools, which you use to read the dataset
and the two files the run writes.

## Setup: apify-client (Python or JavaScript)

```bash
pip install apify-client
export APIFY_TOKEN=...
```

```python
import os
from decimal import Decimal
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/pdf-image-text-markdown-extractor").call(
    run_input={"url": "https://example.com/report.pdf", "outputs": ["markdown", "chunks"]},
    max_total_charge_usd=Decimal("0.50"),          # hard cap for this run
)
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
pages = [r for r in rows if r["type"] == "page"]
document = next(r for r in rows if r["type"] == "document")
```

Full examples in Python, JavaScript and curl: `examples/` and
`tutorials/pdf-image-text-markdown-extractor.md` in this repository.

## Input

| Field | Type | Default | Meaning |
|---|---|---|---|
| `url` | string | | Public http(s) link to a PDF, PNG, JPEG, TIFF or .docx (up to 50 MB), or the URL of a record in your own Apify key-value store. Give `url` or `base64`, not both. |
| `base64` | string | | The file itself, base64-encoded (a `data:` URI prefix is accepted), up to 20 MB decoded. |
| `fileName` | string | | Optional name such as `report.pdf`; the type is always sniffed from the bytes. |
| `ocr` | `auto` / `never` / `always` | `auto` | `auto` runs OCR only on pages whose text layer is empty or illegible. `never` fails on an image (images have no text layer). |
| `maxPages` | integer 1-2000 | 500 | Stop after this many pages. For .docx a "page" is 3,000 characters. |
| `outputs` | array | all four | Any of `text`, `markdown`, `chunks`, `tables`. Leave `tables` out and no table event is charged. |
| `chunkChars` | integer 200-20000 | 1500 | Target size of each RAG chunk. Chunks break at paragraph and table boundaries. |

## Output

One dataset row per page, then one `document` row:

```json
{"type": "page", "page": 2, "text": "...", "markdown": "### Harvest by crop\n\n| Crop | Beds | Harvest (kg) |...",
 "tables": [{"index": 0, "rows": [["Crop", "Beds", "Harvest (kg)"], ["Tomato", "12", "340"]], "markdown": "..."}],
 "facts": {"text_source": "text-layer", "legibility_score": 1.0, "fonts": ["Helvetica"], "images": 0, "chars": 276},
 "ocr": false, "legible": true}
```

```json
{"type": "document", "pages": 2, "pages_processed": 2, "pages_ocr": 0, "tables_found": 1, "chunks": 3,
 "markdown_url": "https://api.apify.com/v2/key-value-stores/.../records/document.md",
 "chunks_url": "https://api.apify.com/v2/key-value-stores/.../records/chunks.json",
 "truncated": false, "reason": null}
```

- `document.md` is the whole document as Markdown with `<!-- page N -->` markers.
- `chunks.json` is `{"chunks": [{"index", "text", "page_start", "page_end", "chars"}]}`: feed it
  straight into a vector store; each chunk knows the pages it spans.
- `legible: false` is an explicit verdict (empty page or OCR noise), never a silent empty string.
- A URL that answers with an HTTP error (404 and the like) produces one `error` row, **billed as
  one page** (`page-extracted`).

## Cost and budget

- `$0.001` per page delivered (`page-extracted`), plus `$0.005` per page whose text came from OCR
  (`page-ocr`) and `$0.003` per table delivered (`table-extracted`). The first page of every run is
  free, add-ons included. Blank pages are free. Platform usage is included: no "+usage" line.
- Always set a cap: `max_total_charge_usd` in the client, or **Max cost per run** in the Console.
  The Actor stops cleanly at the cap and marks the document row `truncated: true, reason: "budget"`.
- Worked example from those prices (first page free): a 100-page text PDF with no tables is
  `99 x $0.001 = $0.099`; the same document scanned adds `99 x $0.005` of OCR, `$0.594` in all.
  Say the number to the user before running a large document.
- A link that returns an HTTP error (such as 404) produces one error row, billed as one page.
- Invalid input (both or neither of `url` and `base64`, an unsupported type, a private address, a
  file over the limit) fails at once and costs nothing.

## Edge cases the agent should handle

- **Image input with `ocr: "never"`** fails with a clear message: use `auto`.
- **Private documents:** the Actor cannot and will not log in. Pass `base64`, or upload the file to
  your own key-value store in the Apify Console and pass that record URL; the run reads it with the
  run's own token.
- **Word files** have no pages: each 3,000 characters of extracted text is one billed row. OCR is
  never charged for .docx.
- **Truncation:** `reason: "maxPages"` means raise `maxPages`; `reason: "budget"` means raise the cap.
- **Retention:** the run's dataset and files live in your Apify account for your plan's retention
  period (7 days for unnamed storages on most plans). Download what you want to keep. The document
  is processed inside your run only; its text is never logged or copied out.

## Related

- The job-board data skill in this repository: `skills/apify-ats-jobs-data/SKILL.md`.
- Store page and agent-readable listing: https://apify.com/atarivo/pdf-image-text-markdown-extractor
  and https://apify.com/atarivo/pdf-image-text-markdown-extractor.md
- Not affiliated with or endorsed by Adobe, Microsoft or the Tesseract project.
