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
