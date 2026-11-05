#!/usr/bin/env python3
"""Round 8 merge: insert JD-verified net-new rows into README and fix all counts."""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
INBOX = ROOT / "inbox" / "linkedin-guest--2026-11-04--v1.md"
NEW_JSON = Path("/tmp/r8_new.json")


def norm_url(u: str) -> str:
    u = re.sub(r"[?#].*$", "", u.strip()).rstrip("/")
    u = re.sub(r"^https?://", "", u, flags=re.I)
    return re.sub(r"^www\.", "", u, flags=re.I).lower()


def inbox_rows() -> dict[str, dict]:
    out = {}
    for line in INBOX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 5 or c[0] in ("Posted", "---") or set(c[0]) <= {"-"}:
            continue
        out[norm_url(c[4])] = {"date": c[0], "title": c[1], "company": c[2],
                               "location": c[3], "url": c[4], "note": c[5] if len(c) > 5 else ""}
    return out


def cell(s: str) -> str:
    s = html.unescape(s).replace("|", r"\/").strip()
    return re.sub(r"\s+", " ", s)


def build_row(r: dict, src: dict) -> str:
    vc = r.get("vendor_counts", {})
    hits = vc.get("ServiceNow") or vc.get("Salesforce") or 0
    vendor = "ServiceNow" if vc.get("ServiceNow") else "Salesforce"
    yrs = r.get("years_min")
    note = f"via linkedin-guest--2026-11-04--v1.md · JD-verified {hits}× {vendor}"
    if yrs:
        note += f", {yrs} yrs min"
    if r.get("remote"):
        note += ", remote/hybrid"
    return (f"| {src['date']} | [{cell(src['title'])}]({src['url']}) | {cell(src['company'])} "
            f"| {cell(src['location'])} | {note} |")


def main() -> int:
    new = json.loads(NEW_JSON.read_text())
    src = inbox_rows()
    lines = README.read_text(encoding="utf-8").split("\n")

    snow, sf04, sf03 = [], [], []
    missing = []
    for r in new:
        s = src.get(norm_url(r["url"]))
        if not s:
            missing.append(r["url"])
            continue
        row = build_row(r, s)
        if r["bucket"] == "snow":
            snow.append(row)
        elif s["date"] >= "2026-11-04":
            sf04.append(row)
        else:
            sf03.append(row)

    if missing:
        print(f"!! {len(missing)} rows had no inbox source: {missing}")
        return 1

    print(f"snow={len(snow)} sf(11-04)={len(sf04)} sf(older)={len(sf03)}")

    def find(pred, start=0):
        for i in range(start, len(lines)):
            if pred(lines[i]):
                return i
        raise SystemExit("anchor not found")

    # --- ServiceNow: insert right after its table header
    i_snow_sec = find(lambda l: l.startswith("### ServiceNow jobs"))
    i_snow_hdr = find(lambda l: l.startswith("|---|---|---|---|---|"), i_snow_sec)
    lines[i_snow_hdr + 1:i_snow_hdr + 1] = snow

    # --- Salesforce: insert older-than-11-04 rows at first 2026-11-03 row
    i_sf_sec = find(lambda l: l.startswith("### Salesforce jobs"))
    i_sf_first_old = find(lambda l: l.startswith("| 2026-11-03 |"), i_sf_sec)
    lines[i_sf_first_old:i_sf_first_old] = sf03

    # --- Salesforce: insert 11-04 rows right after the table header
    i_sf_hdr = find(lambda l: l.startswith("|---|---|---|---|---|"), i_sf_sec)
    lines[i_sf_hdr + 1:i_sf_hdr + 1] = sf04

    text = "\n".join(lines)

    # --- recount
    def count_section(name: str, nxt: str | None) -> int:
        a = re.search(rf"^### {name} jobs \(\d+\)$", text, re.M).end()
        b = re.search(rf"^### {nxt} jobs \(\d+\)$", text, re.M).start() if nxt else \
            re.search(r"^## User / AI agent guide$", text, re.M).start()
        return sum(1 for l in text[a:b].split("\n")
                   if l.startswith("| 20") and l.count("|") >= 5)

    n_snow = count_section("ServiceNow", "Salesforce")
    n_sf = count_section("Salesforce", "Other")
    n_other = count_section("Other", None)
    total = n_snow + n_sf + n_other
    print(f"recount: ServiceNow={n_snow} Salesforce={n_sf} Other={n_other} total={total}")

    # --- rewrite every count location
    text = re.sub(r"^### ServiceNow jobs \(\d+\)$", f"### ServiceNow jobs ({n_snow})", text, re.M)
    text = re.sub(r"^### Salesforce jobs \(\d+\)$", f"### Salesforce jobs ({n_sf})", text, re.M)
    text = re.sub(r"^### Other jobs \(\d+\)$", f"### Other jobs ({n_other})", text, re.M)
    text = re.sub(r"^\s*- \[ServiceNow jobs \(\d+\)\]\(#servicenow-jobs-\d+\)$",
                  f"  - [ServiceNow jobs ({n_snow})](#servicenow-jobs-{n_snow})", text, re.M)
    text = re.sub(r"^\s*- \[Salesforce jobs \(\d+\)\]\(#salesforce-jobs-\d+\)$",
                  f"  - [Salesforce jobs ({n_sf})](#salesforce-jobs-{n_sf})", text, re.M)
    text = re.sub(r"^\s*- \[Other jobs \(\d+\)\]\(#other-jobs-\d+\)$",
                  f"  - [Other jobs ({n_other})](#other-jobs-{n_other})", text, re.M)
    text = re.sub(r"<summary><strong>Show \d+ postings</strong></summary>",
                  lambda m: m.group(0), text)
    # per-section "Show N postings"
    for name, n in (("ServiceNow", n_snow), ("Salesforce", n_sf), ("Other", n_other)):
        a = re.search(rf"^### {name} jobs \(\d+\)$", text, re.M).end()
        nxt = {"ServiceNow": "Salesforce", "Salesforce": "Other"}.get(name)
        b = re.search(rf"^### {nxt} jobs \(\d+\)$", text, re.M).start() if nxt else \
            re.search(r"^## User / AI agent guide$", text, re.M).start()
        seg = re.sub(r"<summary><strong>Show \d+ postings</strong></summary>",
                     f"<summary><strong>Show {n} postings</strong></summary>", text[a:b])
        text = text[:a] + seg + text[b:]
    text = re.sub(r"\*\*\d+ live postings\*\*", f"**{total} live postings**", text)

    README.write_text(text, encoding="utf-8")
    print(f"README updated: {total} live postings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
