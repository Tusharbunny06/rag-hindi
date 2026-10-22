"""Layout-aware extraction of text *and tables* from the Hindi PDF using PyMuPDF.

Why this design (all findings come from testing five extractors on this exact PDF):
  * pdfplumber/pdfminer drop conjunct consonants ("अग्नि" -> "अ  क") -> unusable for Devanagari.
  * pdfium inserts spurious spaces after matras ("कला म") and duplicates characters.
  * PyMuPDF's letters are correct once a repeated dependent vowel sign is collapsed (textutil.normalize).
  * PyMuPDF's own table-cell text is scrambled, but its table *geometry* is right, so we use
    `find_tables()` only for cell rectangles and read the text inside each rectangle ourselves.
Pure-pip dependency: no poppler / OCR binaries, so it runs the same on Windows, macOS and Linux.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from .textutil import collapse_whitespace, is_decorative

# A line is a new paragraph if the vertical gap above it exceeds this fraction of its height.
_PARA_GAP_RATIO = 0.6
# A line that stops this many points short of the page's right text edge ends its paragraph.
_SHORT_LINE_MARGIN = 25.0


@dataclass
class Block:
    page: int                       # 1-based physical PDF page
    kind: str                       # "paragraph" | "table"
    text: str = ""                  # paragraph text
    header: list[str] = field(default_factory=list)       # table header cells
    rows: list[list[str]] = field(default_factory=list)   # table body rows
    y: float = 0.0                  # top edge, used to keep reading order


def _line_text(raw: str) -> str:
    """One PyMuPDF block == one visual line. Its inner '\\n' marks a font-run boundary, which can
    fall *inside* a word ("निष्क्रि\\nय"), so it is deleted, never turned into a space. Real word
    breaks keep their own leading space (" की"), so nothing is glued together."""
    return collapse_whitespace(raw.strip("\n").replace("\n", ""))


def _inside(rect: pymupdf.Rect, container: pymupdf.Rect) -> bool:
    area = rect.get_area()
    return area > 0 and (rect & container).get_area() > 0.5 * area


def _cell_text(page: pymupdf.Page, bbox) -> str:
    x0, y0, x1, y1 = bbox
    clip = pymupdf.Rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1)  # 1pt inset: ignore neighbour-cell overlap
    lines = [_line_text(b[4]) for b in page.get_text("blocks", clip=clip, sort=True) if b[6] == 0]
    return collapse_whitespace(" ".join(l for l in lines if l))


def _real_tables(page: pymupdf.Page):
    # a 1-row / 1-column "table" is just a styled callout box, not data
    return [t for t in page.find_tables().tables if len(t.rows) >= 2 and t.col_count >= 2]


def _table_blocks(page: pymupdf.Page, page_no: int, tables) -> list[Block]:
    out = []
    for t in tables:
        grid = [[_cell_text(page, c) if c else "" for c in row.cells] for row in t.rows]
        out.append(Block(page=page_no, kind="table", header=grid[0], rows=grid[1:], y=t.bbox[1]))
    return out


def _paragraphs(page: pymupdf.Page, page_no: int, table_rects: list[pymupdf.Rect]) -> list[Block]:
    lines = []  # (y0, y1, x1, text)
    for x0, y0, x1, y1, raw, _no, btype in page.get_text("blocks", sort=True):
        if btype != 0:
            continue
        if any(_inside(pymupdf.Rect(x0, y0, x1, y1), tr) for tr in table_rects):
            continue
        text = _line_text(raw)
        if text and not is_decorative(text):
            lines.append((y0, y1, x1, text))
    if not lines:
        return []

    right_edge = max(l[2] for l in lines)
    paragraphs: list[list[tuple]] = [[lines[0]]]
    for prev, cur in zip(lines, lines[1:]):
        height = max(cur[1] - cur[0], 1.0)
        new_para = (cur[0] - prev[1]) > _PARA_GAP_RATIO * height or prev[2] < right_edge - _SHORT_LINE_MARGIN
        if new_para:
            paragraphs.append([cur])
        else:
            paragraphs[-1].append(cur)

    blocks = []
    for para in paragraphs:
        text = ""
        for _, _, _, line in para:
            # a line ending in a hyphen continues the same compound word ("रिट्रीवल-" + "ऑगमेंटेड")
            text = text + line if text.endswith("-") else (text + " " + line).strip()
        blocks.append(Block(page=page_no, kind="paragraph", text=text, y=para[0][0]))
    return blocks


def extract_blocks(pdf_path: str | Path) -> list[Block]:
    """Return paragraphs and tables for every page, in reading order."""
    doc = pymupdf.open(str(pdf_path))
    out: list[Block] = []
    for page_no, page in enumerate(doc, start=1):
        tables = _real_tables(page)
        table_rects = [pymupdf.Rect(t.bbox) for t in tables]
        page_blocks = _paragraphs(page, page_no, table_rects) + _table_blocks(page, page_no, tables)
        out.extend(sorted(page_blocks, key=lambda b: b.y))
    doc.close()
    return out
