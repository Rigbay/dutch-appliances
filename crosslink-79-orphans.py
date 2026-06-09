#!/usr/bin/env python3
"""
Cross-link all 79 orphan articles with contextual inline links.
For each orphan, find 3-5 related articles and insert natural inline links.
Updates enrichment-plan.json with all new mappings.
"""
import os, re, json, sys
from collections import defaultdict

REVIEWS_DIR = "src/content/reviews"
ENRICHMENT_PATH = "enrichment-plan.json"

os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

# ── Load all articles ──────────────────────────────────────────────
def load_article(slug):
    path = os.path.join(REVIEWS_DIR, f"{slug}.md")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        raw = f.read()
    m = re.search(r'^---\n(.*?)\n---\n(.*)', raw, re.DOTALL)
    if not m:
        return None
    fm_text = m.group(1)
    body = m.group(2)
    cat_m = re.search(r'category:\s*(\S+)', fm_text)
    title_m = re.search(r'title:\s*(.+)', fm_text)
    desc_m = re.search(r'description:\s*(.+)', fm_text)
    return {
        'slug': slug,
        'category': cat_m.group(1) if cat_m else 'overig',
        'title': title_m.group(1).strip() if title_m else '',
        'description': desc_m.group(1).strip() if desc_m else '',
        'body': body,
        'raw': raw,
        'fm_text': fm_text,
    }

all_slugs = [f.replace('.md', '') for f in os.listdir(REVIEWS_DIR) if f.endswith('.md')]
articles = {}
for s in all_slugs:
    a = load_article(s)
    if a:
        articles[s] = a

print(f"Loaded {len(articles)} articles")

# Load enrichment plan
with open(ENRICHMENT_PATH) as f:
    plan = json.load(f)

planned = set(plan.keys())
orphan_slugs = [s for s in all_slugs if s + '.md' not in planned]
print(f"Orphans: {len(orphan_slugs)}")

# ── Build keyword index for matching ───────────────────────────────
def extract_keywords(slug, title, description):
    """Extract meaningful Dutch keywords from slug/title/description."""
    text = f"{slug} {title} {description}".lower()
    # Remove common stopwords and year
    text = re.sub(r'\b2026\b', '', text)
    text = re.sub(r'\b(de|het|een|van|voor|met|die|dat|en|of|op|in|aan|bij|als|ook|dan|nog|wel|niet|geen|welke|jouw|onze|beste|koopgids|vergelijking|gids|vs|versus)\b', '', text)
    # Extract meaningful tokens
    tokens = set(re.findall(r'[a-z]{4,}', text))
    return tokens

# Build keyword index for all articles
keyword_index = {}
for s, a in articles.items():
    keyword_index[s] = extract_keywords(s, a['title'], a['description'])

# ── Find related articles for each orphan ──────────────────────────
def find_related(orphan_slug, orphan_data, n=5):
    """Find n best related articles for an orphan."""
    orphan_cat = orphan_data['category']
    orphan_kw = keyword_index[orphan_slug]
    
    candidates = []
    for s, a in articles.items():
        if s == orphan_slug:
            continue
        # Score: category match + keyword overlap
        score = 0
        if a['category'] == orphan_cat:
            score += 3
        elif a['category'] in ('keuken', 'huishoudelijk') and orphan_cat in ('keuken', 'huishoudelijk'):
            score += 1  # adjacent categories
        
        kw_overlap = len(orphan_kw & keyword_index[s])
        score += kw_overlap * 2
        
        # Bonus for slug similarity (e.g., beste-koekenpan → koekenpan-vs-braadpan)
        orphan_base = re.sub(r'^(beste-|vs-)', '', orphan_slug)
        other_base = re.sub(r'^(beste-|vs-)', '', s)
        if orphan_base in other_base or other_base in orphan_base:
            score += 4
        
        candidates.append((s, score, a))
    
    candidates.sort(key=lambda x: -x[1])
    return [c for c in candidates[:n] if c[1] > 0]

