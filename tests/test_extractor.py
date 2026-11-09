from pathlib import Path

from scripts.referral.extractor import best, extract

FIXTURE = Path(__file__).parent / "fixtures" / "referral_page.html"
HTML = FIXTURE.read_text(encoding="utf-8")


def test_finds_refer_a_friend_anchor():
    hits = extract(HTML)
    anchors = [h for h in hits if h.pattern in ("refer a friend", "referral path")
               or "refer a friend" in h.evidence.lower()]
    assert anchors, [h.pattern for h in hits]
    assert any(h.kind == "page" for h in hits)


def test_finds_referral_mailto_inbox():
    emails = [h.value for h in extract(HTML) if h.kind == "email"]
    assert "referrals@acme.test" in emails
    assert "careers@acme.test" not in emails     # not a referral inbox


def test_finds_referral_form_field():
    forms = [h for h in extract(HTML) if h.kind == "form"]
    assert forms, "referrer_name field must be detected"
    assert forms[0].confidence >= 0.9


def test_refer_to_the_job_description_is_not_a_hit():
    html = "<html><body><p>Please refer to the job description for details. " \
           "This is referred to as a level 3 role.</p></body></html>"
    assert best(extract(html)) is None


def test_bare_referral_alone_below_threshold():
    html = "<html><body><p>Referral to a specialist may be required.</p></body></html>"
    assert best(extract(html)) is None


def test_ats_question_hit_is_top_confidence():
    hits = extract("", structured_questions=[
        "Were you referred by a current employee? If so, please provide their name."])
    top = best(hits)
    assert top is not None
    assert top.kind == "question"
    assert top.confidence >= 0.9


def test_generic_how_did_you_hear_is_weak_but_present():
    hits = extract("", structured_questions=["How did you hear about this role?"])
    assert any(h.pattern.endswith("how did you hear") for h in hits)
    assert best(hits) is None          # 0.6 + 0.03 bonus < 0.75 threshold


def test_empty_input_returns_empty():
    assert extract("") == []
    assert extract("", structured_questions=[]) == []


def test_preferred_name_is_not_a_hit():
    html = '<html><body><input name="preferred_name" type="text"></body></html>'
    assert best(extract(html)) is None
