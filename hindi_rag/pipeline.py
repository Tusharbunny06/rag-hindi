"""Question -> retrieve -> grounded answer -> citations, plus output formatting."""
from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass, field

import numpy as np

from . import config
from .llm import SYSTEM_PROMPT, ChatLLM, build_user_prompt, get_llm, not_found_message, parse_generation
from .textutil import normalize, split_sentences
from .vectorstore import Hit, Retriever


@dataclass
class Answer:
    query: str
    answer: str
    cited: list[Hit]                  # the chunks the answer is attributed to
    retrieved: list[Hit]              # everything the LLM was shown
    backend: str
    citation_mode: str                # "model" | "lexical" | "top-1" | "extractive" | "none"
    grounded: bool = True             # every number in the answer occurs in the retrieved context
    abstained: bool = False
    ungrounded_numbers: list[str] = field(default_factory=list)
    retrieval_ms: float = 0.0         # query embedding + vector search
    llm_ttft_ms: float | None = None  # LLM request -> first streamed text
    llm_total_ms: float | None = None

    @property
    def ttft_ms(self) -> float | None:
        """End-to-end time to first token as a user would see it: retrieval + LLM first token."""
        return None if self.llm_ttft_ms is None else self.retrieval_ms + self.llm_ttft_ms


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[ऀ-ॿ]{2,}|[A-Za-z0-9\-]{2,}", normalize(text))}


def _attribute(answer: str, hits: list[Hit]) -> tuple[list[Hit], str]:
    """Fallback when the model gave no valid [n] marker: cite the chunk(s) that share the most
    tokens with the answer (works for numbers/names), else the top-ranked chunk."""
    ans = _tokens(answer)
    overlap = [len(ans & _tokens(h.text)) for h in hits]
    if overlap and max(overlap) > 0:
        best = max(overlap)
        return [h for h, o in zip(hits, overlap) if o == best][:2], "lexical"
    return hits[:1], "top-1"


def _unverified_numbers(answer: str, hits: list[Hit]) -> list[str]:
    context = normalize(" ".join(h.text for h in hits))
    return [n for n in dict.fromkeys(re.findall(r"\d+", normalize(answer))) if n not in context]


class RAGPipeline:
    def __init__(self, retriever: Retriever | None = None, backend: str | None = None, low_memory: bool | None = None):
        self.retriever = retriever or Retriever()
        self.backend = (backend or config.LLM_BACKEND).lower()
        if low_memory is None:  # default: free the embedder before loading a local LLM on machines < 15 GB RAM
            from .llm import _total_ram_gb
            env = os.getenv("RAG_LOW_MEMORY")
            low_memory = env == "1" if env in ("0", "1") else (self.backend == "hf" and _total_ram_gb() < 15)
        self.low_memory = low_memory
        self._llm: ChatLLM | None = None
        self._warm = False

    # -- generation ------------------------------------------------------------------------
    def _extractive(self, query: str, hits: list[Hit]) -> tuple[str, list[Hit]]:
        """No-LLM fallback: the single context sentence most similar to the question."""
        emb = self.retriever.embedder
        pairs = [(s, h) for h in hits for s in (split_sentences(h.text) or [h.text])]
        sims = emb.embed_passages([s for s, _ in pairs]) @ emb.embed_queries([normalize(query)])[0]
        sentence, hit = pairs[int(np.argmax(sims))]
        return sentence, [hit]

    def _answer_one(self, query: str, hits: list[Hit], retrieval_ms: float) -> Answer:
        if not hits or hits[0].score < config.MIN_SCORE:
            return Answer(query, not_found_message(query), [], hits, self.backend, "none", abstained=True,
                          retrieval_ms=retrieval_ms)

        if self.backend == "extractive":
            text, cited = self._extractive(query, hits)
            return Answer(query, text, cited, hits, "extractive", "extractive", retrieval_ms=retrieval_ms)

        comp = self._llm.complete(SYSTEM_PROMPT, build_user_prompt(query, hits))
        timing = {"retrieval_ms": retrieval_ms, "llm_ttft_ms": comp.ttft_ms, "llm_total_ms": comp.total_ms}
        gen = parse_generation(comp.text, len(hits))
        if gen.not_found or not gen.text:
            return Answer(query, not_found_message(query), [], hits, self._llm.name, "none", abstained=True, **timing)
        if gen.cited:
            cited, mode = [hits[i] for i in gen.cited], "model"
        else:
            cited, mode = _attribute(gen.text, hits)
        missing = _unverified_numbers(gen.text, hits)
        return Answer(query, gen.text, cited, hits, self._llm.name, mode, grounded=not missing,
                      ungrounded_numbers=missing, **timing)

    # -- public API ------------------------------------------------------------------------
    def ask_many(self, queries: list[str], k: int = config.TOP_K) -> list[Answer]:
        # retrieve everything first so the embedding model can be released before a large LLM loads
        if not self._warm:  # first search pays one-off model/index load costs; keep that out of the timings
            self.retriever.search(queries[0], k=k)
            self._warm = True
        all_hits, retrieval_ms = [], []
        for q in queries:
            t0 = time.perf_counter()
            all_hits.append(self.retriever.search(q, k=k))
            retrieval_ms.append((time.perf_counter() - t0) * 1000)
        if self.backend != "extractive":
            if self.low_memory:
                self.retriever.embedder.unload()
            if self._llm is None:
                self._llm = get_llm(self.backend)
                if hasattr(self._llm, "warmup"):
                    self._llm.warmup()
        return [self._answer_one(q, h, ms) for q, h, ms in zip(queries, all_hits, retrieval_ms)]

    def ask(self, query: str, k: int = config.TOP_K) -> Answer:
        return self.ask_many([query], k=k)[0]


# -- presentation ---------------------------------------------------------------------------
def format_answer(a: Answer, show_retrieved: bool = True) -> str:
    lines = [f"Query   : {a.query}", f"Answer  : {a.answer}"]
    if a.cited:
        for i, h in enumerate(a.cited):
            lines.append(f"{'Source  : ' if i == 0 else '          '}{h.citation()}")
    else:
        lines.append("Source  : — (no supporting passage found)")
    notes = []
    if a.citation_mode in ("lexical", "top-1"):
        notes.append(f"citation inferred ({a.citation_mode}): the model gave no [n] marker")
    if not a.grounded:
        notes.append("WARNING: number(s) not found in retrieved context: " + ", ".join(a.ungrounded_numbers))
    if notes:
        lines.append("Note    : " + "; ".join(notes))
    timing = f"retrieval {a.retrieval_ms:.0f} ms"
    if a.ttft_ms is not None:
        timing += (f" + LLM first token {a.llm_ttft_ms:,.0f} ms = end-to-end TTFT {a.ttft_ms:,.0f} ms"
                   f" (LLM complete after {a.llm_total_ms:,.0f} ms)")
    lines.append(f"Latency : {timing}  [{a.backend}]")
    if show_retrieved:
        lines.append("Retrieved context (rank · page · chunk_id · score):")
        for rank, h in enumerate(a.retrieved, 1):
            mark = "*" if h in a.cited else " "
            lines.append(f"  {mark}{rank}. p{h.pages} · #{h.chunk_id} · {h.score:.2f} · {h.text[:90]}")
    return "\n".join(lines)
