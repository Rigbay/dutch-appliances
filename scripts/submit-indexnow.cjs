/**
 * Post-build IndexNow submission script.
 * Submits ALL page URLs to IndexNow APIs (Bing, Yandex, Seznam) after every build.
 * 
 * Usage: node scripts/submit-indexnow.cjs
 * 
 * Reads the sitemap from Astro's build output, extracts all URLs,
 * and submits them in batches to the IndexNow protocol endpoints.
 * 
 * IndexNow key: 107f03c08e12ebfc07a124ba28b5dd6f
 * Site: https://rigbay.github.io/dutch-appliances
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const KEY = '107f03c08e12ebfc07a124ba28b5dd6f';
const BASE = 'https://rigbay.github.io/dutch-appliances';
const SITEMAP_PATH = path.join(__dirname, '..', 'dist', 'sitemap-0.xml');

// IndexNow endpoints
const ENDPOINTS = [
  'https://api.indexnow.org/indexnow',
  'https://www.bing.com/indexnow',
  'https://yandex.com/indexnow',
  'https://search.seznam.cz/indexnow',
];

// Also try the key-location GET method (Bing specifically)
const BING_KEY_URL = `https://www.bing.com/indexnow/getat?url=${encodeURIComponent(BASE + '/' + KEY + '.txt')}&key=${KEY}&keyLocation=${encodeURIComponent(BASE + '/' + KEY + '.txt')}`;

function postJSON(url, data) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(data);
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(body)
      },
      timeout: 15000
    };
    const req = https.request(options, (res) => {
      let buf = '';
      res.on('data', (c) => { buf += c; });
      res.on('end', () => resolve({ status: res.statusCode, body: buf }));
    });
    req.on('error', (e) => reject(e));
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.write(body);
    req.end();
  });
}

async function main() {
  console.log('🔍 IndexNow — submitting URLs to search engines...\n');

  // Read all sitemaps
  const distDir = path.join(__dirname, '..', 'dist');
  if (!fs.existsSync(distDir)) {
    console.error('❌ dist/ directory not found. Run `npx astro build` first.');
    process.exit(1);
  }

  // Extract URLs from sitemap XML
  const files = fs.readdirSync(distDir).filter(f => f.startsWith('sitemap-') && f.endsWith('.xml'));
  if (files.length === 0) {
    console.error('❌ No sitemap files found in dist/');
    process.exit(1);
  }

  const urls = [];
  for (const file of files) {
    const xml = fs.readFileSync(path.join(distDir, file), 'utf-8');
    const matches = xml.matchAll(/<loc>([^<]+)<\/loc>/g);
    for (const m of matches) {
      urls.push(m[1].trim());
    }
  }

  console.log(`📊 Found ${urls.length} URLs in ${files.length} sitemap(s)`);

  if (urls.length === 0) {
    console.log('⚠️  No URLs to submit. Exiting.');
    return;
  }

  // Submit in batches of 100 (IndexNow limits to 10K per batch)
  const BATCH_SIZE = 100;
  let totalSubmitted = 0;
  let totalErrors = 0;

  for (let i = 0; i < urls.length; i += BATCH_SIZE) {
    const batch = urls.slice(i, i + BATCH_SIZE);
    const payload = {
      host: new URL(BASE).host,
      key: KEY,
      keyLocation: `${BASE}/${KEY}.txt`,
      urlList: batch
    };

    for (const endpoint of ENDPOINTS) {
      const engine = endpoint.includes('bing') ? 'Bing' :
                     endpoint.includes('yandex') ? 'Yandex' :
                     endpoint.includes('seznam') ? 'Seznam' :
                     'IndexNow';
      try {
        const result = await postJSON(endpoint, payload);
        if (result.status === 200 || result.status === 202) {
          console.log(`  ✅ ${engine}: ${result.status} (${batch.length} URLs)`);
          totalSubmitted += batch.length;
        } else {
          console.log(`  ⚠️  ${engine}: ${result.status} — ${result.body.substring(0, 100)}`);
          totalErrors++;
        }
      } catch (err) {
        console.log(`  ❌ ${engine}: ${err.message}`);
        totalErrors++;
      }
    }
  }

  // Also ping Bing's alternate endpoint
  try {
    const bingCheck = await postJSON(BING_KEY_URL, {});
    console.log(`\n🔑 Bing key verification: ${bingCheck.status}`);
  } catch (err) {
    console.log(`\n🔑 Bing key verification: failed (${err.message})`);
  }

  console.log(`\n✅ Done. ${totalSubmitted} URLs submitted, ${totalErrors} errors.`);
}

main().catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});
