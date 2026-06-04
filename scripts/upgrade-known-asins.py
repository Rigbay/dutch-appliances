#!/usr/bin/env python3
"""Replace Amazon search URLs with known ASINs by matching product MODEL NUMBERS.
Also does loose token matching as fallback.

Strategy:
1. Extract model numbers from both article product names and known ASIN entries
2. Match by model number first (reliable, unambiguous)
3. Fall back to token matching with 0.6 threshold for products without model numbers

Run from /home/cls/kieskeuken/
"""

import json, re, os

REVIEWS_DIR = "src/content/reviews"
ASIN_FILE = "scripts/known-asins.json"

# Model number patterns: AF400EU, NA352/00, HD9650/90, EY8018, etc.
MODEL_RE = re.compile(r'\b([A-Z0-9]{2,}(?:/\d+)?)\b')

# Skip tokens common in search queries but not useful for matching
SKIP_TOKENS = {'de', 'en', 'het', 'van', 'met', 'voor', 'x', '&', 'en/'}


def load_asins():
    data = json.load(open(ASIN_FILE))
    raw = data["known_asins"]
    collisions = set(data["collisions"].keys())

    safe = {}
    for raw_name, asin in raw.items():
        clean = raw_name.strip("*").strip().lower()
        if asin not in collisions or asin == "B07HFY6N2R":
            safe[clean] = asin
    return safe, collisions


def extract_model_numbers(name):
    """Extract meaningful model/part numbers from a product name."""
    models = set()
    for match in MODEL_RE.finditer(name):
        m = match.group(1)
        # Skip short codes that are likely common words
        if len(m) < 4:
            continue
        # Skip if it looks like a generic category word
        if m.lower() in ['series', 'plus', 'ultra', 'premium', 'max', 'pro', 'range', 'dark']:
            continue
        models.add(m)
    return models


def token_match_score(product_tokens, known_tokens):
    """Jaccard-like score for token overlap."""
    if not known_tokens:
        return 0
    product_set = set(product_tokens) - SKIP_TOKENS
    known_set = set(known_tokens) - SKIP_TOKENS
    if not known_set:
        return 0
    intersection = product_set & known_set
    return len(intersection) / len(known_set)


def find_best_match(product_name, safe_map):
    """Find best ASIN for a product name. Returns (asin, matched_known, method, score)."""
    product_lower = product_name.lower().strip()
    product_models = extract_model_numbers(product_name + " " + product_name.upper())
    
    best_model_match = None
    best_model_known = None
    best_token_match = None
    best_token_known = None
    best_token_score = 0

    for known, asin in safe_map.items():
        # Model number matching
        known_models = extract_model_numbers(known)
        shared_models = product_models & known_models
        if shared_models:
            if best_model_match is None:
                best_model_match = asin
                best_model_known = known

        # Token matching
        prod_tokens = product_lower.split()
        known_tokens = known.split()
        score = token_match_score(prod_tokens, known_tokens)
        if score > best_token_score:
            best_token_score = score
            best_token_match = asin
            best_token_known = known

    # Prefer model number match (it's unambiguous)
    if best_model_match:
        return best_model_match, best_model_known, "model", 1.0

    # Token match with threshold
    if best_token_score >= 0.55:
        return best_token_match, best_token_known, "token", best_token_score

    return None, None, None, 0


def process_article(filepath, safe_map):
    """Process one article — replace search URLs with ASIN links."""
    content = open(filepath).read()
    lines = content.split("\n")

    current_product_name = None
    replacements = 0
    new_lines = []

    for line in lines:
        # Track current product name from frontmatter
        name_match = re.match(r'^(\s*)- name:\s+(.+)$', line)
        if name_match:
            current_product_name = name_match.group(2).strip().strip("\"'")
            new_lines.append(line)
            continue

        # Replace affiliateLink search URLs for our current product
        if current_product_name and 'affiliateLink:' in line and 'amazon.nl/s?k=' in line:
            asin, matched_known, method, score = find_best_match(current_product_name, safe_map)
            if asin:
                indent = re.match(r'^(\s*)', line).group(1)
                new_line = f'{indent}affiliateLink: https://www.amazon.nl/dp/{asin}?tag=kieskeukennl-21'
                new_lines.append(new_line)
                # Truncate long names for display
                name_short = current_product_name[:45]
                print(f"  ✅ {name_short:<45} → {asin} ({method}, {score:.2f})")
                replacements += 1
                current_product_name = None
                continue

        current_product_name = None
        new_lines.append(line)

    if replacements > 0:
        with open(filepath, "w") as f:
            f.write("\n".join(new_lines))
        return replacements
    return 0


def main():
    safe_map, _ = load_asins()
    
    print(f"Safe ASIN entries: {len(safe_map)}")
    print(f"{'='*60}")
    
    total_replaced = 0
    changed_files = []
    model_matches = 0
    token_matches = 0

    for fname in sorted(os.listdir(REVIEWS_DIR)):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(REVIEWS_DIR, fname)
        replaced = process_article(path, safe_map)
        if replaced > 0:
            total_replaced += replaced
            changed_files.append(fname)

    print(f"\n{'='*60}")
    print(f"Articles scanned: {len([f for f in os.listdir(REVIEWS_DIR) if f.endswith('.md')])}")
    print(f"Articles with replacements: {len(changed_files)}")
    print(f"Search URLs → ASIN links: {total_replaced}")
    
    if changed_files:
        changed_str = "\n".join(f"  - {f}" for f in changed_files)
        print(f"\nChanged files ({len(changed_files)}):\n{changed_str}")

if __name__ == "__main__":
    main()