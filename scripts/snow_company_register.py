#!/usr/bin/env python3
"""Turn the board's own corpus into a ServiceNow employer seed list.

Every row we have ever published carries a company name. Some of those rows are
ServiceNow work -- a title like "ServiceNow Platform Engineer" is direct evidence
that the employer was running the platform on the day they posted it. This script
harvests those names, normalises them, drops the vendor and the staffing agencies,
diffs what is left against the ATS board registry, and writes a candidate file.

It does three things and nothing else:

  1. reads `jobs.json` and every `inbox/*.md` table row;
  2. classifies each row as grade A (ServiceNow in the TITLE) or grade B
     (ServiceNow only in the body/excerpt/tags), and pulls the board tenant out of
     the row's URL when the URL is already an ATS link;
  3. subtracts every board we already sweep, so the output is *new* employers.

It never invents a date, never fetches anything, and never writes to the board.
Discovery output is a candidate list; a posting still has to be fetched from the
employer's own board before it can be published.

Usage
    python3 scripts/snow_company_register.py                 # write reports/
    python3 scripts/snow_company_register.py --show 40        # + print the top 40
    python3 scripts/snow_company_register.py --include-agencies
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

SN_RE = re.compile(r"service[\s\-_]*now", re.I)
# Module vocabulary is weaker evidence than the product name: "CSM" is also a
# Customer Success Manager and "GRC" is also a compliance team. Kept separate so
# it can inform a hunt without ever promoting a company on its own.
MODULES = {
    "itsm", "itom", "cmdb", "hrsd", "spm", "fsm", "irm", "ham", "sam",
    "discovery", "now platform", "glide", "snowflake", "moveworks",
}
MOD_ROLE = re.compile(
    r"(administrator|developer|architect|engineer|consultant|analyst|specialist|"
    r"lead|manager|director|sme|implementer)", re.I)

LEGAL = {
    "inc", "incorporated", "ltd", "limited", "llc", "llp", "lp", "ulc", "corp",
    "corporation", "co", "company", "plc", "gmbh", "sa", "ag", "bv", "nv", "pty",
    "the", "group", "holdings", "holding", "enterprises", "solutions",
    "technologies", "technology", "services", "systems", "international",
    "north", "america", "canada", "ca", "usa", "us",
    # "global" deliberately NOT stripped: "Insight Global" is an agency name,
    # not "Insight" plus noise, and stripping it hid the agency check.
}

VENDOR = {"servicenow", "service now", "servicenow inc"}

# Rows posted by these carry a client's role, not the poster's own stack. They
# still deserve a board (they hire ServiceNow staff) but they are never evidence
# that the *poster* runs ServiceNow, so they are excluded from the customer seed.
AGENCIES = {
    "hays", "procom", "procom consultants", "insight global", "robert half",
    "teksystems", "randstad", "adecco", "manpower", "kelly services", "kelly",
    "aerotek", "motion recruitment", "judge group", "robert walters",
    "michael page", "lancesoft", "artech", "collabera", "vaco", "aston carter",
    "ifg", "david aplin", "recruiting in motion", "peopletogo", "altis",
    "emergent", "systematix", "bevertec", "maplesoft", "q analysts", "matlen silver",
    "modis", "experis", "kforce", "apex systems", "dice", "cybercoders",
    "jobgether", "hands hr", "s.i. systems", "si systems", "itc technologies",
    "talentify", "partnerre", "eagle professional resources", "prospect",
    "compugen", "cdw", "softchoice", "long view systems", "longview",
    "leveragetek", "leveragetek staffing", "us tech solutions",
    "staffing solutions", "talent solutions", "resourcing", "recruit",
    "randstad technologies", "modis canada", "provision",
    "itc federal", "apex", "hays specialist recruitment",
    "alldus", "morson", "source code", "raise", "flexstaf", "flexstaf it",
    "acestack", "resonaite", "tehora", "2isolutions", "zodiac solutions",
    "saransh", "bull it solutions", "epsilon solutions", "iconma",
    "addmore group", "hrconnects", "whopper technologies", "optovia",
    "forhyre", "randstad canada", "robert half technology",
}

# Same employer, two legal names. Only entries where the equivalence is certain.
ALIASES = {
    "bank montreal": "bmo",
    "royal bank": "rbc",
    "toronto dominion": "td",
    "rexall pharmacy": "rexall",
}

# Some sources stuff the location (or a scraper's own status line) into the
# company field. Those are not employers and must never become a candidate.
JUNK_TOKENS = {
    "remote", "anywhere", "confidential", "verified", "myworkdayjobs",
    "smartrecruiters", "workday", "greenhouse", "lever", "ashby", "linkedin",
    "indeed", "usa", "us", "various",
}
CITIES = {
    "toronto", "ottawa", "vancouver", "montreal", "calgary", "edmonton",
    "mississauga", "brampton", "waterloo", "hamilton", "winnipeg", "victoria",
}
PROVINCE_RE = re.compile(
    r",\s*(on|ontario|quebec|qc|bc|british columbia|alberta|ab|canada)\b", re.I)


def is_junk(company: str, key: str) -> bool:
    """Company field that is really a location, a scraper status line, or a host."""
    low = (company or "").lower()
    if not key or key == "?":
        return True
    if ".com" in low or "http" in low:
        return True
    if any(tok in key.split() for tok in JUNK_TOKENS):
        return True
    if PROVINCE_RE.search(low):
        return True
    if key.endswith(" region") or " usa " in f" {key} ":
        return True
    head = key.split()[0]
    if head in CITIES and ("," in low or "/" in low):
        return True
    return False


STAFFING_RE = re.compile(r"\b(staffing|recruit(ing|ment)?|resourcing|talent solutions)\b", re.I)

AGGREGATORS = {
    "linkedin", "indeed", "glassdoor", "eluta", "adzuna", "talent.com",
    "ziprecruiter", "monster", "careerjet", "jooble", "workopolis", "jobs.ca",
    "justjobs", "ladders", "built in", "builtin", "simplyhired", "jobs",
    "confidential", "n/a", "various", "client", "our client", "unknown",
}

# URL -> (platform, tenant token, extra site/realm). Ordered: first match wins.
BOARD_PATTERNS = [
    (re.compile(r"https?://([a-z0-9\-]+)\.wd(\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/?#]+)", re.I), "workday"),
    (re.compile(r"https?://boards\.greenhouse\.io/([^/?#]+)", re.I), "greenhouse"),
    (re.compile(r"https?://job-boards\.greenhouse\.io/([^/?#]+)", re.I), "greenhouse"),
    (re.compile(r"https?://jobs\.lever\.co/([^/?#]+)", re.I), "lever"),
    (re.compile(r"https?://jobs\.ashbyhq\.com/([^/?#]+)", re.I), "ashby"),
    (re.compile(r"https?://jobs\.smartrecruiters\.com/([^/?#]+)", re.I), "smartrecruiters"),
    (re.compile(r"https?://apply\.workable\.com/([^/?#]+)", re.I), "workable"),
    (re.compile(r"https?://([a-z0-9\-]+)\.icims\.com/", re.I), "icims"),
    (re.compile(r"https?://jobs\.([a-z0-9\-]+)\.com/", re.I), "successfactors"),
]


def norm(name: str) -> str:
    """Company name -> comparison key. Legal suffixes and generic words out."""
    s = name.lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    toks = [t for t in s.split() if t and t not in LEGAL]
    key = " ".join(toks).strip()
    return ALIASES.get(key, key)


def is_agency(key: str) -> bool:
    if key in AGENCIES or STAFFING_RE.search(key):
        return True
    return any(a and (key.startswith(a + " ") or key.endswith(" " + a))
               for a in AGENCIES)


def board_hint(url: str) -> dict | None:
    for pat, platform in BOARD_PATTERNS:
        m = pat.search(url or "")
        if not m:
            continue
        if platform == "workday":
            return {"platform": "workday", "tenant": m.group(1).lower(),
                    "site": m.group(3), "url": url}
        return {"platform": platform, "tenant": m.group(1).lower(), "url": url}
    return None


def load_registry() -> tuple[set[str], set[str]]:
    """Names and tokens the sweeper already covers."""
    names, tokens = set(), set()

    extra = ROOT / "raw" / "ats_boards_extra.json"
    if extra.exists():
        try:
            data = json.loads(extra.read_text(encoding="utf-8"))
            for _route, toks in (data or {}).items():
                for t in toks or []:
                    tokens.add(norm(str(t)))
        except Exception as exc:  # noqa: BLE001
            print(f"WARN raw/ats_boards_extra.json unreadable: {exc}", file=sys.stderr)

    slugs = ROOT / "tools" / "ats_board_slugs_ca.txt"
    if slugs.exists():
        for line in slugs.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) == 2:
                tokens.add(norm(parts[1]))

    try:
        import ats_board_sweep as sweep  # noqa: PLC0415

        sweep.load_extra()
        for attr in ("WORKDAY", "GREENHOUSE", "LEVER", "ASHBY", "WORKABLE",
                     "SMARTRECRUITERS", "RECRUITEE", "BREEZY", "POLYMER", "GEM",
                     "TEAMTAILOR"):
            for row in getattr(sweep, attr, []) or []:
                if isinstance(row, (tuple, list)) and row:
                    tokens.add(norm(str(row[0])))
                    if len(row) > 1:
                        names.add(norm(str(row[-1])))
                else:
                    tokens.add(norm(str(row)))
    except Exception as exc:  # noqa: BLE001
        print(f"WARN could not import ats_board_sweep ({exc}); "
              "registry limited to raw/ + slug file", file=sys.stderr)

    names.discard("")
    tokens.discard("")
    return names, tokens


def in_registry(key: str, names: set[str], tokens: set[str]) -> str | None:
    if not key:
        return None
    if key in names:
        return key
    if key in tokens:
        return key
    for cand in names | tokens:
        if len(cand) >= 3 and (key.startswith(cand + " ") or key.endswith(" " + cand)):
            return cand
    for cand in names | tokens:
        if len(cand) >= 4 and (cand in key or key in cand):
            return cand
    return None


def rows_from_jobs(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    recs = data if isinstance(data, list) else data.get("jobs", [])
    out = []
    for r in recs:
        out.append({
            "title": r.get("title", "") or "",
            "company": r.get("company", "") or "",
            "location": r.get("location", "") or "",
            "url": r.get("url", "") or "",
            "posted": r.get("postedDate", "") or "",
            "source": r.get("source", "") or "",
            "blob": " ".join(str(r.get(k, "")) for k in ("title", "excerpt", "tags", "note")),
        })
    return out


ROW = re.compile(r"^\|(.+)\|\s*$")


def rows_from_inbox(folder: Path) -> list[dict]:
    out = []
    if not folder.is_dir():
        return out
    for f in sorted(folder.glob("*.md")):
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = ROW.match(line)
            if not m:
                continue
            cells = [c.strip() for c in m.group(1).split("|")]
            if len(cells) < 4 or set("".join(cells)) <= set("-: "):
                continue
            posted, role, company, location = cells[0], cells[1], cells[2], cells[3]
            url = cells[4] if len(cells) > 4 else ""
            link = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", role)
            title = link.group(1) if link else role
            if not url:
                url = link.group(2) if link else ""
            if not company or company.lower() in {"company", "---"}:
                continue
            out.append({
                "title": title, "company": company, "location": location,
                "url": url, "posted": posted, "source": f"inbox:{f.name}",
                "blob": " ".join([title, role, " ".join(cells[4:])]),
            })
    return out


def classify(row: dict) -> tuple[str | None, list[str]]:
    title = row["title"] or ""
    blob = row["blob"] or ""
    hits = []
    if SN_RE.search(title):
        hits.append("servicenow")
        return "A", hits
    if SN_RE.search(blob):
        hits.append("servicenow")
        return "B", hits
    low = f"{title} {blob}".lower()
    mods = [m for m in MODULES if m in low]
    if mods and MOD_ROLE.search(title):
        return "module", mods
    return None, []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", default=str(ROOT / "jobs.json"))
    ap.add_argument("--inbox", default=str(ROOT / "inbox"))
    ap.add_argument("--out-dir", default=str(ROOT / "reports"))
    ap.add_argument("--show", type=int, default=0)
    ap.add_argument("--include-agencies", action="store_true",
                    help="keep staffing agencies in the candidate list")
    args = ap.parse_args()

    rows = rows_from_jobs(Path(args.jobs)) + rows_from_inbox(Path(args.inbox))
    names, tokens = load_registry()

    groups: dict[str, dict] = {}
    excluded = collections.defaultdict(list)
    module_only: dict[str, list] = collections.defaultdict(list)

    for row in rows:
        grade, hits = classify(row)
        if not grade:
            continue
        key = norm(row["company"]) or "?"
        rec = {
            "title": row["title"][:160], "posted": row["posted"],
            "url": row["url"][:300], "source": row["source"],
            "location": row["location"][:80],
        }
        if grade == "module":
            module_only[key].append(rec)
            continue
        if key in VENDOR or key.startswith("servicenow"):
            excluded["vendor"].append(rec)
            continue
        if is_junk(row["company"], key) or ":" in row["company"]:
            excluded["junk"].append({**rec, "company": row["company"]})
            continue
        if key in AGGREGATORS:
            excluded["aggregator"].append(rec)
            continue
        if is_agency(key) and not args.include_agencies:
            excluded["agency"].append({**rec, "company": row["company"]})
            continue
        g = groups.setdefault(key, {
            "company": row["company"], "variants": collections.Counter(),
            "grade": grade, "hits": set(), "rows": [], "boards": [],
        })
        g["variants"][row["company"]] += 1
        g["hits"].update(hits)
        g["grade"] = "A" if "A" in (g["grade"], grade) else grade
        g["rows"].append(rec)
        hint = board_hint(row["url"])
        if hint:
            tn = norm(hint.get("tenant", ""))
            head = key.split()[0] if key else ""
            if tn and (tn in key or (head and (head in tn or tn.startswith(head)))):
                if hint not in g["boards"]:
                    g["boards"].append(hint)

    cands = []
    for key, g in groups.items():
        seen, deduped = set(), []
        for r in sorted(g["rows"], key=lambda r: r["posted"], reverse=True):
            sig = (r["title"].lower(), r["url"])
            if sig in seen:
                continue
            seen.add(sig)
            deduped.append(r)
        g["rows"] = deduped
        matched = in_registry(key, names, tokens)
        cands.append({
            "company": g["company"], "key": key,
            "variants": [v for v, _ in g["variants"].most_common(4)],
            "grade": g["grade"], "sn_terms": sorted(g["hits"]),
            "rows": sorted(g["rows"], key=lambda r: r["posted"], reverse=True)[:8],
            "row_count": len(g["rows"]),
            "board_hint": g["boards"][0] if g["boards"] else None,
            "in_registry": bool(matched), "registry_match": matched,
        })
    cands.sort(key=lambda c: (c["in_registry"] is True, c["grade"] != "A",
                              -c["row_count"]))
    new = [c for c in cands if not c["in_registry"]]

    stamp = dt.date.today().isoformat()
    out = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "inputs": {"jobs": args.jobs, "inbox": args.inbox,
                   "rows_scanned": len(rows)},
        "totals": {
            "grade_a_rows": sum(c["row_count"] for c in cands if c["grade"] == "A"),
            "companies_total": len(cands),
            "companies_new": len(new),
            "companies_in_registry": len(cands) - len(new),
            "excluded": {k: len(v) for k, v in excluded.items()},
            "module_only_companies": len(module_only),
        },
        "candidates": cands,
        "excluded": {k: v[:40] for k, v in excluded.items()},
        "module_only": {k: v[:5] for k, v in list(module_only.items())[:40]},
    }
    outdir = Path(args.out_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    jpath = outdir / f"snow_candidates_{stamp}.json"
    jpath.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")

    md = [f"# ServiceNow employer candidates — {stamp}", "",
          f"Source rows scanned: {len(rows)}. Companies with ServiceNow work: "
          f"{len(cands)} ({len(new)} not yet in the board registry).", "",
          "Grade A = ServiceNow in the job title. Grade B = ServiceNow only in the "
          "body. Grade D is never emitted: discovery produces employers, not rows.", "",
          "| Company | Grade | Rows | In registry | Board hint | Example title |",
          "|---|---|---|---|---|---|"]
    for c in cands[:60]:
        hint = c["board_hint"]["platform"] + ":" + c["board_hint"]["tenant"] if c["board_hint"] else ""
        ex = (c["rows"][0]["title"] if c["rows"] else "").replace("|", "/")
        md.append(f"| {c['company'][:48]} | {c['grade']} | {c['row_count']} | "
                  f"{'yes' if c['in_registry'] else 'NO'} | {hint} | {ex[:58]} |")
    if excluded["agency"]:
        md += ["", "## Excluded as staffing agencies (they hire ServiceNow staff; "
                   "they are not customer evidence)", ""]
        md += [f"- {e['company']} — {e['title'][:70]}" for e in excluded["agency"][:25]]
    mpath = outdir / f"snow_candidates_{stamp}.md"
    mpath.write_text("\n".join(md) + "\n", encoding="utf-8")

    t = out["totals"]
    print(f"rows scanned      : {len(rows)}")
    print(f"companies (A/B)   : {t['companies_total']}  "
          f"(A-title rows {t['grade_a_rows']})")
    print(f"  already covered : {t['companies_in_registry']}")
    print(f"  NEW candidates  : {t['companies_new']}")
    print(f"excluded          : {t['excluded']}")
    print(f"module-only names : {t['module_only_companies']} (not promoted)")
    print(f"wrote             : {jpath.name} / {mpath.name}")
    if args.show:
        print("\n" + " | ".join(["company", "g", "rows", "registry", "hint"]))
        for c in cands[:args.show]:
            hint = f"{c['board_hint']['platform']}:{c['board_hint']['tenant']}" if c["board_hint"] else "-"
            print(f"  {c['company'][:40]:40} {c['grade']} {c['row_count']:4} "
                  f"{'yes' if c['in_registry'] else 'NEW':4} {hint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
