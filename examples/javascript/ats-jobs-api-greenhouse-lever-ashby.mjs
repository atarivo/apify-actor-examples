// ATS Jobs API: Greenhouse, Lever & Ashby.
//   npm install apify-client && export APIFY_TOKEN=... && node ats-jobs-api-greenhouse-lever-ashby.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('atarivo/ats-jobs-api-greenhouse-lever-ashby').call(
    { boards: ['lever:palantir', 'ashby:ashby'], maxJobsPerBoard: 3 }, { maxTotalChargeUsd: 0.05 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const j of items.filter((r) => !r.error)) {
    console.log(`${j.ats} | ${j.title} | ${j.location} | ${j.dedup_key}`);
}
