"""Central configuration. Every value can be overridden with an environment variable,
so nothing is hard-coded and no secret ever needs to live in the repo."""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:  # optional: read API keys / settings from a local .env file (never committed, see .gitignore)
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:
    pass


def _env(name: str, default):
    value = os.getenv(name)
    return type(default)(value) if value not in (None, "") else default


# ---- paths ---------------------------------------------------------------------------
PDF_PATH = Path(os.getenv("RAG_PDF", ROOT / "data" / "Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf"))
CHROMA_DIR = Path(os.getenv("RAG_CHROMA_DIR", ROOT / "chroma_db"))
OUTPUT_DIR = ROOT / "outputs"
GOLD_PATH = ROOT / "eval" / "gold.json"

# ---- embeddings ----------------------------------------------------------------------
# bge-m3 is trained for multilingual + cross-lingual retrieval (100+ languages incl. Hindi).
EMBED_MODEL = os.getenv("RAG_EMBED_MODEL", "BAAI/bge-m3")

# ---- chunking (sizes are measured in *embedding-model tokens*, not characters) --------
CHUNK_MAX_TOKENS = _env("RAG_CHUNK_MAX_TOKENS", 200)   # ceiling for a chunk (median paragraph here = 21 tokens, max 169)
CHUNK_OVERLAP_TOKENS = _env("RAG_CHUNK_OVERLAP", 40)   # sentence overlap, used only if one paragraph exceeds the ceiling

# ---- retrieval -----------------------------------------------------------------------
TOP_K = _env("RAG_TOP_K", 4)                # chunks retrieved and given to the LLM
QUERY_INT8 = os.getenv("RAG_QUERY_INT8", "0") == "1"   # int8 query encoder on CPU (faster; see README)
EXPAND_TABLES = os.getenv("RAG_EXPAND_TABLES", "1") == "1"  # add sibling rows of small tables to the context
TABLE_EXPAND_MAX = _env("RAG_TABLE_EXPAND_MAX", 8)          # a table with at most this many rows is one unit
MIN_SCORE = _env("RAG_MIN_SCORE", 0.30)     # below this the system answers "not found" instead of guessing

# ---- generation ----------------------------------------------------------------------
# auto | hf (local, no key) | groq | gemini | openai | ollama | anthropic | extractive (no LLM)
# "auto" uses the first hosted API whose key is set, otherwise the local Hugging Face model.
def _auto_backend() -> str:
    for backend, key in (("groq", "GROQ_API_KEY"), ("gemini", "GEMINI_API_KEY"),
                         ("openai", "OPENAI_API_KEY"), ("anthropic", "ANTHROPIC_API_KEY")):
        if os.getenv(key):
            return backend
    return "hf"


LLM_BACKEND = os.getenv("RAG_LLM", "auto")
if LLM_BACKEND == "auto":
    LLM_BACKEND = _auto_backend()
HF_LLM_MODEL = os.getenv("RAG_HF_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
LLM_MODEL = os.getenv("RAG_LLM_MODEL", "")  # for anthropic/openai backends; empty -> backend default
MAX_NEW_TOKENS = _env("RAG_MAX_NEW_TOKENS", 160)

# ---- document structure --------------------------------------------------------------
# A page whose first line is one of these is navigation, not content.
NON_CONTENT_HEADINGS = ("विषय-सूची",)


def model_slug(name: str = EMBED_MODEL) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()


def collection_name(name: str = EMBED_MODEL) -> str:
    # one collection per embedding model: vectors from different models must never be mixed
    return f"kalam_{model_slug(name)}"[:63]
