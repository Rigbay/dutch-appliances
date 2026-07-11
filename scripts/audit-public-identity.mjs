import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const skippedDirectories = new Set(['.git', 'dist', 'node_modules']);
const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const forbidden = [
  {
    label: 'referral tracking requires an anonymous brand-owned ID',
    pattern: /https?:\/\/(?:www\.)?(?:beehiiv\.com|descript\.com|opus\.pro|trendspider\.com)\/\?via=/i,
  },
  {
    label: 'personal identity token is not allowed in the public repository',
    pattern: /\b(?:anonymous-operator(?:[ -]hilman)?|anonymous-operator(?:[ -]hilman)?)\b/i,
  },
  {
    label: 'copied private agent context is not allowed in the public repository',
    pattern: /(?:^|\n)#\s*(?:USER|SOUL|MEMORY)\.md\b/i,
  },
];
const forbiddenPaths = [
  {
    label: 'agent execution logs are not public source',
    pattern: /(?:^|\/)delegate(?:-cc)?-log-[^/]*\.md$/i,
  },
  {
    label: 'private operator state is not public source',
    pattern: /(?:^|\/)private\//i,
  },
];
const findings = [];
let filesChecked = 0;

const trackedFiles = execFileSync('git', ['ls-files', '-z'], { cwd: repoRoot })
  .toString('utf8')
  .split('\0')
  .filter(Boolean)
  .filter((repoPath) => !repoPath.split('/').some((part) => skippedDirectories.has(part)));

for (const repoPath of trackedFiles) {
  const file = join(repoRoot, repoPath);
  for (const rule of forbiddenPaths) {
    if (rule.pattern.test(repoPath)) findings.push(`${repoPath}: ${rule.label}`);
  }
  if (repoPath === 'scripts/audit-public-identity.mjs') continue;

  let source;
  try {
    source = readFileSync(file, 'utf8');
  } catch {
    continue;
  }
  filesChecked += 1;

  for (const rule of forbidden) {
    if (rule.pattern.test(source)) findings.push(`${repoPath}: ${rule.label}`);
  }
}

if (findings.length > 0) {
  console.error('Public identity audit failed:');
  for (const finding of findings) console.error(`- ${finding}`);
  process.exit(1);
}

console.log(`Public identity audit passed (${filesChecked} files checked).`);
