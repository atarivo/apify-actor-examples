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
