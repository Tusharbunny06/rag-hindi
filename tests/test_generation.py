"""Citation formatting, [n] marker parsing, abstention and grounding checks (no model or API needed)."""
from hindi_rag.evaluate import keywords_ok
from hindi_rag.llm import not_found_message, parse_generation
from hindi_rag.pipeline import _unverified_numbers
from hindi_rag.vectorstore import Hit


def hit(chunk_id=19, page=8, text="SLV-III ने 1980 में रोहिणी उपग्रह को कक्षा में स्थापित किया।", score=0.6849):
    return Hit(chunk_id, page, page, "इसरो के वर्ष और SLV-III", "", "text", text, score)


def test_citation_format_matches_assignment():
    assert hit().citation() == 'page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 19 · score: 0.68'


def test_parse_markers_and_ignore_out_of_range():
    gen = parse_generation("Arun Tiwari co-wrote it; published 1999. [1][3][7]", n_hits=4)
    assert gen.text == "Arun Tiwari co-wrote it; published 1999."
    assert gen.cited == [0, 2] and not gen.not_found


def test_not_found_is_abstention_in_question_language():
    assert parse_generation("NOT_FOUND", 4).not_found
    assert not_found_message("Who won the World Cup?").startswith("The document does not")
    assert not_found_message("विश्व कप किसने जीता?").startswith("दस्तावेज़")


def test_numbers_not_in_context_are_flagged():
    assert _unverified_numbers("Rohini, in 1980.", [hit()]) == []
    assert _unverified_numbers("Rohini, in 1981.", [hit()]) == ["1981"]


def test_answer_keyword_scoring_accepts_hindi_or_english():
    groups = [["Tiwari", "तिवारी"], ["1999"]]
    assert keywords_ok("अरुण तिवारी के साथ, 1999 में।", groups)
    assert keywords_ok("Arun Tiwari, 1999", groups)
    assert not keywords_ok("Arun Tiwari", groups)
