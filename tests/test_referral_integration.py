"""End-to-end tests with the network stubbed out."""
import json
from pathlib import Path

import pytest

from scripts.referral import ats_adapters
from scripts.referral import enhanced_referral_hunt as hunt
from scripts.referral.host_gate import HostGate
from scripts.referral.tiered_fetcher import FetchResult

FIXTURE = (Path(__file__).parent / "fixtures" / "referral_page.html").read_text(
    encoding="utf-8")


def _job(**kw):
    base = {"id": "greenhouse:boards.greenhouse.io/acme/jobs/1",
            "company": "Acme", "title": "ServiceNow Developer",
            "url": "https://boards.greenhouse.io/acme/jobs/1"}
    base.update(kw)
    return base


def test_ats_question_hit_produces_found(monkeypatch):
    monkeypatch.setattr(
        ats_adapters, "fetch",
        lambda kind, url: ats_adapters.AtsPayload(
            description_html="<p>Great role.</p>",
            questions=["Were you referred by a current Acme employee?"],
            canonical_url=url, ok=True, detail="stub"))
    rec = hunt.inspect_job(_job(), gate=HostGate(min_interval_s=0),
                           allow_playwright=False)
    assert rec["status"] == "found"
    assert rec["referral"]["kind"] == "question"
    assert rec["referral"]["confidence"] >= 0.9
    assert rec["tier"] == "ats_api"


def test_api_miss_falls_through_to_web(monkeypatch):
    monkeypatch.setattr(ats_adapters, "fetch",
                        lambda kind, url: ats_adapters.AtsPayload(ok=False))
    monkeypatch.setattr(
        hunt, "tiered_fetch",
        lambda url, **kw: FetchResult(FIXTURE, "curl_cffi", 200, url))
    rec = hunt.inspect_job(_job(), gate=HostGate(min_interval_s=0),
                           allow_playwright=False)
    assert rec["status"] == "found"
    assert rec["tier"] == "curl_cffi"
    # The extractor ranks email (mailto) higher than form (page) due to confidence tiebreak.
    # The fixture contains both.
    assert rec["referral"]["email"] == "referrals@acme.test"


def test_linkedin_is_skipped_without_network(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("must not fetch LinkedIn")
    monkeypatch.setattr(hunt, "tiered_fetch", boom)
    rec = hunt.inspect_job(_job(url="https://www.linkedin.com/jobs/view/123"),
                           gate=HostGate(min_interval_s=0),
                           allow_playwright=False)
    assert rec["status"] == "skipped_aggregator"


def test_blocked_status_on_403(monkeypatch):
    monkeypatch.setattr(ats_adapters, "fetch",
                        lambda kind, url: ats_adapters.AtsPayload(ok=False))
    monkeypatch.setattr(
        hunt, "tiered_fetch",
        lambda url, **kw: FetchResult(None, "none", 403, url, "HTTP 403"))
    rec = hunt.inspect_job(_job(), gate=HostGate(min_interval_s=0),
                           allow_playwright=False)
    assert rec["status"] == "blocked"


def test_apply_writes_referral_info(monkeypatch, tmp_path):
    jobs_file = tmp_path / "jobs.json"
    jobs_file.write_text(json.dumps({"jobs": [_job()]}), encoding="utf-8")
    monkeypatch.setattr(hunt, "JOBS", jobs_file)
    results = [{"job_id": _job()["id"], "status": "found",
                "referral": {"kind": "question", "url": None, "email": None,
                             "confidence": 1.0, "evidence": "stub"}}]
    assert hunt.apply_to_jobs(results) == 1
    row = json.loads(jobs_file.read_text(encoding="utf-8"))["jobs"][0]
    assert row["referral_info"]["kind"] == "question"
