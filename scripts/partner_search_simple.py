#!/usr/bin/env python3
"""Partner-focused ServiceNow job search — search only (no scoring)."""
import sys
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from ai_scan_pipeline import parallel_ai_search, KEYS, TODAY

PARTNERS = [
    "Ateko", "Deloitte Canada", "Ernst & Young", "KPMG",
    "Cognizant", "Fujitsu", "IBM", "Tanium",
    "BDO Canada", "CDW", "Compugen", "NewRocket", "RapDev",
    "TELUS Business", "Tech Mahindra",
]

TERMS = ["ServiceNow developer", "ServiceNow administrator", "ServiceNow consultant"]

def main():
    all_results = []
    seen = set()
    
    for partner in PARTNERS:
        for term in TERMS:
            query = f"{term} {partner} Canada job"
            print(f"Searching: {query}")
            try:
                results = parallel_ai_search(query, num_results=5)
                for r in results:
                    u = r.get("url", "")
                    if u and u not in seen:
                        seen.add(u)
                        all_results.append(r)
                print(f"  -> {len(results)} results")
            except Exception as e:
                print(f"  -> ERROR: {e}")
            time.sleep(0.3)
    
    print(f"\nTotal unique results: {len(all_results)}")
    
    # Save raw results
    out_dir = ROOT / "scan_results"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{TODAY}_partner_raw.json"
    out_file.write_text(json.dumps(all_results, indent=2), encoding="utf-8")
    print(f"Saved to {out_file}")
    
    # Print all results
    for r in all_results:
        print(f"  {r.get('title','')[:70]} | {r.get('url','')[:80]}")

if __name__ == "__main__":
    main()
