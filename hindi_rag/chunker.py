"""Section-aware, danda-aware, token-counted chunking with citation metadata.

Strategy (justified by measurements on this PDF: 219 sentences, mean 25 tokens; paragraphs
median 21 / max 169 tokens; ~270 narrative tokens per section):
  1. Respect document structure first: a chunk never crosses a section or sub-heading boundary,
     and every table row becomes its own self-contained chunk ("year: 1997; award: भारत रत्न; ...").
  2. Inside a section, pack whole paragraphs up to CHUNK_MAX_TOKENS (measured with the embedding
     model's own tokenizer, because Devanagari is ~3.5 chars/token, not 4-5 like English).
  3. If a single paragraph is longer than the ceiling, split it only at Hindi sentence ends
     (danda / ? / !), carrying the last sentence(s) (<= CHUNK_OVERLAP_TOKENS) into the next chunk
     so a fact that straddles the cut stays retrievable.
  4. Navigation pages (table of contents) and exercise pages (a list of questions with no answers)
     are indexed but tagged answerable=False: they echo user questions almost verbatim, so they
     would otherwise outrank the passages that actually contain the answer.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

from . import config
from .pdf_extract import Block
from .textutil import collapse_whitespace, split_sentences

_NUMBERED_HEADING = re.compile(r"^(\d+)\s*·\s*(.+)$")
_TERMINAL = tuple("।॥?!.:")
_PLACEHOLDER_CELLS = {"", "—", "-", "–"}


@dataclass
class Chunk:
    chunk_id: int
    page: int
    page_end: int
    section: str
    section_no: int
    subsection: str
    kind: str           # "text" | "table_row" | "question_list" | "toc"
    text: str
    n_tokens: int
    table_id: int = -1  # rows of the same table share an id (used to expand a hit to its whole table)
    table_rows: int = 0  # number of rows in that table

    @property
    def answerable(self) -> bool:
        return self.kind in ("text", "table_row")

    @property
    def embed_text(self) -> str:
        """What is actually embedded: the text with its section title as a context header, so a
        sentence like "उन्होंने इसे स्वीकार किया" still knows which topic it belongs to."""
        header = f"{self.section} — {self.subsection}" if self.subsection else self.section
        return f"{header}\n{self.text}"

    def metadata(self, source: str) -> dict:
        return {
            "chunk_id": self.chunk_id, "page": self.page, "page_end": self.page_end,
            "section": self.section, "section_no": self.section_no, "subsection": self.subsection,
            "kind": self.kind, "answerable": self.answerable, "n_tokens": self.n_tokens, "source": source,
            "table_id": self.table_id, "table_rows": self.table_rows,
        }


@dataclass
class _Section:
    no: int
    title: str
    kind: str = "text"
    blocks: list[Block] = field(default_factory=list)


@dataclass
class _Sent:
    text: str
    tokens: int
    page: int
    para: int
    subsection: str


def _heading_of(block: Block, first_on_page: bool) -> tuple[int, str] | None:
    """A numbered line ("5 · वैज्ञानिक करियर...") is always a heading; so is a short, unpunctuated
    first line of a page (cover / contents page)."""
    m = _NUMBERED_HEADING.match(block.text)
    if m:
        return int(m.group(1)), m.group(2).strip()
    if first_on_page and len(block.text) <= 60 and not block.text.endswith(_TERMINAL):
        return 0, block.text
    return None


def _split_sections(blocks: list[Block]) -> list[_Section]:
    sections: list[_Section] = []
    seen_pages: set[int] = set()
    for block in blocks:
        first_on_page = block.page not in seen_pages
        seen_pages.add(block.page)
        heading = _heading_of(block, first_on_page) if block.kind == "paragraph" else None
        if heading:
            no, title = heading
            kind = "toc" if title in config.NON_CONTENT_HEADINGS else "text"
            sections.append(_Section(no=no, title=title, kind=kind))
            continue
        if not sections:  # content before any heading
            sections.append(_Section(no=0, title="(प्रस्तावना)"))
        sections[-1].blocks.append(block)

    for sec in sections:  # a section that is mostly questions is an exercise list, not evidence
        sents = [s for b in sec.blocks if b.kind == "paragraph" for s in split_sentences(b.text)]
        if sec.kind == "text" and sents and sum(s.endswith("?") for s in sents) / len(sents) >= 0.5:
            sec.kind = "question_list"
    return sections


def _is_subheading(block: Block, next_block: Block | None, section_no: int) -> bool:
    """Short, unpunctuated one-line paragraph directly above real body text, inside a numbered section."""
    return (
        section_no > 0 and block.kind == "paragraph" and len(block.text) <= 50
        and not block.text.endswith(_TERMINAL) and not re.match(r"^\d+[.)]", block.text)
        and next_block is not None and next_block.page == block.page
        and (next_block.kind == "table" or len(next_block.text) >= 2 * len(block.text))
    )


def _row_text(header: list[str], row: list[str]) -> str:
    """Turn a table row into one natural sentence-like string that embeds well."""
    cells = [(h, c) for h, c in zip(header, row) if c not in _PLACEHOLDER_CELLS]
    if len(header) == 2 and len(cells) == 2:      # key/value tables: "जन्म: 15 अक्टूबर 1931, ..."
        return f"{cells[0][1]}: {cells[1][1]}"
    return "; ".join(f"{h}: {c}" for h, c in cells)


def build_chunks(blocks: list[Block], count_tokens: Callable[[str], int]) -> list[Chunk]:
    max_tok, overlap_tok = config.CHUNK_MAX_TOKENS, config.CHUNK_OVERLAP_TOKENS
    chunks: list[Chunk] = []
    n_tables = 0

    for sec in _split_sections(blocks):
        cur: list[_Sent] = []

        def emit(sents: list[_Sent], chunk_kind: str, table_id: int = -1, table_rows: int = 0) -> None:
            if not sents:
                return
            text = " ".join(s.text for s in sents)
            chunks.append(Chunk(
                chunk_id=len(chunks), page=sents[0].page, page_end=sents[-1].page, section=sec.title,
                section_no=sec.no, subsection=sents[0].subsection, kind=chunk_kind, text=text,
                n_tokens=count_tokens(text), table_id=table_id, table_rows=table_rows,
            ))

        def flush() -> None:
            nonlocal cur
            emit(cur, sec.kind)
            cur = []

        subsection = ""
        for i, block in enumerate(sec.blocks):
            nxt = sec.blocks[i + 1] if i + 1 < len(sec.blocks) else None
            if block.kind == "table":
                flush()
                rows = [t for t in (collapse_whitespace(_row_text(block.header, r)) for r in block.rows) if t]
                for text in rows:
                    emit([_Sent(text, count_tokens(text), block.page, i, subsection)],
                         "table_row" if sec.kind == "text" else sec.kind, table_id=n_tables, table_rows=len(rows))
                n_tables += 1
                continue
            if _is_subheading(block, nxt, sec.no):
                flush()
                subsection = block.text
                continue

            sents = [_Sent(s, count_tokens(s), block.page, i, subsection) for s in split_sentences(block.text)]
            para_tokens = sum(s.tokens for s in sents)
            if para_tokens <= max_tok:  # whole paragraph fits: keep it intact
                if sum(s.tokens for s in cur) + para_tokens > max_tok:
                    flush()
                cur.extend(sents)
                continue
            for s in sents:             # oversized paragraph: split at sentence ends with overlap
                if cur and sum(c.tokens for c in cur) + s.tokens > max_tok:
                    carry: list[_Sent] = []
                    for prev in reversed(cur):
                        if prev.para != s.para or sum(c.tokens for c in carry) + prev.tokens > overlap_tok:
                            break
                        carry.insert(0, prev)
                    flush()
                    cur = carry
                cur.append(s)
        flush()

    return chunks
