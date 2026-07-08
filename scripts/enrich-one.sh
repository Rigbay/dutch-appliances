#!/bin/bash
# Enrich one thin article using Gemini API via curl
set -e

TARGET="$1"
if [ -z "$TARGET" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

REVIEWS_DIR="src/content/reviews"
FILEPATH="$REVIEWS_DIR/$TARGET"

if [ ! -f "$FILEPATH" ]; then
    echo "File not found: $FILEPATH"
    exit 1
fi

# Get API key
API_KEY=$(grep "^GEMINI_API_KEY=" ~/.hermes/.env | grep -v "^#" | grep -v "your_gemini" | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d ' ')

# Extract frontmatter and body
FM=$(sed -n '/^---$/,/^---$/p' "$FILEPATH" | sed '1d;$d')
BODY=$(sed '1,/^---$/d' "$FILEPATH" | sed '1,/^---$/d')

# Extract key fields
TITLE=$(echo "$FM" | grep "^title:" | head -1 | sed 's/^title:\s*//' | tr -d "'\"")
DESC=$(echo "$FM" | grep "^description:" | head -1 | sed 's/^description:\s*//' | tr -d "'\"")
FEATURED=$(echo "$FM" | grep "^featuredProduct:" | head -1 | sed 's/^featuredProduct:\s*//' | tr -d "'\"")
PRICE=$(echo "$FM" | grep "^priceRange:" | head -1 | sed 's/^priceRange:\s*//' | tr -d "'\"")

WORD_COUNT=$(echo "$BODY" | wc -w)
echo "Enriching $TARGET ($WORD_COUNT words body)..."

# Build prompt (escaped for JSON)
PROMPT=$(cat <<PROMPT_END
Je bent een Nederlandse copywriter voor koopgidsen. Schrijf een complete artikel-body (800-1200 woorden) voor:

TITEL: $TITLE
BESCHRIJVING: $DESC
HOOFDPRODUCT: $FEATURED
PRIJSKLASSE: $PRICE

BESTAANDE CONTENT (dun, moet vervangen):
$(echo "$BODY" | head -c 500)

STRUCTUUR:
## Inleiding (2-3 alinea's)
## Snel advies
## Waar let je op bij het kopen? (4-6 punten, **vette** kernbegrippen)
## Onze topkeuzes (per product: naam, prijs, voor wie, sterk/minpunt)
## Veelgestelde vragen (3-5)
## Conclusie

REGELS: vlot NL-NL, korte alinea's, prijzen in €, Amazon.nl (tag: kieskeukennl-21), geen placeholders, ALLEEN body — begin met ## Inleiding
PROMPT_END
)

# Escape for JSON
PROMPT_JSON=$(python3 -c "import json; print(json.dumps(open('/dev/stdin').read()))" <<< "$PROMPT")

# Call Gemini
RESPONSE=$(curl -s --max-time 120 \
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"contents\":[{\"parts\":[{\"text\":$PROMPT_JSON}]}],\"generationConfig\":{\"temperature\":0.7,\"maxOutputTokens\":4096}}")

# Extract text
NEW_BODY=$(echo "$RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    text = data['candidates'][0]['content']['parts'][0]['text']
    # Clean up
    text = text.strip()
    if text.startswith('```'): 
        text = text.split('\n', 1)[1] if '\n' in text else text[3:]
    if text.endswith('```'):
        text = text[:-3].strip()
    print(text)
except Exception as e:
    print('ERROR:', e, file=sys.stderr)
    sys.exit(1)
" 2>&1)

if echo "$NEW_BODY" | grep -q "^ERROR:"; then
    echo "Gemini API error: $NEW_BODY"
    echo "Raw response: $RESPONSE" | head -c 500
    exit 1
fi

NEW_WORDS=$(echo "$NEW_BODY" | wc -w)
if [ "$NEW_WORDS" -lt 200 ]; then
    echo "FAILED: generated body too short ($NEW_WORDS words)"
    exit 1
fi

# Reconstruct file
{
    echo "---"
    echo "$FM"
    echo "---"
    echo ""
    echo "$NEW_BODY"
    echo ""
    echo "---"
    echo ""
    echo "*Dit artikel is bijgewerkt voor 2026. Productvermeldingen en prijzen kunnen afwijken. Sommige links in dit artikel zijn affiliate-links. Als je via deze links een product koopt, ontvangen wij een kleine commissie zonder dat jij extra betaalt.*"
} > "$FILEPATH"

echo "DONE: $WORD_COUNT → $NEW_WORDS words"
