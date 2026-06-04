#!/usr/bin/env python3
"""Debug: check what product names exist and what models they contain."""
import json, re

ASIN_FILE = "scripts/known-asins.json"
d = json.load(open(ASIN_FILE))
SKIP = {'de', 'en', 'het', 'van', 'met', 'voor', 'x', 'and', 'en/'}

safe = {}
for raw_name, asin in d["known_asins"].items():
    clean = raw_name.strip("*").strip().lower()
    if asin not in d["collisions"] or asin == "B07HFY6N2R":
        safe[clean] = asin

MODEL_RE = re.compile(r'\b([A-Z0-9]{2,}(?:/\d+)?)\b')

# Check first 30 articles for product names that DO match
import os
reviews_dir = "src/content/reviews"
matches_found = 0
total_products = 0

for fname in sorted(os.listdir(reviews_dir)):
    if not fname.endswith(".md"):
        continue
    content = open(os.path.join(reviews_dir, fname)).read()
    
    # Also get the first few lines which have topline links
    lines = content.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r'^\s*- name:\s+(.+)$', line)
        if not m:
            continue
        name = m.group(1).strip().strip("\"'")
        total_products += 1
        
        n_lower = name.lower().strip()
        prod_models = set()
        for m2 in MODEL_RE.finditer(name + " " + name.upper()):
            code = m2.group(1)
            if len(code) < 4 or code.lower() in ['series','plus','ultra','premium','max','pro','range','dark']:
                continue
            prod_models.add(code)
        
        found = False
        for known, asin in safe.items():
            known_models = set()
            for m2 in MODEL_RE.finditer(known + " " + known.upper()):
                code = m2.group(1)
                if len(code) < 4 or code.lower() in ['series','plus','ultra','premium','max','pro','range','dark']:
                    continue
                known_models.add(code)
            
            if prod_models & known_models:
                matches_found += 1
                found = True
                break
        
        if not found:
            prod_tokens = set(n_lower.split()) - SKIP
            best_score = 0
            best_known = None
            best_asin = None
            for known, asin in safe.items():
                known_tokens = set(known.split()) - SKIP
                if known_tokens:
                    inter = prod_tokens & known_tokens
                    score = len(inter) / len(known_tokens)
                    if score > best_score:
                        best_score = score
                        best_known = known
                        best_asin = asin
            if best_score >= 0.55:
                matches_found += 1

print(f"Total products scanned: {total_products}")
print(f"Matches found: {matches_found}")

# Show 10 products that DIDN'T match, to understand why
print("\n--- NON-MATCHING SAMPLE (first 10) ---")
count = 0
for fname in sorted(os.listdir(reviews_dir)):
    if not fname.endswith(".md") or count >= 10:
        continue
    content = open(os.path.join(reviews_dir, fname)).read()
    lines = content.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r'^\s*- name:\s+(.+)$', line)
        if not m:
            continue
        name = m.group(1).strip().strip("\"'")
        n_lower = name.lower().strip()
        prod_models = set()
        for m2 in MODEL_RE.finditer(name + " " + name.upper()):
            code = m2.group(1)
            if len(code) < 4 or code.lower() in ['series','plus','ultra','premium','max','pro','range','dark']:
                continue
            prod_models.add(code)
        
        found = False
        for known, asin in safe.items():
            known_models = set()
            for m2 in MODEL_RE.finditer(known + " " + known.upper()):
                code = m2.group(1)
                if len(code) < 4 or code.lower() in ['series','plus','ultra','premium','max','pro','range','dark']:
                    continue
                known_models.add(code)
            if prod_models & known_models:
                found = True
                break
            prod_tokens = set(n_lower.split()) - SKIP
            known_tokens = set(known.split()) - SKIP
            if known_tokens:
                inter = prod_tokens & known_tokens
                if len(inter) / len(known_tokens) >= 0.55:
                    found = True
                    break
        
        if not found:
            count += 1
            models_str = ", ".join(prod_models) if prod_models else "(none)"
            print(f"\n  [{fname}] {name[:50]}")
            print(f"    models: {models_str}")
            best_score = 0
            best_match = None
            for known, asin in safe.items():
                known_tokens = set(known.split()) - SKIP
                if known_tokens:
                    inter = set(n_lower.split()) - SKIP & known_tokens
                    score = len(inter) / len(known_tokens)
                    if score > best_score:
                        best_score = score
                        best_match = known
            print(f"    best token: '{best_match}' (score: {best_score:.2f})")