#!/usr/bin/env python3
"""
Add inline Amazon affiliate links to body text of articles that lack them.
Targets recommendation sections: "Snel Advies", "Beste Keuze", "Kies de...", etc.
Avoids markdown tables and headings.
"""
import glob, yaml, re
from pathlib import Path

REVIEWS_DIR = Path('src/content/reviews')

def extract_products(frontmatter):
    """Extract product names and affiliate links from frontmatter."""
    prods = {}
    for p in frontmatter.get('products', []):
        name = (p.get('name', '') or '').replace('**', '').strip()
        link = (p.get('affiliateLink', '') or '').strip()
        if name and link and 'amazon' in link.lower():
            prods[name] = link
    return prods

def is_in_recommendation_context(body, pos, name):
    """Check if a product mention is in a recommendation context."""
    # Get the paragraph/line containing this mention
    line_start = body.rfind('\n', 0, pos) + 1
    line_end = body.find('\n', pos + len(name))
    if line_end == -1:
        line_end = len(body)
    line = body[line_start:line_end].lower()
    
    # Don't link in markdown tables
    if line.strip().startswith('|'):
        return False
    
    # Don't link in headings
    if body[max(0, pos-5):pos].startswith('#') or body[max(0, pos-3):pos].startswith('##'):
        return False
    
    # Don't link if already inside a markdown link [...](url)
    before = body[:pos]
    after = body[pos + len(name):]
    
    # Check for incomplete link: [text...
    last_open = before.rfind('[')
    last_close = before.rfind(']')
    if last_open > last_close:
        return False  # Inside a link
    
    # Check for ]( close by
    if after.strip().startswith(']('):
        return False  # Already part of a link text
    
    # Recommendation indicators
    rec_indicators = [
        'kies de', 'kies voor de', 'onze keuze', 'beste keuze', 
        'onze aanrader', 'topkeuze', 'aanbevolen', 'uitstekende keuze',
        'absolute topper', 'beste koop', 'beste prestaties',
        'sterk aangeraden', 'ga voor de', 'onze favoriet',
    ]
    
    # Check 80 chars before the mention
    ctx_start = max(0, pos - 80)
    ctx = body[ctx_start:pos].lower()
    
    return any(ind in ctx for ind in rec_indicators)

def process_article(filepath):
    """Process one article, adding exactly one inline affiliate link per product."""
    content = filepath.read_text(encoding='utf-8')
    parts = content.split('---', 2)
    if len(parts) < 3:
        return 0
    
    body = parts[2]
    body_lower = body.lower()
    
    # Skip if already has Amazon or Bol links in body
    if 'amazon.nl' in body_lower or 'bol.com' in body_lower:
        return 0
    
    try:
        fm = yaml.safe_load(parts[1])
    except:
        return 0
    
    products = extract_products(fm)
    if not products:
        return 0
    
    # We'll work from end to start to preserve indices
    additions = []  # (position, old_text, new_text)
    modified = body
    
    for product_name, affiliate_link in products.items():
        if product_name not in modified:
            continue
        
        # Find all occurrences that are in recommendation contexts
        idx = 0
        while idx < len(modified):
            idx = modified.find(product_name, idx)
            if idx == -1:
                break
            
            # Skip if already linked
            before_ctx = modified[max(0, idx-3):idx+len(product_name)]
            if f'[{product_name}](' in modified[max(0, idx-5):idx+len(product_name)+10]:
                idx += 1
                continue
            
            if is_in_recommendation_context(modified, idx, product_name):
                # Only add ONE link per product — first one found
                new_text = f'[{product_name}]({affiliate_link})'
                additions.append((idx, product_name, new_text))
                idx = len(modified)  # break out
            idx += 1
    
    if not additions:
        return 0
    
    # Apply in reverse order
    additions.sort(key=lambda x: x[0], reverse=True)
    for idx, old, new in additions:
        modified = modified[:idx] + new + modified[idx + len(old):]
    
    # Write back
    new_content = f'---{parts[1]}---{modified}'
    filepath.write_text(new_content, encoding='utf-8')
    
    return len(additions)

def main():
    articles = sorted(glob.glob(str(REVIEWS_DIR / '*.md')))
    
    processed = 0
    total_links = 0
    already_had = 0
    no_products = 0
    
    for path_str in articles:
        path = Path(path_str)
        slug = path.stem
        added = process_article(path)
        
        if added > 0:
            processed += 1
            total_links += added
            print(f'✅ {slug}: {added} inline link(s)')
        elif added == 0:
            # Determine why
            content = path.read_text(encoding='utf-8')
            body = content.split('---', 2)[-1].lower() if '---' in content else ''
            if 'amazon.nl' in body or 'bol.com' in body:
                already_had += 1
            else:
                no_products += 1
    
    print()
    print(f'=== SUMMARY ===')
    print(f'Articles enhanced: {processed}')
    print(f'Total inline affiliate links added: {total_links}')
    print(f'Skipped (already had links): {already_had}')
    print(f'Skipped (no products/matches): {no_products}')

if __name__ == '__main__':
    main()
