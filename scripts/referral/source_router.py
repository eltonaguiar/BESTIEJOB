"""Map a job's URL to a fetch route.

Kept separate from the fetcher so tests can assert routing without a network
call, and so the orchestrator can skip whole families (LinkedIn) cheaply.
"""
from __future__ import annotations

from enum import Enum
from urllib.parse import urlsplit


class SourceKind(Enum):
    ATS_GREENHOUSE = "ats_greenhouse"
    ATS_LEVER = "ats_lever"
    ATS_ASHBY = "ats_ashby"
    ATS_WORKDAY = "ats_workday"
    ATS_SMARTRECRUITERS = "ats_smartrecruiters"
    AGGREGATOR_ADZUNA = "aggregator_adzuna"
    AGGREGATOR_LINKEDIN = "aggregator_linkedIn"
    COMPANY_DIRECT = "company_direct"
    UNROUTABLE = "unroutable"


# Order matters: `jobs.smartrecruiters.com` must not be caught by a looser rule.
_HOST_RULES: tuple[tuple[str, SourceKind], ...] = (
    ("boards.greenhouse.io", SourceKind.ATS_GREENHOUSE),
    ("boards-api.greenhouse.io", SourceKind.ATS_GREENHOUSE),
    ("job-boards.greenhouse.io", SourceKind.ATS_GREENHOUSE),
    ("greenhouse.io", SourceKind.ATS_GREENHOUSE),
    ("jobs.lever.co", SourceKind.ATS_LEVER),
    ("api.lever.co", SourceKind.ATS_LEVER),
    ("lever.co", SourceKind.ATS_LEVER),
    ("jobs.ashbyhq.com", SourceKind.ATS_ASHBY),
    ("api.ashbyhq.com", SourceKind.ATS_ASHBY),
    ("ashbyhq.com", SourceKind.ATS_ASHBY),
    ("myworkdayjobs.com", SourceKind.ATS_WORKDAY),
    ("myworkdaysite.com", SourceKind.ATS_WORKDAY),
    ("jobs.smartrecruiters.com", SourceKind.ATS_SMARTRECRUITERS),
    ("api.smartrecruiters.com", SourceKind.ATS_SMARTRECRUITERS),
    ("smartrecruiters.com", SourceKind.ATS_SMARTRECRUITERS),
    ("adzuna.ca", SourceKind.AGGREGATOR_ADZUNA),
    ("adzuna.com", SourceKind.AGGREGATOR_ADZUNA),
    ("linkedin.com", SourceKind.AGGREGATOR_LINKEDIN),
)

# Routes where fetching the human page is known not to pay off.
NO_FETCH = frozenset({SourceKind.AGGREGATOR_LINKEDIN, SourceKind.UNROUTABLE})

ATS_KINDS = frozenset({
    SourceKind.ATS_GREENHOUSE,
    SourceKind.ATS_LEVER,
    SourceKind.ATS_ASHBY,
    SourceKind.ATS_WORKDAY,
    SourceKind.ATS_SMARTRECRUITERS,
})


def classify(job: dict) -> SourceKind:
    url = (job.get("url") or "").strip()
    if not url:
        return SourceKind.UNROUTABLE
    try:
        host = urlsplit(url).netloc.lower()
    except ValueError:
        return SourceKind.UNROUTABLE
    if not host:
        return SourceKind.UNROUTABLE
    host = host.split(":")[0]
    for suffix, kind in _HOST_RULES:
        if host == suffix or host.endswith("." + suffix):
            return kind
    if urlsplit(url).scheme not in ("http", "https"):
        return SourceKind.UNROUTABLE
    return SourceKind.COMPANY_DIRECT
