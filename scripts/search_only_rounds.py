#!/usr/bin/env python3
"""
Search-only phase: run platform-focused rounds, collect raw results, save to scan_results/.
Scoring done separately via finalize_rounds.py (keyword-based, fast).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from ai_scan_pipeline import exa_search, parallel_ai_search, TODAY

SCAN_DIR = ROOT / "scan_results"
SCAN_DIR.mkdir(exist_ok=True)

PLATFORM_TERMS = {
    "sn": [
        "ServiceNow developer", "ServiceNow administrator", "ServiceNow architect",
        "ServiceNow consultant", "ServiceNow CSA", "ServiceNow CAD",
        "ServiceNow ITSM", "ServiceNow ITAM", "ServiceNow CMDB",
    ],
    "sf": [
        "Salesforce developer", "Salesforce administrator", "Salesforce architect",
        "Salesforce consultant", "Salesforce Platform Developer I",
        "Salesforce JavaScript Developer I", "Salesforce CPQ",
    ],
    "other": [
        "IT service management job Toronto", "ITSM consultant Canada",
        "platform administrator job Canada", "IT operations manager Toronto",
        "business analyst ServiceNow Salesforce Canada", "CRM developer Canada",
        "cloud platform engineer Toronto", "IT service desk manager Canada",
    ],
}

GEO_MODIFIERS = [
    "Toronto GTA Ontario Canada",
    "Canada remote",
    "Mississauga Markham Brampton",
    "Ottawa Ontario",
    "Vancouver BC",
    "Calgary Alberta",
]


def build_queries(platform: str, round_num: int) -> list[tuple[str, str]]:
    terms = PLATFORM_TERMS[platform]
    geo = GEO_MODIFIERS[round_num % len(GEO_MODIFIERS)]
    return [(f"{term} {geo} job", f"{platform}_r{round_num}") for term in terms]


def main() -> int:
    ap = argparse.ArgumentParser(description="Search-only platform rounds")
    ap.add_argument("--platform", choices=["sn", "sf", "other", "all"], default="all")
    ap.add_argument("--rounds", type=int, default=30)
    args = ap.parse_args()

    platforms = ["sn", "sf", "other"] if args.platform == "all" else [args.platform]
    rounds_per = args.rounds
    total = len(platforms) * rounds_per

    print(f"=== SEARCH-ONLY: {total} rounds ({rounds_per} per platform) ===")
    print(f"Date: {TODAY}")

    grand_raw = 0
    round_num = 0

    for platform in platforms:
        print(f"\n--- Platform: {platform.upper()} ---")
        for r in range(1, rounds_per + 1):
            round_num += 1
            queries = build_queries(platform, r)
            seen: dict[str, dict] = {}
            all_results: list[dict] = []

            start = time.time()
            for query, geo_label in queries:
                for api in ("exa", "parallel"):
                    try:
                        if api == "exa":
                            results = exa_search(query, num_results=5)
                        else:
                            results = parallel_ai_search(query, num_results=5)
                        for res in results:
                            u = res.get("url", "")
                            if u and u not in seen:
                                seen[u] = res
                                all_results.append(res)
                    except Exception as e:
                        print(f"    [{api}] {query[:45]} -> error: {e}")
                time.sleep(0.4)

            grand_raw += len(all_results)
            elapsed = time.time() - start

            # Save raw results for this round
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            out = {
                "platform": platform,
                "round": r,
                "global_round": round_num,
                "queries": len(queries),
                "raw_results": len(all_results),
                "generated_at": stamp,
                "results": all_results,
            }
            raw_file = SCAN_DIR / f"{TODAY}_{platform}_round{r}_raw_{stamp}.json"
            raw_file.write_text(json.dumps(out, indent=1, ensure_ascii=False))

            print(f"  Round {r:2d}: {len(all_results):3d} results in {elapsed:5.1f}s (cumulative raw: {grand_raw})")

    print(f"\n=== SEARCH COMPLETE ===")
    print(f"Total rounds: {total}")
    print(f"Total raw results: {grand_raw}")
    print(f"Files saved to: {SCAN_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
