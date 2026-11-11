#!/usr/bin/env python3
"""locscope.py — one answer to "which country does this location name?".

Two callers need it and they must never disagree: `scripts/enforce_canada_scope.py`
decides which rows leave a Canadian board, and `scripts/board_invariants.py`
audits what is left. When they disagreed on 2026-11-11 the audit reported 43
"non-Canada" rows the purge had deliberately kept (dual-location rows), and it
called `London, Middlesex` non-Canadian when Middlesex is a county in Ontario.

Returns:
    "ca"            a Canadian marker is present (country, province, city, ", ON")
    "us"            a US marker is present and Canada is not
    "<country>"     another named country
    None            the location names no country (ambiguous, not foreign)

`None` is deliberately not "Canada": absent evidence stays ambiguous and is
reported as a warning, never purged.
"""

from __future__ import annotations

import re
import unicodedata

CA = re.compile(
    r"\b(canada|canadian|ontario|quebec|british columbia|alberta|manitoba|"
    r"saskatchewan|nova scotia|new brunswick|newfoundland|prince edward island|"
    r"yukon|nunavut|northwest territories|"
    r"toronto|ottawa|montreal|montr[eé]al|laval|brossard|gatineau|sherbrooke|"
    r"mississauga|brampton|markham|vaughan|waterloo|kitchener|windsor|oshawa|"
    r"hamilton|calgary|edmonton|vancouver|victoria|kelowna|winnipeg|regina|"
    r"saskatoon|halifax|fredericton|moncton|etobicoke|scarborough|north york|"
    r"woodbridge|oakville|burlington|guelph|cambridge|kingston|london, on|"
    r",\s*(on|qc|ab|bc|mb|sk|ns|nb|nl|pe|yt|nt|nu)\b)", re.I)

US = re.compile(
    r"(\bus\b|\bunited states\b|\bu\.s\.a?\.|\busa\b|\bus\s*remote\b|"
    r"\bremote\s*[-,(]?\s*us\b|\b(anywhere in the us|us only|us-based)\b|"
    r"\b(alabama|alaska|arizona|arkansas|california|colorado|connecticut|delaware|"
    r"florida|hawaii|idaho|illinois|indiana|iowa|kansas|kentucky|louisiana|maine|"
    r"maryland|massachusetts|michigan|minnesota|mississippi|missouri|montana|"
    r"nebraska|nevada|new hampshire|new jersey|new mexico|new york|north carolina|"
    r"north dakota|ohio|oklahoma|oregon|pennsylvania|rhode island|south carolina|"
    r"south dakota|tennessee|texas|utah|vermont|virginia|west virginia|wisconsin|"
    r"wyoming|washington,?\s*d\.?c\.?|san francisco|chicago|boston|seattle|austin|"
    r"dallas|houston|atlanta|denver|phoenix|detroit|pittsburgh|los angeles|san diego|"
    r"san jose|sacramento|minneapolis|st\.? louis|cincinnati|cleveland|columbus)\b)", re.I)

# US state / district codes, matched case-sensitively against the raw string. A
# case-insensitive [A-Z]{2} turns the preposition "in" into Indiana and "or" into
# Oregon, which inflated the first Canada purge from 890 to 1,172 rows. `CA` is
# deliberately absent: on this board it is far more often Canada than California,
# and "Los Angeles, CA" is already caught by the city name.
US_STATE = re.compile(
    r"(?:^|[,/(\s])("
    r"AL|AK|AZ|AR|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|"
    r"MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC"
    r")(?=[\s,)/]|$)")

OFFSHORE = re.compile(
    r"\b(india|bengaluru|bangalore|hyderabad|pune|chennai|mumbai|gurgaon|noida|"
    r"philippines|manila|australia|sydney|melbourne|brisbane|perth|adelaide|"
    r"singapore|malaysia|united kingdom|england|scotland|wales|ireland|dublin|"
    r"poland|warsaw|romania|bucharest|brazil|mexico|argentina|chile|colombia|"
    r"japan|tokyo|germany|berlin|munich|spain|madrid|barcelona|france|paris|"
    r"israel|tel aviv|ukraine|netherlands|amsterdam|switzerland|italy|"
    r"united arab emirates|dubai|saudi arabia|qatar|south africa|new zealand)\b", re.I)


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text or "")
                   if not unicodedata.combining(c))


def region_of(location: str) -> str | None:
    """'ca' | 'us' | country token | None when the location names no country."""
    raw = strip_accents(location or "")
    s = raw.lower().strip()
    if not s:
        return None
    if CA.search(s):
        return "ca"
    if US_STATE.search(raw):
        return "us"
    if US.search(s):
        return "us"
    m = OFFSHORE.search(s)
    if m:
        return m.group(0)
    return None


def is_canadian(location: str) -> bool:
    return region_of(location) == "ca"


def is_foreign(location: str) -> bool:
    """Names a country and that country is not Canada."""
    region = region_of(location)
    return bool(region) and region != "ca"
