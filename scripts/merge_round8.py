#!/usr/bin/env python3
"""Round 8 merge planner: classify KEEP rows and drop anything already in README."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"


def norm_url(u: str) -> str:
    u = u.strip()
    u = re.sub(r"[?#].*$", "", u)
    u = u.rstrip("/")
    u = re.sub(r"^https?://", "", u, flags=re.I)
    u = re.sub(r"^www\.", "", u, flags=re.I)
    return u.lower()


def norm_text(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def readme_keys() -> tuple[set[str], set[str]]:
    urls, pairs = set(), set()
    text = README.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 5:
            continue
        row = "|".join(cols)
        for m in re.finditer(r"\((https?://[^\s)]+)\)", row):
            urls.add(norm_url(m.group(1)))
        for m in re.finditer(r"\]\((https?://[^\s)]+)\)\s*\|", row):
            urls.add(norm_url(m.group(1)))
        # title | company from the stripped link text
        link = re.search(r"\[([^\]]*)\]\((https?://[^\s)]+)\)", row)
        if link:
            rest = row.split(")", 1)[-1]
            comp = rest.lstrip("|").split("|")[0].strip() if "|" in rest else ""
            if comp:
                pairs.add(f"{norm_text(link.group(1))[:60]}|{norm_text(comp)[:30]}")
    return urls, pairs


def classify(title: str, company: str, blob: str) -> str:
    r = f"{title} {company}".lower()
    if "servicenow" in r or "service now" in r:
        return "snow"
    if "salesforce" in r or "apex" in r or "lwc" in r:
        return "sf"
    if "servicenow" in blob:
        return "snow"
    if "salesforce" in blob:
        return "sf"
    return "other"


def main() -> int:
    verified = json.loads(Path("/tmp/r8_verified.json").read_text())
    urls, pairs = readme_keys()
    print(f"README index: {len(urls)} urls, {len(pairs)} title|company pairs")

    keep = [r for r in verified if r.get("verdict") == "KEEP"]
    new, dup = [], []
    for r in keep:
        u = norm_url(r["url"])
        p = f"{norm_text(r['title'])[:60]}|{norm_text(r['company'])[:30]}"
        if u in urls or p in pairs:
            dup.append(r)
            continue
        urls.add(u)
        pairs.add(p)
        blob = " ".join(r.get("vendor_counts", {}).keys()).lower()
        r["bucket"] = classify(r["title"], r["company"], blob)
        new.append(r)

    print(f"KEEP={len(keep)}  already-listed={len(dup)}  net-new={len(new)}\n")
    for r in dup:
        print(f"  DUP  {r['company'][:26]:26s} :: {r['title'][:56]}")
    print()
    for r in new:
        print(f"  NEW  [{r['bucket']:5s}] {r.get('datePosted','')[:10]} {r['company'][:26]:26s} :: {r['title'][:56]}")

    Path("/tmp/r8_new.json").write_text(json.dumps(new, indent=1))
    print(f"\nWrote /tmp/r8_new.json ({len(new)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
