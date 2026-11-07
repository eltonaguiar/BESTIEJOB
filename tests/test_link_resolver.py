from scripts.referral.link_resolver import absolutize, dedupe, same_target, strip_tracking


def test_relative_path_resolves_against_posting():
    got = absolutize("/referrals/new", "https://boards.greenhouse.io/acme/jobs/1")
    assert got == "https://boards.greenhouse.io/referrals/new"


def test_query_only_href_resolves():
    got = absolutize("?refer=1", "https://jobs.lever.co/acme/abc")
    assert got == "https://jobs.lever.co/acme/abc?refer=1"


def test_rejects_mailto_and_javascript():
    assert absolutize("mailto:a@b.com", "https://x.test/") is None
    assert absolutize("javascript:void(0)", "https://x.test/") is None


def test_strip_tracking_removes_utm_keeps_meaning():
    got = strip_tracking("https://x.test/refer?utm_source=li&team=abc")
    assert "utm_source" not in got
    assert "team=abc" in got


def test_same_target_ignores_www_slash_and_utm():
    a = "https://www.x.test/refer/?utm_medium=email"
    b = "https://x.test/refer"
    assert same_target(a, b)


def test_dedupe_collapses_tracking_variants():
    urls = ["https://x.test/refer?utm_source=a", "https://x.test/refer",
            "https://x.test/other"]
    assert len(dedupe(urls)) == 2
