import { readdirSync, readFileSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const skippedDirectories = new Set(['.git', 'dist', 'node_modules']);
const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const identityBearingReferral = /https?:\/\/(?:www\.)?(?:beehiiv\.com|descript\.com|opus\.pro|trendspider\.com)\/\?via=/i;
const findings = [];
let filesChecked = 0;

function* walk(directory = repoRoot) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    if (entry.isDirectory() && skippedDirectories.has(entry.name)) continue;
    const path = join(directory, entry.name);
    if (entry.isDirectory()) yield* walk(path);
    else if (entry.isFile()) yield path;
  }
}

for (const file of walk()) {

  let source;
  try {
    source = readFileSync(file, 'utf8');
  } catch {
    continue;
  }
  filesChecked += 1;

  if (identityBearingReferral.test(source)) {
    findings.push(`${relative(repoRoot, file)}: referral tracking requires an anonymous brand-owned ID`);
  }
}

if (findings.length > 0) {
  console.error('Public identity audit failed:');
  for (const finding of findings) console.error(`- ${finding}`);
  process.exit(1);
}

console.log(`Public identity audit passed (${filesChecked} files checked).`);
