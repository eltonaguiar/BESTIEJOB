#!/usr/bin/env python3
"""Full referral sweep over jobs.json.

Usage (from bestiejob/):
    python3 scripts/referral/enhanced_referral_hunt.py --limit 25
    python3 scripts/referral/enhanced_referral_hunt.py --kinds ats_greenhouse,ats_lever
    python3 scripts/referral/enhanced_referral_hunt.py --apply
"""
from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

REPO = Path(__file__).resolve().parent.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))          # `python scripts/referral/...` has no package root

from scripts.referral import ats_adapters, extractor, link_resolver, source_router
from scripts.referral.host_gate import HostGate
from scripts.referral.tiered_fetcher import fetch as tiered_fetch

JOBS = REPO / "jobs.json"
RAW = REPO / "raw"
NOW = datetime.now(timezone.utc)

_WRITE_LOCK = threading.Lock()


def load_jobs(path: Path | None = None) -> list[dict]:
    data = json.loads((path or JOBS).read_text(encoding="utf-8"))
    return data["jobs"] if isinstance(data, dict) else data


def _evidence(hit) -> str:
    return (hit.evidence or hit.pattern or "")[:280]


def inspect_job(job: dict, *, gate: HostGate, allow_playwright: bool) -> dict:
    url = (job.get("url") or "").strip()
    kind = source_router.classify(job)
    record = {
        "job_id": job.get("id"),
        "company": job.get("company"),
        "title": job.get("title"),
        "url": url,
        "route": kind.value,
        "status": "no_referral",
        "tier": "none",
        "referral": None,
        "checked_at": NOW.isoformat().replace("+00:00", "Z"),
    }
    if kind is source_router.SourceKind.UNROUTABLE:
        record["status"] = "unroutable"
        return record
    if kind in source_router.NO_FETCH:
        record["status"] = "skipped_aggregator"
        return record

    hits = []

    # --- ATS API channel ------------------------------------------------
    if kind in source_router.ATS_KINDS and ats_adapters.has_api(kind):
        payload = ats_adapters.fetch(kind, url)
        if payload.ok:
            record["tier"] = "ats_api"
            hits = extractor.extract(payload.description_html,
                                     title=job.get("title") or "",
                                     company=job.get("company") or "",
                                     structured_questions=payload.questions)
            if payload.canonical_url:
                url = payload.canonical_url
                record["canonical_url"] = payload.canonical_url

    # --- Web channel (only if the API channel was silent) ---------------
    if not extractor.best(hits):
        if gate.is_quarantined(urlsplit(url).netloc.lower()):
            record["status"] = "blocked"
            record["detail"] = "host quarantined"
            return record
        result = tiered_fetch(url, gate=gate, allow_playwright=allow_playwright)
        if not result.ok:
            record["status"] = "blocked" if result.status in (403, 429) else "error"
            record["tier"] = result.tier
            record["detail"] = result.detail[:160]
            return record
        record["tier"] = result.tier
        script_hits = extractor.extract(result.html,
                                       title=job.get("title") or "",
                                       company=job.get("company") or "")
        base = result.url or url
        for h in script_hits:
            if h.kind in ("page", "form") and h.value:
                resolved = link_resolver.absolutize(h.value, base)
                if resolved:
                    h.value = resolved
            hits.append(h)
        hits = extractor._rank(hits)

    top = extractor.best(hits)
    if top is None:
        record["all_hits"] = [
            {"kind": h.kind, "value": h.value, "conf": h.confidence,
             "pattern": h.pattern} for h in hits[:5]]
        return record

    record["status"] = "found"
    record["referral"] = {
        "kind": top.kind,
        "url": top.value if top.kind in ("form", "page") else None,
        "email": top.value if top.kind == "email" else None,
        "confidence": top.confidence,
        "evidence": _evidence(top),
        "all_hits": [{"kind": h.kind, "value": h.value, "conf": h.confidence,
                      "pattern": h.pattern} for h in hits[:6]],
    }
    return record


def _checkpoint(path: Path, results: list[dict]) -> None:
    with _WRITE_LOCK:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"generated_at": NOW.isoformat(),
                                   "results": results}, indent=1,
                                  ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)


def apply_to_jobs(results: list[dict], jobs_path: Path | None = None) -> int:
    """Inject `referral_info` into matching jobs rows. Returns rows touched."""
    path = jobs_path or JOBS
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data["jobs"] if isinstance(data, dict) else data
    by_id = {r["job_id"]: r for r in results if r.get("job_id")}
    touched = 0
    for row in rows:
        rec = by_id.get(row.get("id"))
        if not rec or rec["status"] != "found":
            continue
        row["referral_info"] = rec["referral"]
        touched += 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    return touched


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jobs", default=str(JOBS))
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=0, help="0 = all")
    ap.add_argument("--kinds", default="", help="comma-separated SourceKind values")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--no-playwright", action="store_true")
    ap.add_argument("--resume", action="store_true", help="skip ids already in --out")
    ap.add_argument("--apply", action="store_true", help="write referral_info into jobs.json")
    args = ap.parse_args()

    jobs_path = Path(args.jobs)
    out = Path(args.out) if args.out else RAW / f"referral_hunt_{NOW:%Y-%m-%d}.json"
    RAW.mkdir(exist_ok=True)

    jobs = load_jobs(jobs_path)
    if args.kinds:
        wanted = {k.strip() for k in args.kinds.split(",") if k.strip()}
        keep = [j for j in jobs
                if source_router.classify(j).value in wanted]
        # keep input order, but only the requested routes
        jobs = keep
    if args.limit:
        jobs = jobs[: args.limit]

    done: dict[str, dict] = {}
    if args.resume and out.exists():
        for r in json.loads(out.read_text(encoding="utf-8")).get("results", []):
            if r.get("job_id"):
                done[r["job_id"]] = r
        jobs = [j for j in jobs if j.get("id") not in done]

    print(f"sweeping {len(jobs)} jobs -> {out}  "
          f"workers={args.workers} playwright={not args.no_playwright}")

    gate = HostGate()
    results = list(done.values())
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(inspect_job, j, gate=gate,
                               allow_playwright=not args.no_playwright): j
                   for j in jobs}
        for i, fut in enumerate(as_completed(futures), 1):
            job = futures[fut]
            try:
                results.append(fut.result())
            except Exception as exc:                             # noqa: BLE001
                results.append({"job_id": job.get("id"), "status": "error",
                                "detail": f"{type(exc).__name__}: {exc}"[:160],
                                "url": job.get("url"), "company": job.get("company"),
                                "title": job.get("title"), "referral": None})
            if i % 25 == 0:
                _checkpoint(out, results)
                rate = i / max(time.time() - t0, 1e-6)
                print(f"  {i}/{len(jobs)}  {rate:.1f}/s  "
                      f"found={sum(1 for r in results if r.get('status') == 'found')}")

    _checkpoint(out, results)

    from collections import Counter
    counts = Counter(r.get("status") for r in results)
    print("\nstatus:", dict(counts))
    found = [r for r in results if r.get("status") == "found"]
    print(f"referral artifacts: {len(found)}")
    for r in found[:25]:
        ref = r["referral"]
        print(f"  {ref['confidence']:.2f} {ref['kind']:8s} "
              f"{(ref.get('url') or ref.get('email') or '')[:70]}")
        print(f"        {(r.get('company') or '')[:26]:26} {(r.get('title') or '')[:52]}")

    if args.apply:
        n = apply_to_jobs(results, jobs_path)
        print(f"\njobs.json: added referral_info to {n} rows")

    print(f"\nwrote {out} ({len(results)} records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
