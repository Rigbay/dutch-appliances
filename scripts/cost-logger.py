#!/usr/bin/env python3
"""
Cost logger for the Dutch content site: reads cost-log.json and prints summary.
Usage:
  python cost-logger.py          # summary
  python cost-logger.py --reset  # archive + reset log
"""

import argparse
import json
import shutil
from datetime import date
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent / "cost-log.json"


def main():
    parser = argparse.ArgumentParser(description="Cost logging for content pipeline")
    parser.add_argument("--reset", action="store_true", help="archive current log and start fresh")
    args = parser.parse_args()

    if not LOG_PATH.exists():
        print("No cost log yet. Run generate-article.py first.")
        return

    entries = json.loads(LOG_PATH.read_text())

    if args.reset:
        archive_dir = LOG_PATH.parent / "cost-archive"
        archive_dir.mkdir(exist_ok=True)
        archive_name = f"cost-log-{date.today().isoformat()}.json"
        shutil.move(str(LOG_PATH), str(archive_dir / archive_name))
        print(f"Archived to {archive_dir / archive_name}")
        return

    # Summary
    total = sum(e["cost_est"] for e in entries)
    articles = len(entries)

    print(f"=== Cost Summary ===")
    print(f"Articles generated: {articles}")
    print(f"Total API cost:     ${total:.4f}")
    print(f"Avg cost/article:   ${total/articles:.4f}" if articles else "")

    # Per-model breakdown
    models = {}
    for e in entries:
        m = e["model"]
        models.setdefault(m, {"count": 0, "cost": 0.0, "tokens_in": 0, "tokens_out": 0})
        models[m]["count"] += 1
        models[m]["cost"] += e["cost_est"]
        models[m]["tokens_in"] += e["tokens_in"]
        models[m]["tokens_out"] += e["tokens_out"]

    print()
    for model, stats in models.items():
        print(f"  {model}: {stats['count']} articles, ${stats['cost']:.4f}, "
              f"{stats['tokens_in']:,} in / {stats['tokens_out']:,} out")

    # Projection
    if articles > 0:
        for n in [50, 100, 200, 500]:
            proj = (total / articles) * n
            print(f"  Projected cost for {n} articles: ${proj:.2f}")

    print()
    print(f"Log: {LOG_PATH}")


if __name__ == "__main__":
    main()
