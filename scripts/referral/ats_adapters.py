"""Pull a posting's description and application questions from its ATS API.

Every endpoint here is public, unauthenticated and returns the posting body as
a string. That makes the ATS channel both the cheapest and the most reliable
source of a referral signal: Greenhouse's `?questions=true` literally returns
the application form, so "were you referred by an employee?" is answerable
without fetching a single web page.
"""
from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from .source_router import SourceKind


@dataclass
class AtsPayload:
    description_html: str = ""
    questions: list[str] = field(default_factory=list)
    canonical_url: str = ""
    detail: str = ""
    ok: bool = False


def _api_get(url: str, timeout: float = 20.0) -> dict | list | None:
    try:
        from curl_cffi import requests as cr
        r = cr.get(url, impersonate="chrome", timeout=timeout)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:                                            # noqa: BLE001
        return None


# --------------------------------------------------------------------------
# URL shapes
#   greenhouse  boards.greenhouse.io/<token>/jobs/<id>
#               job-boards.greenhouse.io/<token>/jobs/<id>
#               boards-api.greenhouse.io/v1/boards/<token>/jobs/<id>
#   lever       jobs.lever.co/<site>/<uuid>
#   ashby       jobs.ashbyhq.com/<token>/<uuid>
#   smartrec    jobs.smartrecruiters.com/<company>/<postingId>
#   workday     <tenant>.wd<N>.myworkdayjobs.com/en-US/<site>/job/<path>
# --------------------------------------------------------------------------
GH_PATH = re.compile(r"/([^/]+)/jobs/(\d+)")
GH_API_PATH = re.compile(r"/v1/boards/([^/]+)/jobs/(\d+)")
LEVER_PATH = re.compile(r"/([^/]+)/([0-9a-f-]{20,})", re.I)
ASHBY_PATH = re.compile(r"/([^/]+)/([0-9a-f-]{20,})", re.I)
SR_PATH = re.compile(r"/([^/]+)/(\d{6,})")
WD_HOST = re.compile(r"^(?P<tenant>[^.]+)\.(?P<wd>wd\d+)\.myworkdayjobs\.com$")


def _greenhouse(url: str) -> AtsPayload:
    parts = urlsplit(url)
    m = GH_API_PATH.search(parts.path) or GH_PATH.search(parts.path)
    if not m:
        return AtsPayload(detail="unparsed greenhouse url")
    token, job_id = m.group(1), m.group(2)
    data = _api_get("https://boards-api.greenhouse.io/v1/boards/"
                    f"{token}/jobs/{job_id}?questions=true")
    if not isinstance(data, dict):
        return AtsPayload(detail="greenhouse api miss")
    questions: list[str] = []
    for q in data.get("questions") or []:
        label = (q.get("label") or "").strip()
        if label:
            questions.append(label)
        for fld in q.get("fields") or []:
            if fld.get("name"):
                questions.append(f"{label} :: {fld['name']}")
    content = data.get("content") or ""
    return AtsPayload(
        description_html=html.unescape(content),
        questions=questions,
        canonical_url=data.get("absolute_url") or url,
        detail=f"{len(questions)} application questions",
        ok=True)


def _lever(url: str) -> AtsPayload:
    m = LEVER_PATH.search(urlsplit(url).path)
    if not m:
        return AtsPayload(detail="unparsed lever url")
    site, posting_id = m.group(1), m.group(2)
    data = _api_get(f"https://api.lever.co/v0/postings/{site}/{posting_id}")
    if not isinstance(data, dict):
        return AtsPayload(detail="lever api miss")
    body = " ".join(filter(None, [
        data.get("description") or "",
        data.get("descriptionPlain") or "",
        *(l.get("content") or "" for l in (data.get("lists") or [])),
        data.get("additional") or "",
    ]))
    return AtsPayload(description_html=body,
                      canonical_url=data.get("hostedUrl") or url,
                      detail="lever posting detail", ok=True)


def _ashby(url: str) -> AtsPayload:
    m = ASHBY_PATH.search(urlsplit(url).path)
    if not m:
        return AtsPayload(detail="unparsed ashby url")
    token = m.group(1)
    data = _api_get("https://api.ashbyhq.com/posting-api/job-board/"
                    f"{token}?includeCompensation=true")
    if not isinstance(data, dict):
        return AtsPayload(detail="ashby board miss")
    target = m.group(2).lower()
    for j in data.get("jobs") or []:
        if target in (j.get("jobUrl") or "").lower() or target == str(j.get("id") or "").lower():
            return AtsPayload(
                description_html=j.get("descriptionHtml") or "",
                questions=[],
                canonical_url=j.get("jobUrl") or url,
                detail="ashby posting", ok=True)
    return AtsPayload(detail="ashby posting not in board payload")


def _smartrecruiters(url: str) -> AtsPayload:
    m = SR_PATH.search(urlsplit(url).path)
    if not m:
        return AtsPayload(detail="unparsed smartrecruiters url")
    company, posting_id = m.group(1), m.group(2)
    data = _api_get("https://api.smartrecruiters.com/v1/companies/"
                    f"{company}/postings/{posting_id}")
    if not isinstance(data, dict):
        return AtsPayload(detail="smartrecruiters api miss")
    sections = ((data.get("jobAd") or {}).get("sections") or {})
    body = " ".join(
        (sections.get(k) or {}).get("text") or ""
        for k in ("companyDescription", "jobDescription", "qualifications",
                  "additionalInformation"))
    return AtsPayload(description_html=body,
                      canonical_url=f"https://jobs.smartrecruiters.com/{company}/{posting_id}",
                      detail="smartrecruiters posting", ok=True)


def _workday(url: str) -> AtsPayload:
    """Workday has no public per-posting JSON endpoint we can rely on.

    The CXS job-list call needs the site id and a POST body; the posting page
    itself is JS-rendered. So the adapter reports "no API" and the orchestrator
    falls through to the tiered fetcher, which handles Workday via curl_cffi.
    """
    host = urlsplit(url).netloc
    return AtsPayload(detail=f"workday unapi'd ({host})", ok=False)


_ADAPTERS = {
    SourceKind.ATS_GREENHOUSE: _greenhouse,
    SourceKind.ATS_LEVER: _lever,
    SourceKind.ATS_ASHBY: _ashby,
    SourceKind.ATS_SMARTRECRUITERS: _smartrecruiters,
    SourceKind.ATS_WORKDAY: _workday,
}


def fetch(kind: SourceKind, url: str) -> AtsPayload:
    fn = _ADAPTERS.get(kind)
    if fn is None:
        return AtsPayload(detail=f"no adapter for {kind.value}")
    return fn(url)


def has_api(kind: SourceKind) -> bool:
    return kind in _ADAPTERS and kind is not SourceKind.ATS_WORKDAY
