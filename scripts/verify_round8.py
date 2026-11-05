#!/usr/bin/env python3
"""Round 8 verification: fetch JSON-LD JDs, count vendor mentions.
"""
import json
import re
import sys
import urllib.request
import time
import argparse
from pathlib import Path

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

VENDORS = {
    "ServiceNow": r"servicenow",
    "Salesforce": r"salesforce",
    "Jira": r"\bjira\b",
    "SAP": r"\bsap\b",
    "Guidewire": r"guidewire",
    "HubSpot": r"hubspot",
    "Workday": r"workday",
    "PowerBI": r"power\s*bi",
    "SQL": r"\bsql\b",
    "ITIL": r"\bitil\b",
}

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-CA,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

ENTITIES = {
    "&#38;amp;": "&", "&#38;lt;": "<", "&#38;gt;": ">",
    "&#38;nbsp;": " ", "&#38;#39;": "'", "&#38;quot;": '"',
    "&#38;rsquo;": "\u2019", "&#38;lsquo;": "\u2018",
    "&#38;mdash;": "\u2014", "&#38;ndash;": "\u2013",
}

def strip_html(s):
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    for ent, rep in ENTITIES.items():
        s = s.replace(ent, rep)
    return re.sub(r"[ \t]+", " ", s)

def jsonld(html):
    for m in re.finditer(
            r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
            html, re.S | re.I):
        try:
            data = json.loads(m.group(1).strip())
        except Exception:
            continue
        stack = [data]
        while stack:
            cur = stack.pop()
            if isinstance(cur, list):
                stack.extend(cur)
                continue
            if isinstance(cur, dict):
                if str(cur.get("@type", "")).lower() in ("jobposting", "jobposting "):
                    return cur
                stack.extend(cur.values())
    return {}

def years_min(text):
    best = None
    for m in re.finditer(r"(\d+)\s*(?:\+|plus)?\s*(?:to\s*\d+\s*)?year", text, re.I):
        try:
            n = int(m.group(1))
        except ValueError:
            continue
        if 0 < n <= 15 and (best is None or n < best):
            best = n
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()
    
    candidates = []
    for f in args.files:
        with open(f, "r") as fh:
            for line in fh:
                if line.startswith("|"):
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) > 5 and parts[1] != "Posted" and parts[1] != "---":
                        candidates.append({"date": parts[1], "title": parts[2], "company": parts[3], "url": parts[5]})

    results = []
    for row in candidates:
        try:
            html = fetch(row["url"])
        except Exception as e:
            row["error"] = f"fetch failed: {type(e).__name__}"
            results.append(row)
            print(f"ERR  {row['company']} :: {row['title']} :: {row['error']}")
            time.sleep(1.2)
            continue

        jd = jsonld(html)
        desc = strip_html(jd.get("description", "") or "")
        blob = f"{jd.get('title','')} {desc}".lower()

        row["jd_title"] = jd.get("title")
        row["datePosted"] = jd.get("datePosted")
        if not desc:
            row["error"] = "no JSON-LD description"

        counts = {name: len(re.findall(pat, blob, re.I)) for name, pat in VENDORS.items()}
        row["vendor_counts"] = {k: v for k, v in counts.items() if v}
        row["years_min"] = years_min(desc)
        row["remote"] = bool(re.search(r"\bremote\b|\bhybrid\b|\btelework\b", blob))
        row["verdict"] = ("KEEP" if counts.get("ServiceNow", 0) >= 1 or counts.get("Salesforce", 0) >= 1
                          else "DROP")
        results.append(row)
        print(f"{row['verdict']:4s} {row['company'][:28]:28s} :: {row['title'][:46]:46s} :: "
              f"{row['vendor_counts']} yrs={row['years_min']}")
        time.sleep(1.2)

    keep = [r for r in results if r.get("verdict") == "KEEP"]
    print(f"\n=== KEEP {len(keep)} / {len(results)} ===")
    with open("/tmp/r8_verified.json", "w") as f:
        json.dump(results, f, indent=1)
    print("\nWrote /tmp/r8_verified.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
