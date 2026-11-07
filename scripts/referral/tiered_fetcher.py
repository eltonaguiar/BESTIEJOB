"""Escalating HTTP fetcher: curl_cffi -> playwright -> httpx.

Most employer sites answer a TLS-fingerprinted GET. The ones that don't are
usually JS-rendered, which is what the browser tier is for. httpx is the last
resort for plain hosts that dislike curl_cffi's headers.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass

from .host_gate import HostGate

UA_POOL = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
)

_PW_LOCK = threading.Lock()
_PW_BROWSER = None

@dataclass
class FetchResult:
    html: str | None
    tier: str            # curl_cffi | playwright | httpx | none
    status: int
    url: str
    detail: str = ""

    @property
    def ok(self) -> bool:
        return bool(self.html)


def _tier_curl(url: str, timeout: float, host: str, gate: HostGate) -> FetchResult:
    try:
        from curl_cffi import requests as cr
    except ImportError:
        return FetchResult(None, "curl_cffi", 0, url, "curl_cffi missing")
    try:
        r = cr.get(url, impersonate="chrome", timeout=timeout,
                   allow_redirects=True,
                   headers={"Accept-Language": "en-CA,en;q=0.9"})
    except Exception as exc:                                    # noqa: BLE001
        return FetchResult(None, "curl_cffi", 0, url, type(exc).__name__)
    if r.status_code == 200 and r.text:
        gate.record(host, True)
        return FetchResult(r.text, "curl_cffi", 200, str(r.url))
    return FetchResult(None, "curl_cffi", r.status_code, url,
                       f"HTTP {r.status_code}")


def _tier_httpx(url: str, timeout: float, host: str, gate: HostGate) -> FetchResult:
    try:
        import httpx
    except ImportError:
        return FetchResult(None, "httpx", 0, url, "httpx missing")
    try:
        with httpx.Client(http2=True, follow_redirects=True,
                          timeout=timeout,
                          headers={"User-Agent": UA_POOL[0],
                                   "Accept-Language": "en-CA,en;q=0.9"}) as client:
            r = client.get(url)
    except Exception as exc:                                    # noqa: BLE001
        return FetchResult(None, "httpx", 0, url, type(exc).__name__)
    if r.status_code == 200 and r.text:
        return FetchResult(r.text, "httpx", 200, str(r.url))
    return FetchResult(None, "httpx", r.status_code, url, f"HTTP {r.status_code}")


def _browser():
    global _PW_BROWSER
    from playwright.sync_api import sync_playwright
    if _PW_BROWSER is None:
        pw = sync_playwright().start()
        _PW_BROWSER = (pw, pw.chromium.launch(headless=True))
    return _PW_BROWSER


def _tier_playwright(url: str, timeout_ms: int) -> FetchResult:
    with _PW_LOCK:                     # sync API is not thread-safe
        try:
            _, browser = _browser()
            ctx = browser.new_context(
                user_agent=UA_POOL[0], locale="en-CA",
                viewport={"width": 1366, "height": 900})
            page = ctx.new_page()
            page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
            page.wait_for_timeout(1200)          # let client-side hydration settle
            html = page.content()
            final = page.url
            ctx.close()
        except Exception as exc:                                # noqa: BLE001
            return FetchResult(None, "playwright", 0, url, type(exc).__name__)
    if html:
        return FetchResult(html, "playwright", 200, final)
    return FetchResult(None, "playwright", 200, url, "empty document")


def fetch(url: str, *, gate: HostGate, timeout: float = 20.0,
          allow_playwright: bool = True) -> FetchResult:
    """Try each tier in order, stopping at the first non-empty document."""
    from urllib.parse import urlsplit
    host = urlsplit(url).netloc.lower()
    if gate.is_quarantined(host):
        return FetchResult(None, "none", 0, url, "host quarantined")
    gate.wait(host)

    first = _tier_curl(url, timeout, host, gate)
    if first.ok:
        return first

    if first.status in (301, 302, 303, 307, 308):
        gate.record(host, True)         # redirect handled by allow_redirects
    else:
        gate.record(host, False)

    if allow_playwright and not gate.is_quarantined(host):
        pw = _tier_playwright(url, int(timeout * 1500))
        if pw.ok:
            return pw
        last_ts = pw
    else:
        last_ts = first

    third = _tier_httpx(url, timeout, host, gate)
    if third.ok:
        return third
    return FetchResult(None, "none", third.status or last_ts.status, url,
                       f"{first.detail} | {third.detail}")
