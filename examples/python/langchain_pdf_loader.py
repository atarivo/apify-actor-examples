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
