// Workable, Recruitee, Personio & Teamtailor Jobs API.
//   npm install apify-client && export APIFY_TOKEN=... && node ats-jobs-api-workable-recruitee-personio-teamtailor.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('atarivo/ats-jobs-api-workable-recruitee-personio-teamtailor').call(
    { boards: ['https://career.teamtailor.com'], maxJobsPerBoard: 5 }, { maxTotalChargeUsd: 0.05 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const j of items.filter((r) => !r.error)) {
    console.log(`${j.ats} | ${j.title} | ${j.location} | remote: ${j.remote}`);
}
