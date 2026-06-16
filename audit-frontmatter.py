#!/usr/bin/env python3
"""Find and fix articles with missing rating/affiliateLink in products."""
import os, re, yaml

OUT_DIR = "/home/cls/kieskeuken/src/content/reviews"

def check_article(path):
    with open(path) as f:
        content = f.read()
    
    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    
    fm_text = parts[1]
    try:
        fm = yaml.safe_load(fm_text)
    except:
        return f"YAML parse error"
    
    issues = []
    
    # Check description length
    desc = fm.get("description", "")
    if len(desc) > 180:
        issues.append(f"description too long ({len(desc)} chars)")
    
    # Check products
    products = fm.get("products", [])
    if not products:
        issues.append("no products")
    else:
        for i, p in enumerate(products):
            p_issues = []
            if "rating" not in p or p["rating"] is None:
                p_issues.append("missing rating")
            if "affiliateLink" not in p or p["affiliateLink"] is None:
                p_issues.append("missing affiliateLink")
            if p_issues:
                issues.append(f"product[{i}]: {', '.join(p_issues)}")
    
    # Check pros/cons count
    pros = fm.get("pros", [])
    cons = fm.get("cons", [])
    if len(pros) > 3:
        issues.append(f"too many pros ({len(pros)})")
    if len(cons) > 3:
        issues.append(f"too many cons ({len(cons)})")
    
    # Check related count
    related = fm.get("related", [])
    if len(related) < 6:
        issues.append(f"too few related ({len(related)})")
    
    return issues if issues else None

# Scan all articles
print("Scanning all articles...")
problem_files = []
for fname in sorted(os.listdir(OUT_DIR)):
    if not fname.endswith(".md"):
        continue
    path = os.path.join(OUT_DIR, fname)
    issues = check_article(path)
    if issues:
        problem_files.append((fname, issues))
        print(f"  {fname}: {'; '.join(issues)}")

print(f"\nTotal problems: {len(problem_files)} files")
