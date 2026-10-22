"""Devanagari-aware text normalisation and sentence segmentation.

The same `normalize()` is applied to the document at ingestion time and to every user
query, so visually identical strings always compare (and embed) identically.
"""
from __future__ import annotations

import re
import unicodedata

# Zero-width / invisible characters that make identical-looking words differ.
_INVISIBLE = dict.fromkeys(map(ord, "​‌‍⁠﻿­"))

# Devanagari digits -> ASCII digits, so "१९९७" and "1997" match.
_DIGITS = {ord("०") + i: ord("0") + i for i in range(10)}

# PDF text layers sometimes emit a dependent vowel sign twice ("अब्दुुल", "उड़ाान"), occasionally
# together with its anusvara ("मूल्यांांकन"). A repeated vowel-sign(+anusvara) unit is never valid
# Devanagari, so collapsing it is lossless.
_DUP_SIGN = re.compile(r"([ा-ौ][ंः]?|[ंः])\1+")

# Audited corrections: letters PyMuPDF drops that no general rule can recover. Found by diffing the
# extraction against a second extractor (poppler) over the whole PDF: exactly one word family is
# affected. ("पूर्वर्त-" is not Hindi; the document says "पूर्ववर्ती/पूर्ववर्तियों" = "predecessor(s)".)
_KNOWN_FIXES = (("पूर्वर्त", "पूर्ववर्त"),)

# Sentence boundary = whitespace that follows a danda (।), double danda (॥), ? or !, optionally
# followed by one closing quote/bracket that stays with the sentence it closes.
# A bare Latin "." is deliberately NOT a boundary: it would split "ए.पी.जे." and "3.5".
_SENTENCE_END = re.compile(r"(?<=[।॥?!][\"”’')\]])\s+|(?<=[।॥?!])\s+")

_SPACES = re.compile(r"[ \t\r\f\v  -  ]+")


def normalize(text: str) -> str:
    """NFC + invisible-char removal + duplicate-sign collapse + digit unification + space cleanup."""
    text = unicodedata.normalize("NFC", text)
    text = text.translate(_INVISIBLE).translate(_DIGITS)
    text = _DUP_SIGN.sub(r"\1", text)
    for wrong, right in _KNOWN_FIXES:
        text = text.replace(wrong, right)
    return _SPACES.sub(" ", text).strip()


def collapse_whitespace(text: str) -> str:
    """Normalise and also fold newlines into single spaces (for flowing prose)."""
    return re.sub(r"\s+", " ", normalize(text)).strip()


def split_sentences(text: str) -> list[str]:
    """Split on danda / ? / ! — the Hindi sentence terminators."""
    return [s.strip() for s in _SENTENCE_END.split(collapse_whitespace(text)) if s.strip()]


def strip_all_space(text: str) -> str:
    """Whitespace-free form, used only for tolerant substring checks in evaluation."""
    return re.sub(r"\s+", "", normalize(text))


def is_decorative(line: str) -> bool:
    """True for lines with no letters or digits at all (e.g. the cover's ✺ ornament)."""
    return not any(ch.isalnum() for ch in line)
