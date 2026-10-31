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
