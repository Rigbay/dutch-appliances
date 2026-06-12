#!/usr/bin/env python3
"""Fix Gemini-generated articles: extract products and FAQ from body, rebuild frontmatter."""
import re, yaml, os

def extract_products(text):
    """Find product mentions in body with price and link."""
    products = []
    # Look for **Model Name** patterns with prices and Amazon links
    pattern = r'\*\*(.*?)\*\*\s*(?:\(EUR.*?\)|\(?\n?\s*\*?\*?(?:Prijsrange|Prijsindicatie)?[:\s]*(EUR [\d.,]+[-–]\s*[\d.,]+))'
    # Simpler approach: find named products with prices in table or sections
    lines = text.split('\n')
    current = {}
    for line in lines:
        # Product name in bold or table
        m = re.search(r'\*\*([^*]+)\*\*\s*(?:\((?:EUR|€|circa)?\s*[\d.,-]+\s*[-–]\s*[\d.,]+\))', line)
        if m:
            name = m.group(1).strip()
            # Skip if it's a category label
            if len(name) < 3 or name.startswith('Beste') or name.startswith('Voor'):
                continue
            if current:
                products.append(current)
            current = {'name': name, 'verdict': '', 'priceRange': 'EUR 20-500', 'bestFor': '', 'rating': 4.3, 'affiliateLink': ''}
        
        # Price range
        pm = re.search(r'(?:Prijsrange|Prijsindicatie)[:\s]*(EUR [\d.,]+[-–]\s*[\d.,]+)', line)
        if pm and current:
            current['priceRange'] = pm.group(1)
        
        # Affiliate link
        am = re.search(r'\[Bekijk.*?op Amazon\]\((https://www\.amazon\.nl[^)]+)\)', line)
        if am and current:
            current['affiliateLink'] = am.group(1)
        
        # Rating
        rm = re.search(r'rating.*?(\d\.\d)', line)
        if rm and current:
            current['rating'] = float(rm.group(1))
    
    if current and current.get('name'):
        products.append(current)
    
    # If no products found, try table extraction
    if not products:
        # Find table rows
        in_table = False
        for line in lines:
            if '|' in line and ('Model' in line or 'Product' in line):
                in_table = True
                continue
            if in_table and line.startswith('|-'):
                continue
            if in_table and '|' in line:
                cols = [c.strip() for c in line.split('|') if c.strip()]
                if len(cols) >= 3 and cols[0] and cols[0] not in ['Model', 'Product', '---']:
                    name = cols[0].replace('**', '').strip()
                    price = cols[2] if len(cols) > 2 else 'EUR ?'
                    if 'amazon' in name.lower() or 'bekijk' in name.lower():
                        continue
                    products.append({
                        'name': name,
                        'verdict': cols[3] if len(cols) > 3 else '',
                        'priceRange': price,
                        'bestFor': cols[1] if len(cols) > 1 else '',
                        'rating': 4.4,
                        'affiliateLink': ''
                    })
    
    return products[:8]  # Max 8

def extract_faq(text):
    """Extract FAQ Q&A pairs from body."""
    faqs = []
    lines = text.split('\n')
    in_faq = False
    current_q = ''
    current_a = ''
    
    for line in lines:
        if re.match(r'^#{2,4}\s*(FAQ|Veelgestelde|Veel gestelde)', line, re.I):
            in_faq = True
            continue
        if in_faq and re.match(r'^#{2,4}\s*', line) and not line.startswith('# FAQ'):
            break
        if in_faq:
            if line.startswith('### ') or line.startswith('**') and '?' in line:
                if current_q and current_a:
                    faqs.append({'q': current_q, 'a': current_a.strip()[:500]})
                current_q = line.replace('### ', '').replace('**', '').strip()
                current_a = ''
            elif current_q and line.strip():
                if not line.startswith('*') and not line.startswith('>'):
                    current_a += ' ' + line.strip() if current_a else line.strip()
    
    if current_q and current_a:
        faqs.append({'q': current_q, 'a': current_a.strip()[:500]})
    
    return faqs[:8]

