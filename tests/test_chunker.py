"""Section-aware chunking, table rows, non-answerable pages, sentence-boundary splitting."""
from hindi_rag import config
from hindi_rag.chunker import build_chunks
from hindi_rag.pdf_extract import Block


def words(text: str) -> int:  # stand-in tokenizer so tests need no model download
    return len(text.split())


BLOCKS = [
    Block(1, "paragraph", "अग्नि की उड़ान"),                           # cover title
    Block(2, "paragraph", "1 · बचपन"),                                 # numbered heading
    Block(2, "paragraph", "कलाम का जन्म रामेश्वरम में हुआ। उनके पिता नाव चलाते थे।"),
    Block(2, "table", header=["वर्ष", "सम्मान"], rows=[["1997", "भारत रत्न"], ["1990", "पद्म विभूषण"]]),
    Block(3, "paragraph", "2 · प्रश्न"),
    Block(3, "paragraph", "कलाम कहाँ पैदा हुए? उनका पहला रॉकेट कौन सा था?"),
]


def test_sections_tables_and_metadata():
    chunks = build_chunks(BLOCKS, words)
    text, row1, row2, questions = chunks
    assert (text.section, text.kind, text.page) == ("बचपन", "text", 2)
    assert text.text == "कलाम का जन्म रामेश्वरम में हुआ। उनके पिता नाव चलाते थे।"
    assert (row1.text, row1.kind, row1.section) == ("1997: भारत रत्न", "table_row", "बचपन")
    assert row1.table_id == row2.table_id and row1.table_rows == 2
    assert questions.kind == "question_list" and not questions.answerable
    meta = row1.metadata("doc.pdf")
    assert {"page", "section", "chunk_id", "answerable", "table_id"} <= meta.keys()
    assert [c.chunk_id for c in chunks] == [0, 1, 2, 3]


def test_long_paragraph_splits_only_at_dandas_with_overlap(monkeypatch):
    monkeypatch.setattr(config, "CHUNK_MAX_TOKENS", 10)
    monkeypatch.setattr(config, "CHUNK_OVERLAP_TOKENS", 6)
    sents = ["कलाम ने पहला रॉकेट बनाया।", "कलाम ने दूसरा रॉकेट बनाया।", "कलाम ने तीसरा रॉकेट बनाया।",
             "कलाम ने चौथा रॉकेट बनाया।"]
    chunks = build_chunks([Block(1, "paragraph", "1 · रॉकेट"), Block(1, "paragraph", " ".join(sents))], words)
    assert [c.text for c in chunks] == [" ".join(sents[0:2]), " ".join(sents[1:3]), " ".join(sents[2:4])]
    assert all(c.text.endswith("।") and c.n_tokens <= 10 for c in chunks)
