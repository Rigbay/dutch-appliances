#!/usr/bin/env node
const fs = require('node:fs');
const path = require('node:path');

const dist = path.join(process.cwd(), 'dist');
const base = '/dutch-appliances';
const origin = 'https://rigbay.github.io';

if (!fs.existsSync(dist)) {
  console.error(`dist directory not found: ${dist}`);
  process.exit(1);
}

const exts = new Set(['.html', '.xml', '.txt', '.json', '.svg']);
let changedFiles = 0;
let replacements = 0;

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (exts.has(path.extname(entry.name))) fixFile(full);
  }
}

function countReplace(input, regex, replacement) {
  let count = 0;
  const output = input.replace(regex, (...args) => {
    count += 1;
    return typeof replacement === 'function' ? replacement(...args) : replacement;
  });
  replacements += count;
  return output;
}

function fixFile(file) {
  const before = fs.readFileSync(file, 'utf8');
  let s = before;

  // Root-absolute internal paths break on project GitHub Pages. Prefix them with the repo base.
  s = countReplace(s, /\b(href|src|content|url)=(["'])\/(?!dutch-appliances(?:\/|$)|\/|#)([^"' >]*)\2/g, (_m, attr, quote, rest) => {
    return `${attr}=${quote}${base}/${rest}${quote}`;
  });

  // Inline CSS url('/...') / url("/...") / url(/...) references.
  s = countReplace(s, /url\((['"]?)\/(?!dutch-appliances(?:\/|$)|\/|#)([^)'" ]+)\1\)/g, (_m, quote, rest) => {
    return `url(${quote}${base}/${rest}${quote})`;
  });

  // JSON-LD/canonical URLs manually built against the origin must include the repo base.
  s = countReplace(s, new RegExp(`${origin.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\/(?!dutch-appliances(?:\/|$)|#)([^"'<>\\s)]*)`, 'g'), (_m, rest) => {
    return `${origin}${base}/${rest}`;
  });

  // A few old internal links used /reviews/<slug>/, but generated review pages live at /<slug>/.
  s = countReplace(s, /\/dutch-appliances\/reviews\//g, `${base}/`);

  if (s !== before) {
    fs.writeFileSync(file, s);
    changedFiles += 1;
  }
}

walk(dist);
console.log(`GitHub Pages base fix: ${replacements} replacements across ${changedFiles} files`);