# ── Find natural insertion point in body ───────────────────────────
def find_insertion_point(body, keywords, orphan_slug, orphan_title):
    """Find a natural place to insert an inline link in the body text."""
    # Try to find a paragraph that mentions one of the keywords
    paragraphs = body.split('\n\n')
    
    # Score each paragraph for keyword matches
    best_para_idx = -1
    best_score = 0
    best_keyword = None
    
    for i, para in enumerate(paragraphs):
        if len(para) < 50:
            continue
        if '[/dutch-appliances/' in para:
            continue  # already has a link, but we can still add
        
        for kw in keywords:
            if kw.lower() in para.lower():
                score = len(para)  # prefer longer paragraphs
                if score > best_score:
                    best_score = score
                    best_para_idx = i
                    best_keyword = kw
    
    if best_para_idx < 0:
        # Fallback: find any substantial paragraph
        for i, para in enumerate(paragraphs):
            if len(para) > 80 and '[/dutch-appliances/' not in para:
                best_para_idx = i
                best_keyword = None
                break
    
    return best_para_idx, best_keyword

def make_anchor_text(orphan_slug, orphan_title, keyword):
    """Generate natural Dutch anchor text."""
    title_lower = orphan_title.lower()
    
    # Determine if it's a comparison or single-product guide
    if 'vs' in orphan_slug.lower() or 'versus' in orphan_slug.lower():
        # It's a comparison
        if keyword:
            return f"onze {orphan_title.lower()}"
        return f"onze {orphan_title.lower()}"
    else:
        # Single product guide
        if keyword:
            return f"onze {orphan_title.lower()}"
        return f"onze {orphan_title.lower()}"

# ── Main cross-linking logic ───────────────────────────────────────
new_plan_entries = {}
total_links_added = 0
articles_modified = set()

for orphan_slug in orphan_slugs:
    orphan = articles[orphan_slug]
    related = find_related(orphan_slug, orphan, n=5)
    
    if not related:
        print(f"  SKIP {orphan_slug}: no related articles found")
        continue
    
    related_slugs = []
    links_for_this_orphan = 0
    
    for rel_slug, score, rel_data in related:
        # Find keywords from orphan that appear in related article
        orphan_kw = keyword_index[orphan_slug]
        rel_body = rel_data['body']
        
        # Find which orphan keywords appear in the related article body
        matching_kw = [kw for kw in orphan_kw if kw.lower() in rel_body.lower()]
        
        para_idx, best_kw = find_insertion_point(rel_body, orphan_kw, orphan_slug, orphan['title'])
        
        if para_idx < 0:
            continue
        
        # Build the link
        anchor = make_anchor_text(orphan_slug, orphan['title'], best_kw)
        link = f"[{anchor}](/dutch-appliances/{orphan_slug}/)"
        
        # Insert into paragraph
        paragraphs = rel_body.split('\n\n')
        target_para = paragraphs[para_idx]
        
        # Find insertion point: after a sentence that mentions the keyword, or at end of paragraph
        if best_kw and best_kw.lower() in target_para.lower():
            # Find the sentence containing the keyword
            sentences = re.split(r'(?<=[.!?])\s+', target_para)
            for j, sent in enumerate(sentences):
                if best_kw.lower() in sent.lower():
                    # Insert after this sentence
                    sentences.insert(j + 1, f" {link}")
                    break
            else:
                # Append to end of paragraph
                target_para = target_para.rstrip() + f" {link}"
                sentences = [target_para]
            new_para = ' '.join(sentences)
        else:
            # Append to end of paragraph
            new_para = target_para.rstrip() + f" {link}"
        
        paragraphs[para_idx] = new_para
        new_body = '\n\n'.join(paragraphs)
        
        # Write back the modified article
        new_raw = f"---\n{rel_data['fm_text']}\n---\n{new_body}"
        path = os.path.join(REVIEWS_DIR, f"{rel_slug}.md")
        with open(path, 'w') as f:
            f.write(new_raw)
        
        related_slugs.append(rel_slug)
        links_for_this_orphan += 1
        articles_modified.add(rel_slug)
    
    if related_slugs:
        new_plan_entries[orphan_slug + '.md'] = related_slugs
        total_links_added += links_for_this_orphan
        print(f"  {orphan_slug}: {links_for_this_orphan} links → {', '.join(related_slugs[:3])}{'...' if len(related_slugs) > 3 else ''}")

# ── Update enrichment-plan.json ────────────────────────────────────
plan.update(new_plan_entries)
with open(ENRICHMENT_PATH, 'w') as f:
    json.dump(plan, f, indent=2, ensure_ascii=False)

print(f"\n=== SUMMARY ===")
print(f"Orphans processed: {len(orphan_slugs)}")
print(f"New plan entries: {len(new_plan_entries)}")
print(f"Total inline links added: {total_links_added}")
print(f"Articles modified: {len(articles_modified)}")
print(f"enrichment-plan.json now has {len(plan)} entries")
