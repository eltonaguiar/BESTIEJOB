#!/usr/bin/env python3
"""crossurl.py — decide whether two rows are the SAME posting under different URLs.

The merger dedupes on normalized URL. That misses the most common real duplicate
on this board: one requisition that reaches us twice under two labels --

    Take-Two Interactive / "ServiceNow ITOM Lead"  (aggregator, jobs.lever.co URL)
    take2games           / "ServiceNow ITOM Lead"  (employer ATS, jobs.ashbyhq URL)

Same job, two URLs, two different spellings of the employer -- so it survives as
two rows and a job seeker applies twice.

Matching here is deliberately narrow. A job board that collapses two genuine
requisitions is worse than one that shows a duplicate: the seeker loses a role.
So all four of these must hold:

  1. company  — the labels resolve to the same employer (alias-aware)
  2. title    — token-overlap >= TITLE_SIM after removing market noise words
  3. level    — identical seniority words ("Developer" != "Senior Developer",
                "II" != "III"); GDIT and Cognizant post every level separately
  4. location — same city, or one side has no city at all

`location` is compared at city level first: "Toronto, ON" and "Ottawa, ON" must
never collapse, even for the same company and title.
"""

from __future__ import annotations

import re

# Words that describe how/where a job is sold, not what the job is. Aggregators
# append these inconsistently to the same requisition.
NOISE = frozenset("""
remote canada canadian hybrid onsite fully 100 telecommute wfh
""".split())

# Words that are so generic they say nothing about identity.
STOP = frozenset("""
the and of for a an at in on with
""".split())

# Legal / structural suffixes that differ between an employer's own name and the
# handle it uses on an ATS. "Lightspeed Commerce" and "lightspeedhq" are one
# employer; "NewRocket" and "Highmetric" are not, and must not collapse.
SUFFIX = frozenset("""
inc incorporated ltd limited corp corporation co company llc llp plc
canada ca usa us
technologies technology tech solutions solution group groupinc
systems system services service consulting consultants
holdings holding international global worldwide
labs lab software studios studio media digital
hq headquarters
commerce games gaming interactive entertainment
""".split())

# Digit words, so "Take-Two" and "take2" land on the same key.
DIGITS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
          "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}

# Seniority/level markers. Compared as a SET and required to match exactly.
LEVEL = re.compile(
    r"\b(sr|senior|jr|junior|lead|principal|staff|chief|head|vp|director|manager|"
    r"intern|co-?op|associate|i{1,3}|iv|v|[1-5])\b", re.I)

CAMEL = re.compile(r"(?<=[a-z])(?=[A-Z])")


def _squash(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def company_key(name: str) -> str:
    """Collapse an employer label to its identity token.

    'Lightspeed Commerce' -> 'lightspeed'    'lightspeedhq' -> 'lightspeed'
    'Take-Two Interactive' -> 'take2'       'take2games'   -> 'take2'
    'CGI Inc.'             -> 'cgi'
    """
    raw = CAMEL.sub(" ", name or "")
    raw = raw.lower().replace("&", " and ")
    # Split the handle-style compound too: 'lightspeedhq' has no boundary, so
    # strip known suffixes off the end of the squashed string as well.
    tokens = [t for t in re.split(r"[^a-z0-9]+", raw) if t and t not in STOP]
    tokens = [DIGITS.get(t, t) for t in tokens]
    tokens = [t for t in tokens if t not in SUFFIX]
    squashed = "".join(tokens)
    for suf in sorted(SUFFIX, key=len, reverse=True):
        if len(squashed) - len(suf) >= 3 and squashed.endswith(suf):
            squashed = squashed[: -len(suf)]
            break
    return squashed or _squash(name)


def company_match(a: str, b: str) -> bool:
    ka, kb = company_key(a), company_key(b)
    if not ka or not kb:
        return False
    if ka == kb:
        return True
    # One side abbreviated: 'acme' vs 'acmesystems' (systems already stripped,
    # so this mostly catches 'salesforce' vs 'salesforcecanada').
    short, long = sorted((ka, kb), key=len)
    if len(short) >= 4 and long.startswith(short):
        return True
    ta = {t for t in re.split(r"[^a-z0-9]+", (a or "").lower()) if t and t not in STOP
          and t not in SUFFIX}
    tb = {t for t in re.split(r"[^a-z0-9]+", (b or "").lower()) if t and t not in STOP
          and t not in SUFFIX}
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= 0.6


def title_tokens(title: str) -> frozenset[str]:
    t = re.sub(r"\([^)]*\)", " ", (title or "").lower())
    t = re.sub(r"[^a-z0-9+#/ ]", " ", t)
    t = re.sub(r"\bsr\.?\b", " ", t)
    words = {w for w in t.split() if w and w not in NOISE and w not in STOP}
    return frozenset(w.rstrip(".") for w in words)


def level_set(title: str) -> frozenset[str]:
    out = set()
    for m in LEVEL.finditer((title or "").lower()):
        w = m.group(1).lower()
        # normalise so 'sr' and 'senior' are one marker
        out.add({"senior": "sr", "junior": "jr"}.get(w, w))
    return frozenset(out)


def title_sim(a: str, b: str) -> float:
    ta, tb = title_tokens(a), title_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def city(location: str) -> str:
    """City-level key. Never returns a country or a count."""
    l = (location or "").lower()
    l = re.split(r"[,;/(]", l)[0]
    l = re.sub(r"\b(remote|hybrid|onsite|united states|usa|canada)\b", " ", l)
    l = re.sub(r"[^a-z ]", " ", l)
    return re.sub(r"\s+", " ", l).strip()


def location_match(a: str, b: str) -> bool:
    ca, cb = city(a), city(b)
    if not ca or not cb:
        return True            # one side unknown: not grounds to reject
    return ca == cb


TITLE_SIM = 0.75


def same_posting(a: dict, b: dict, *, title_sim_min: float = TITLE_SIM) -> bool:
    """True when two row dicts are one posting (company/title/location keys)."""
    if not company_match(a.get("company", ""), b.get("company", "")):
        return False
    if level_set(a.get("title", "")) != level_set(b.get("title", "")):
        return False
    if title_sim(a.get("title", ""), b.get("title", "")) < title_sim_min:
        return False
    return location_match(a.get("location", ""), b.get("location", ""))


def describe(a: dict, b: dict) -> str:
    return (f"company {company_key(a.get('company',''))!r}~"
            f"{company_key(b.get('company',''))!r} "
            f"title_sim={title_sim(a.get('title',''), b.get('title','')):.2f}")
