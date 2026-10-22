"""Devanagari normalisation and danda-aware sentence splitting."""
from hindi_rag.textutil import normalize, split_sentences


def test_nfc_makes_visually_identical_text_equal():
    precomposed = "क़"            # क़ as a single code point
    decomposed = "क़"       # क + nukta
    assert normalize(precomposed) == normalize(decomposed)


def test_invisible_characters_removed():
    assert normalize("कलाम‍ ​का") == "कलाम का"


def test_devanagari_digits_become_ascii():
    assert normalize("भारत रत्न १९९७") == "भारत रत्न 1997"


def test_duplicated_vowel_sign_from_pdf_layer_collapsed():
    assert normalize("अब्दुुल कलाम") == "अब्दुल कलाम"
    assert normalize("उड़ाान") == "उड़ान"


def test_audited_extraction_fix():
    assert normalize("अपने पूर्वर्तियों से") == "अपने पूर्ववर्तियों से"


def test_split_on_danda_question_and_exclamation():
    text = "कलाम का जन्म 1931 में हुआ। वे वैज्ञानिक थे। क्या आप जानते हैं? हाँ!"
    assert split_sentences(text) == ["कलाम का जन्म 1931 में हुआ।", "वे वैज्ञानिक थे।", "क्या आप जानते हैं?", "हाँ!"]


def test_latin_full_stop_is_not_a_boundary():
    sents = split_sentences("ए.पी.जे. अब्दुल कलाम महान थे। वे शिक्षक भी थे।")
    assert sents == ["ए.पी.जे. अब्दुल कलाम महान थे।", "वे शिक्षक भी थे।"]


def test_closing_quote_stays_with_its_sentence():
    sents = split_sentences('उन्होंने कहा, "सपने देखो।" फिर वे चले गए।')
    assert sents == ['उन्होंने कहा, "सपने देखो।"', "फिर वे चले गए।"]
