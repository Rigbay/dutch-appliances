import os
from collections import Counter

reviews_dir = "src/content/reviews"
files = [f for f in os.listdir(reviews_dir) if f.endswith(".md")]
print(f"Total articles: {len(files)}")
vs = [f for f in files if "-vs-" in f]
print(f"Comparison articles: {len(vs)}")
guides = [f for f in files if "-vs-" not in f]
print(f"Guide articles: {len(guides)}")

cats = Counter()
for f in files:
    with open(os.path.join(reviews_dir, f)) as fh:
        for line in fh:
            if line.startswith("category:"):
                cat = line.split(":", 1)[1].strip().strip("'\"")
                cats[cat] += 1
                break
for cat, count in sorted(cats.items()):
    print(f"  {cat}: {count}")
