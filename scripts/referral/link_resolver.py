"""Turn a relative href / form action into an absolute, deduped URL."""
from __future__ import annotations

from urllib.parse import urljoin, urlsplit, urlunsplit, parse_qsl, urlencode

TRACKING_PREFIXES = ("utm_", "gh_src", "lever-source", "ref_", "source=")


def absolutize(href: str, base: str) -> str | None:
    """Resolve `href` against `base`. Returns None for non-http(s) results."""
    if not href:
        return None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return None
    try:
        absolute = urljoin(base, href)
        parts = urlsplit(absolute)
    except ValueError:
        return None
    if parts.scheme not in ("http", "https") or not parts.netloc:
        return None
    return absolute


def strip_tracking(url: str) -> str:
    """Drop utm_* and ATS source params so two hops to one form dedupe."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return url
    kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if not any(k.lower().startswith(p) for p in ("utm_", "gh_src",
                                                         "lever-source",
                                                         "ref_", "src", "source"))]
    return urlunsplit((parts.scheme, parts.netloc, parts.path,
                       urlencode(kept), ""))


def same_target(a: str, b: str) -> bool:
    """Compare ignoring scheme, trailing slash, tracking params and fragment."""
    def norm(u: str) -> str:
        p = urlsplit(strip_tracking(u))
        return f"{p.netloc.lower().removeprefix('www.')}{p.path.rstrip('/')}".lower()
    return norm(a) == norm(b)


def dedupe(urls: list[str]) -> list[str]:
    out: list[str] = []
    for u in urls:
        if not any(same_target(u, seen) for seen in out):
            out.append(u)
    return out
