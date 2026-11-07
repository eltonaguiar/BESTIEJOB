from scripts.referral import ats_adapters as A
from scripts.referral.source_router import SourceKind


def test_greenhouse_url_variants_parse():
    for url in ("https://boards.greenhouse.io/geotab/jobs/4567890",
                "https://job-boards.greenhouse.io/geotab/jobs/4567890",
                "https://boards-api.greenhouse.io/v1/boards/geotab/jobs/4567890"):
        m = A.GH_API_PATH.search(url) or A.GH_PATH.search(url)
        assert m and m.group(1) == "geotab" and m.group(2) == "4567890", url


def test_lever_uuid_parses():
    m = A.LEVER_PATH.search(
        "/pointclickcare/1f2e3d4c-5b6a-7890-abcd-ef1234567890")
    assert m and m.group(1) == "pointclickcare"


def test_smartrecruiters_parses():
    m = A.SR_PATH.search("/ServiceNow/744000160277860")
    assert m and m.group(1) == "ServiceNow"


def test_workday_has_no_api():
    assert A.has_api(SourceKind.ATS_WORKDAY) is False
    assert A.has_api(SourceKind.ATS_GREENHOUSE) is True


def test_unknown_kind_returns_not_ok():
    payload = A.fetch(SourceKind.COMPANY_DIRECT, "https://example.test/job/1")
    assert payload.ok is False


def test_workday_adapter_is_not_ok():
    payload = A.fetch(SourceKind.ATS_WORKDAY,
                      "https://bmo.wd3.myworkdayjobs.com/en-US/External/job/x")
    assert payload.ok is False
