"""Find a direct employee-referral artifact in a posting.

Scoring exists because English reuses the word "refer" for unrelated things:
"refer to the job description", "referred to as", "referral to a specialist".
Every pattern below is either an unambiguous referral artifact (a form field
named `referrer`, a `mailto:referrals@`) or is scored low enough that a single
ambiguous hit never wins.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

KINDS = ("form", "email", "page", "question")

# --- Negative patterns: force confidence to 0 -----------------------------
# `refer to` is the classic trap. Also "referral" in clinical/legal prose.
_NEGATIVE = re.compile(
    r"\brefer(?:red|ring)?\s+to\b"          # refer to the JD / referred to as
    r"|\breferral\s+to\s+(?:a\s+)?(?:specialist|clinician|physician|program\b)"
    r"|\bplease\s+refer\b",
    re.I,
)

# --- Positive text signals, with their base confidence --------------------
_TEXT_SIGNALS: tuple[tuple[re.Pattern[str], float, str], ...] = (
    (re.compile(r"\brefer\s+a\s+friend\b", re.I), 0.95, "refer a friend"),
    (re.compile(r"\brefer\s+someone\b", re.I), 0.9, "refer someone"),
    (re.compile(r"\bemployee\s+referral\s+(?:program|scheme|bonus)\b", re.I), 0.9,
     "employee referral program"),
    (re.compile(r"\breferral\s+bonus\b", re.I), 0.85, "referral bonus"),
    (re.compile(r"\breferral\s+(?:link|code|form|portal)\b", re.I), 0.9,
     "referral link/code/form"),
    (re.compile(r"\bknow\s+someone\s+who\b", re.I), 0.7, "know someone who"),
    (re.compile(r"\bhow\s+did\s+you\s+hear\b", re.I), 0.6, "how did you hear"),
    (re.compile(r"\bwere\s+you\s+referred\b", re.I), 1.0, "were you referred"),
    (re.compile(r"\bname\s+of\s+(?:the\s+)?(?:employee|referrer)\b", re.I), 0.95,
     "name of referrer"),
    (re.compile(r"\breferral\b", re.I), 0.35, "bare 'referral'"),
)

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_REFERRAL_EMAIL_LOCAL = re.compile(
    r"^(refer|referral|referrals|referafriend|refer-a-friend|employee\.?referral|"
    r"talent\.?referral|internal\.?referral)", re.I)
_REFERRAL_PATH = re.compile(
    r"(?:^|/)(?:refer|referral|referrals|refer-a-friend|employee-referral|"
    r"employee_referral|internal-referral|internal_referral|referral-program)"
    r"(?:/|$|\?)", re.I)
_REFERRAL_FIELD = re.compile(
    r"referr|referral|ref_code|refcode|referred_by|referrer_name|how_did_you_hear",
    re.I)


@dataclass
class ReferralHit:
    kind: str                      # form | email | page | question
    value: str                     # absolute URL (resolved later) or email
    pattern: str
    confidence: float
    evidence: str = ""
    attrs: dict = field(default_factory=dict)


def _snippet(text: str, start: int, end: int, radius: int = 110) -> str:
    lo = max(0, start - radius)
    hi = min(len(text), end + radius)
    return re.sub(r"\s+", " ", text[lo:hi]).strip()


def _score_text(text: str) -> tuple[float, str, str]:
    """Best text-only referral signal in a blob. Returns (conf, pattern, snippet)."""
    if not text:
        return 0.0, "", ""
    if _NEGATIVE.search(text) and not re.search(
            r"\brefer\s+a\s+friend|\bemployee\s+referral\s+program", text, re.I):
        # "refer to" only: the rest of this blob cannot be trusted for a bare
        # `referral` hit, but explicit artifacts were handled by callers.
        pass
    best = (0.0, "", "")
    for rx, conf, label in _TEXT_SIGNALS:
        m = rx.search(text)
        if not m:
            continue
        if conf < best[0]:
            continue
        window = text[max(0, m.start() - 160): m.end() + 160]
        if _NEGATIVE.search(window) and conf < 0.8:
            continue                     # ambiguous and sitting next to "refer to"
        best = (conf, label, _snippet(text, m.start(), m.end()))
    return best


def extract(html: str, *, title: str = "", company: str = "",
            structured_questions: list[str] | None = None) -> list[ReferralHit]:
    """Extract scored referral hits from a posting page or ATS payload."""
    hits: list[ReferralHit] = []
    if structured_questions:
        for q in structured_questions:
            conf, label, snip = _score_text(q or "")
            if conf >= 0.5:
                hits.append(ReferralHit("question", "", f"ats question: {label}",
                                        conf, f"application question: {q[:200]}"))

    if not html:
        return _rank(hits)

    soup = BeautifulSoup(html, "lxml")

    # 1. Anchors whose href or text looks like a referral target.
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = a.get_text(" ", strip=True)
        conf, label, snip = _score_text(f"{text} {href}")
        path_hit = bool(_REFERRAL_PATH.search(href))
        if path_hit:
            conf = max(conf, 0.9)
            label = label or "referral path"
        if conf >= 0.5:
            hits.append(ReferralHit("page", href, label or "anchor",
                                    min(conf, 1.0), snip or text[:160],
                                    {"href": href}))

    # 2. mailto: referral inboxes.
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.lower().startswith("mailto:"):
            continue
        addr = href[7:].split("?")[0].strip()
        for m in _EMAIL_RE.finditer(addr):
            email = m.group(0)
            local = email.split("@")[0]
            if _REFERRAL_EMAIL_LOCAL.search(local) or "refer" in href.lower():
                hits.append(ReferralHit("email", email, "mailto referral inbox",
                                        1.0, f"mailto link: {href[:160]}",
                                        {"href": href}))
                break

    # 3. Form fields and form actions.
    for tag in soup.find_all(["input", "select", "textarea"]):
        name = f"{tag.get('name') or ''} {tag.get('id') or ''} " \
               f"{tag.get('placeholder') or ''}"
        if _REFERRAL_FIELD.search(name):
            form = tag.find_parent("form")
            action = (form.get("action") if form else "") or ""
            hits.append(ReferralHit(
                "form", action, "referral form field", 1.0,
                f"field {tag.name} name={name.strip()[:80]}", {"action": action}))
    for form in soup.find_all("form", action=True):
        action = form["action"].strip()
        if _REFERRAL_PATH.search(action):
            hits.append(ReferralHit("form", action, "referral form action", 0.95,
                                    f"<form action='{action[:120]}'>",
                                    {"action": action}))

    # 4. Plain-text fallback over the visible copy.
    text = soup.get_text(" ", strip=True)
    conf, label, snip = _score_text(text)
    if conf >= 0.85:
        hits.append(ReferralHit("page", "", f"page text: {label}", conf, snip))

    return _rank(hits)


def _rank(hits: list[ReferralHit]) -> list[ReferralHit]:
    kind_bonus = {"form": 0.05, "email": 0.04, "question": 0.03, "page": 0.0}
    for h in hits:
        h.confidence = round(min(1.0, h.confidence + kind_bonus.get(h.kind, 0.0)), 3)
    hits.sort(key=lambda h: (-h.confidence, h.kind, h.value))
    out, seen = [], set()
    for h in hits:
        key = (h.kind, h.value.lower(), h.pattern)
        if key in seen:
            continue
        seen.add(key)
        out.append(h)
    return out[:12]


def best(hits: list[ReferralHit], *, threshold: float = 0.75) -> ReferralHit | None:
    for h in hits:
        if h.confidence >= threshold:
            return h
    return None
