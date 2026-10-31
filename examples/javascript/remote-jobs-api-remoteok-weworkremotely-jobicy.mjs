// Remote Jobs API: Remote OK, We Work Remotely & Jobicy.
//   npm install apify-client && export APIFY_TOKEN=... && node remote-jobs-api-remoteok-weworkremotely-jobicy.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('atarivo/remote-jobs-api-remoteok-weworkremotely-jobicy').call(
    { sources: ['weworkremotely', 'jobicy'], maxJobsPerSource: 5 }, { maxTotalChargeUsd: 0.05 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const j of items.filter((r) => !r.error)) {
    // keep the credit: each board asks for a link back wherever its jobs are shown
    console.log(`${j.source} | ${j.title} | ${j.remote_region} | ${j.source_url} (${j.attribution})`);
}
