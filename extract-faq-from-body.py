#!/usr/bin/env python3
"""Extract FAQ from article body text and inject as structured frontmatter.

Handles multiple FAQ formats found in KiesKeuken articles:
- "## FAQ" followed by bold Q/A pairs
- "## Veelgestelde Vragen" with ### headers or **Q:** patterns

Removes the original body FAQ section to avoid duplication since
ReviewLayout now renders FAQ from frontmatter.
"""

import os, sys, re

REVIEWS_DIR = os.path.expanduser("/home/cls/kieskeuken/src/content/reviews")

def extract_qa_pairs(body):
    """Extract Q&A pairs from body text using multiple strategies."""
    pairs = []
    
    # Strategy 1: Bold **Question?** followed by answer (same line or next line)
    qa_blocks = re.findall(
        r'\*\*(.+?)\*\*\s*(.*?)(?=\n?\s*\*\*|\n\s*(?:###\s|\Z))',
        body, re.DOTALL
    )
    for question, answer in qa_blocks:
        q = question.strip().rstrip('?:!., ')
        a = answer.strip()
        if len(q) > 8 and len(a) > 20:
            pairs.append((q, a[:300]))
    
    if pairs and len(pairs) >= 3:
        return pairs[:6]
    
    # Strategy 2: ### Header style (### Question, then paragraphs)
    lines = body.split('\n')
    current_q = None
    current_a = []
    
    for line in lines:
        header_match = re.match(r'^###\s+(.+)', line)
        if header_match:
            if current_q and len(' '.join(current_a).strip()) > 20:
                pairs.append((current_q, ' '.join(current_a).strip()[:300]))
            current_q = header_match.group(1).strip().rstrip('?:!., ')
            current_a = []
        elif current_q:
            if line.strip() and not line.strip().startswith('#'):
                current_a.append(line.strip())
            elif not line.strip():
                if current_a:
                    current_a.append('')  # preserve paragraph breaks
            elif line.strip().startswith('#'):
                if len(' '.join(current_a).strip()) > 20:
                    pairs.append((current_q, ' '.join(current_a).strip()[:300]))
                current_q = None
                current_a = []
    
    if current_q and len(' '.join(current_a).strip()) > 20:
        pairs.append((current_q, ' '.join(current_a).strip()[:300]))
    
    if pairs and len(pairs) >= 3:
        return pairs[:6]
    
    # Strategy 3: "Vraag:" / "Antwoord:" pattern
    qa_matches = re.findall(
        r'(?:Vraag|Q)[:\)]\s*(.+?)(?:\n|$)',
        body, re.IGNORECASE
    )
    a_matches = re.findall(
        r'(?:Antwoord|A)[:\)]\s*(.+?)(?=\n\s*(?:Vraag|Q|##|\Z))',
        body, re.DOTALL | re.IGNORECASE
    )
    
    for i in range(min(len(qa_matches), len(a_matches))):
        q = qa_matches[i].strip().rstrip('?:!., ')
        a = a_matches[i].strip()
        if len(q) > 8 and len(a) > 20:
            pairs.append((q, a[:300]))
    
    if pairs and len(pairs) >= 3:
        return pairs[:6]
    
    return []

def find_faq_section(body):
    """Locate the FAQ section start position in the body."""
    patterns = [
        r'\n## FAQ\b',
        r'\n## Veelgestelde [Vv]ragen\b',
        r'\n## Veelgestelde vragen\b',
        r'\nVeelgestelde [Vv]ragen\b',
    ]
    
    for pat in patterns:
        m = re.search(pat, body)
        if m:
            return m.start()
    return None

def format_faq_yaml(pairs):
    """Format FAQ list as YAML for frontmatter."""
    lines = ["faq:"]
    for q, a in pairs:
        q_esc = q.replace("'", "''")
        a_esc = a.replace("'", "''")
        lines.append(f"- q: '{q_esc}'")
        lines.append(f"  a: '{a_esc}'")
    return "\n".join(lines)

def process_file(filepath):
    """Process a single article: extract FAQ from body, inject into frontmatter."""
    with open(filepath) as f:
        content = f.read()
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False, "No frontmatter"
    
    fm_text = parts[1]
    body = parts[2]
    
    # Skip if already has FAQ in frontmatter
    if re.search(r'^\s*faq:', fm_text, re.MULTILINE):
        return False, "Already has FAQ frontmatter"
    
    # Find FAQ section in body
    faq_start = find_faq_section(body)
    if faq_start is None:
        return False, "No FAQ section in body"
    
    # Extract FAQ section text
    faq_section = body[faq_start:]
    end_pos = len(faq_section)
    for marker in [r'\n##\s+(?!FAQ|Veelgestelde)', r'\n---', r'\n>\s*\*\*Conclusie']:
        m = re.search(marker, faq_section[1:])
        if m:
            end_pos = min(end_pos, m.start() + 1)
    faq_section = faq_section[:end_pos]
    
    pairs = extract_qa_pairs(faq_section)
    
    if len(pairs) < 3:
        return False, f"Only {len(pairs)} QA pairs extracted"
    
    # Build new frontmatter with FAQ
    faq_block = format_faq_yaml(pairs)
    new_fm = fm_text.rstrip() + "\n" + faq_block
    
    # Remove old FAQ section from body to avoid duplication
    new_body = body[:faq_start].rstrip() + "\n"
    
    new_content = f"---\n{new_fm}\n---\n{new_body}"
    
    with open(filepath, "w") as f:
        f.write(new_content)
    
    return True, f"{len(pairs)} QA pairs"

def main():
    all_files = sorted([f for f in os.listdir(REVIEWS_DIR) if f.endswith('.md')])
    
    success = []
    skipped_faq = []
    no_section = []
    low_qa = []
    
    for fname in all_files:
        fpath = os.path.join(REVIEWS_DIR, fname)
        ok, msg = process_file(fpath)
        
        if ok:
            success.append((fname, msg))
            print(f"  ✓ {fname}: {msg}")
        elif "Already has" in msg:
            skipped_faq.append(fname)
        elif "No FAQ section" in msg:
            no_section.append(fname)
        elif "Only" in msg:
            low_qa.append(fname)
            print(f"  ⚠ {fname}: {msg}")
    
    summary = {
        "injected": len(success),
        "already_had_faq": len(skipped_faq),
        "no_section": len(no_section),
        "low_qa_count": len(low_qa),
        "injected_files": [s[0] for s in success]
    }
    
    print(f"\n--- SUMMARY ---")
    print(f"FAQ injected:   {len(success)}")
    print(f"Already had FAQ: {len(skipped_faq)}")
    print(f"No FAQ section: {len(no_section)}")
    print(f"Too few QAs:    {len(low_qa)}")
    
    return summary

if __name__ == "__main__":
    main()
