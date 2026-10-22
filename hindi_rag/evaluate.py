"""Retrieval evaluation: is the evidence in the top-k chunks, for Hindi *and* English queries?

Two notions of "correct" are scored for every query in eval/gold.json:
  * page hit      -- a top-k chunk comes from a page that holds the answer (citation correctness)
  * evidence hit  -- a top-k chunk's text contains the answer facts (what the LLM needs to see)
It also reports top-1 scores of unanswerable queries, which is how MIN_SCORE was calibrated.
"""
from __future__ import annotations

import json
import re
from statistics import mean

from . import config
from .textutil import strip_all_space
from .vectorstore import Hit, Retriever

KS = (1, 3, 5)


def _page_ok(hit: Hit, pages: list[int]) -> bool:
    return any(p in pages for p in range(hit.page, hit.page_end + 1))


def _evidence_ok(hit: Hit, evidence: list[str]) -> bool:
    text = strip_all_space(hit.text)
    return bool(evidence) and all(strip_all_space(e) in text for e in evidence)


def _first_rank(hits: list[Hit], pred) -> int | None:
    return next((i for i, h in enumerate(hits, 1) if pred(h)), None)


def run(retriever: Retriever, include_extra: bool = True) -> dict:
    gold = json.loads(config.GOLD_PATH.read_text(encoding="utf-8"))
    items = gold["required"] + (gold["extra"] if include_extra else [])
    rows = []
    for item in items:
        hits = retriever.search(item["query"], k=max(KS), expand_tables=False)  # pure ranking quality
        rows.append({
            **item,
            "page_rank": _first_rank(hits, lambda h: _page_ok(h, item["gold_pages"])),
            "evidence_rank": _first_rank(hits, lambda h: _evidence_ok(h, item["evidence"])) if item["evidence"] else None,
            "top1": hits[0],
        })
    unanswerable = [{**u, "top1": retriever.search(u["query"], k=1, expand_tables=False)[0]}
                    for u in gold.get("unanswerable", [])]
    return {"rows": rows, "unanswerable": unanswerable}


# ---- answer-level evaluation ----------------------------------------------------------------
def keywords_ok(answer: str, groups: list[list[str]]) -> bool:
    """Correct when every keyword group has at least one alternative in the answer."""
    a = strip_all_space(answer).lower()
    return all(any(strip_all_space(alt).lower() in a for alt in group) for group in groups)


def citation_ok(cited: list[Hit], gold_pages: list[int]) -> bool:
    return any(_page_ok(h, gold_pages) for h in cited)


JUDGE_SYSTEM = (
    "You are a strict fact-checker for a retrieval-augmented question-answering system. You get numbered "
    "context passages (in Hindi), a question and an answer (Hindi or English). Split the answer into its atomic "
    "factual claims. For each claim decide whether it is directly supported by the passages. Translation between "
    "Hindi and English counts as supported; anything that needs outside knowledge does not.\n"
    'Reply with JSON only: {"claims": [{"claim": "...", "supported": true}]}'
)


def judge_faithfulness(judge, query: str, hits: list[Hit], answer: str) -> tuple[float | None, list[dict]]:
    """Fraction of the answer's claims supported by the retrieved passages (RAGAS-style faithfulness)."""
    context = "\n\n".join(f"[{i}] (page {h.pages})\n{h.text}" for i, h in enumerate(hits, 1))
    user = f"Context passages:\n{context}\n\nQuestion: {query}\nAnswer to check: {answer}\n\nReturn the JSON now."
    raw = judge.complete(JUDGE_SYSTEM, user, max_tokens=1500).text
    match = re.search(r"\{.*\}", raw, re.S)
    try:
        claims = json.loads(match.group(0))["claims"] if match else []
    except (json.JSONDecodeError, KeyError, TypeError):
        claims = []
    if not claims:
        return None, []
    return sum(bool(c.get("supported")) for c in claims) / len(claims), claims


def _rate(ranks: list[int | None], k: int) -> str:
    return f"{sum(r is not None and r <= k for r in ranks) / len(ranks):.0%}" if ranks else "—"


def _mrr(ranks: list[int | None]) -> str:
    return f"{mean(1 / r if r else 0 for r in ranks):.2f}" if ranks else "—"


def to_markdown(result: dict, embed_model: str, n_chunks: int) -> str:
    rows = result["rows"]
    out = [
        "# Retrieval evaluation", "",
        f"Embedding model: `{embed_model}` · indexed chunks: {n_chunks} · filter: `answerable=True` · "
        f"queries: {len(rows)} ({sum(r['lang'] == 'hi' for r in rows)} Hindi, {sum(r['lang'] == 'en' for r in rows)} English)", "",
        "**Evidence hit@k** = a top-k chunk contains the answer facts. **Page hit@k** = a top-k chunk is from a page holding the answer.", "",
        "| Query set | n | Evidence hit@1 | @3 | @5 | MRR | Page hit@1 | @3 | @5 |", "|---|---|---|---|---|---|---|---|---|",
    ]
    groups = {
        "Required 6 (all)": [r for r in rows if r["id"] <= 6],
        "All queries": rows,
        "Hindi queries": [r for r in rows if r["lang"] == "hi"],
        "English queries (cross-lingual EN→HI)": [r for r in rows if r["lang"] == "en"],
    }
    for name, grp in groups.items():
        ev = [r["evidence_rank"] for r in grp if r["evidence"]]
        pg = [r["page_rank"] for r in grp]
        out.append(f"| {name} | {len(grp)} | {_rate(ev, 1)} | {_rate(ev, 3)} | {_rate(ev, 5)} | {_mrr(ev)} | "
                   f"{_rate(pg, 1)} | {_rate(pg, 3)} | {_rate(pg, 5)} |")

    out += ["", "## Per query", "", "| # | Lang | Query | Evidence rank | Page rank | Top-1 (page · chunk · score) |", "|---|---|---|---|---|---|"]
    for r in rows:
        h = r["top1"]
        out.append(f"| {r['id']} | {r['lang']} | {r['query']} | {r['evidence_rank'] or ('miss' if r['evidence'] else '—')} | "
                   f"{r['page_rank'] or 'miss'} | p{h.pages} · #{h.chunk_id} · {h.score:.2f} |")

    ans_scores = [r["top1"].score for r in rows]
    out += ["", "## Calibrating the 'not found' threshold", "",
            f"Top-1 score of the {len(ans_scores)} answerable queries: min {min(ans_scores):.2f}, mean {mean(ans_scores):.2f}.", "",
            "| Unanswerable query | Top-1 score | Top-1 chunk |", "|---|---|---|"]
    for u in result["unanswerable"]:
        out.append(f"| {u['query']} | {u['top1'].score:.2f} | p{u['top1'].pages} · #{u['top1'].chunk_id} |")
    out += ["", f"Configured `MIN_SCORE` = {config.MIN_SCORE}. Scores are only a coarse first filter: the LLM is additionally "
            "instructed to answer `NOT_FOUND` when the retrieved passages do not contain the answer.", ""]
    return "\n".join(out)