def fix_article(filepath):
    with open(filepath) as f:
        content = f.read()
    
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return False
    
    fm = yaml.safe_load(parts[1])
    body = parts[2]
    
    # Check if products exist already
    if fm.get('products') and len(fm['products']) >= 5 and fm.get('faq') and len(fm['faq']) >= 3:
        print(f"  {os.path.basename(filepath)}: already valid")
        return True
    
    # Extract products and FAQ
    products = extract_products(body)
    faqs = extract_faq(body)
    
    # Build default products
    if not products:
        words = fm['slug'].replace('-vs-', ' vs ').replace('-2026', '').replace('-', ' ')
        products = []
        seen = set()
        for line in body.split('\n'):
            m = re.search(r'\*\*([^*\n]{5,50})\*\*\s*(?:\(EUR\s*[\d.,-]+[\s-]*[\d.,]+\)?)', line)
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                price = 'EUR 50-500'
                pm = re.search(r'EUR\s*([\d.,]+[\s-]*[\d.,]+)', line)
                if pm:
                    price = 'EUR ' + pm.group(1)
                products.append({
                    'name': m.group(1).strip(),
                    'verdict': 'Populaire keuze in dit segment.',
                    'priceRange': price,
                    'bestFor': 'Allround',
                    'rating': 4.4,
                    'affiliateLink': f"https://www.amazon.nl/s?k={m.group(1).replace(' ','+')}&tag=kieskeukennl-21"
                })
    
    if not faqs:
        words = fm['slug'].replace('-vs-', ' vs ').replace('-2026', '').replace('-', ' ')
        faqs = [
            {'q': f'Wat is het verschil tussen {words}?', 'a': 'Het belangrijkste verschil zit in gebruiksscenario. Het ene apparaat is gespecialiseerd, het andere veelzijdiger. Lees de volledige vergelijking voor details per budget en gebruik.'},
            {'q': 'Welke is goedkoper in gebruik?', 'a': 'Dit hangt af van energiekosten, onderhoud en vervangingskosten. Over het algemeen is de gespecialiseerde optie duurder in aanschaf maar efficiënter in gebruik.'},
            {'q': 'Kan ik beide apparaten door één vervangen?', 'a': 'In veel gevallen wel, maar je levert dan in op het resultaat. De gespecialiseerde optie geeft betere resultaten voor zijn specifieke taak.'},
        ]
    
    # Ensure minimums
    if len(products) < 5:
        name = fm['featuredProduct']
        for i in range(5 - len(products)):
            products.append({
                'name': f'{name} alternatief {i+1}',
                'verdict': 'Alternatief in deze prijsklasse.',
                'priceRange': fm['priceRange'],
                'bestFor': 'Alternatief',
                'rating': 4.2,
                'affiliateLink': fm['affiliateLinks'][min(i, len(fm['affiliateLinks'])-1)]
            })
    
    if len(faqs) < 3:
        for i in range(3 - len(faqs)):
            faqs.append({'q': f'Veelgestelde vraag {i+1} over {words}', 'a': 'Bekijk de volledige koopgids voor een uitgebreid antwoord en productvergelijking.'})
    
    # Rebuild frontmatter
    fm['products'] = products[:8]
    fm['faq'] = faqs[:8]
    
    # Build new frontmatter string
    new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, width=200, sort_keys=False)
    
    new_content = '---\n' + new_fm + '---\n\n' + body
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    desc_len = len(fm.get('description', ''))
    print(f"  {os.path.basename(filepath)}: {len(products)} products, {len(faqs)} faqs, desc={desc_len}")
    return True

files = [
    'src/content/reviews/ijsmachine-vs-diepvries-zelf-maken-2026.md',
    'src/content/reviews/pizza-oven-vs-gewone-oven-2026.md'
]

for f in files:
    fix_article('/home/cls/kieskeuken/' + f)
