#!/usr/bin/env python3
"""Command-line interface for the Hindi RAG pipeline.

    python rag.py ingest                 build the vector store from the PDF
    python rag.py chunks                 inspect the chunks that were created
    python rag.py ask "your question"    answer one question (Hindi or English) with citations
    python rag.py chat                   interactive question loop
    python rag.py test [--extra]         run the 6 required queries (+14 extra, +3 out-of-scope), score them,
                                         write outputs/test_queries_log.md and .json
    python rag.py eval                   retrieval evaluation (hit@k, MRR), write outputs/retrieval_eval.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path


def _utf8_console() -> None:
    # Windows consoles default to a legacy code page and would crash on Devanagari output.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def cmd_ingest(args) -> None:
    from hindi_rag import config
    from hindi_rag.vectorstore import ingest

    stats = ingest(Path(args.pdf) if args.pdf else config.PDF_PATH)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


def cmd_chunks(args) -> None:
    from hindi_rag import config
    from hindi_rag.chunker import build_chunks
    from hindi_rag.embedder import Embedder
    from hindi_rag.pdf_extract import extract_blocks

    chunks = build_chunks(extract_blocks(config.PDF_PATH), Embedder().count_tokens)
    for c in chunks:
        sub = f" > {c.subsection}" if c.subsection else ""
        body = c.text if args.full else c.text[:80]
        print(f"#{c.chunk_id:<3} p{c.page:<2} {c.kind:<13} {c.n_tokens:>3}t [{c.section}{sub}] {body}")
    print(f"\n{len(chunks)} chunks")


def cmd_ask(args) -> None:
    from hindi_rag.pipeline import RAGPipeline, format_answer

    print(format_answer(RAGPipeline(backend=args.llm).ask(args.question, k=args.k)))


def cmd_chat(args) -> None:
    from hindi_rag.pipeline import RAGPipeline, format_answer

    pipe = RAGPipeline(backend=args.llm)
    print("Ask in Hindi or English. Type 'exit' to quit.")
    while True:
        try:
            q = input("\n? ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in ("exit", "quit", "q"):
            break
        if q:
            print(format_answer(pipe.ask(q, k=args.k)))


def _make_judge(mode: str):
    """LLM-as-judge for faithfulness. Deliberately a *different* model from the answer generator."""
    if mode == "off":
        return None
    from hindi_rag.llm import OpenAICompatChat

    if os.getenv("GROQ_API_KEY"):
        return OpenAICompatChat("groq", model=os.getenv("RAG_JUDGE_MODEL", "openai/gpt-oss-120b"))
    if os.getenv("OPENAI_API_KEY"):
        return OpenAICompatChat("openai", model=os.getenv("RAG_JUDGE_MODEL", "gpt-4o"))
    print("(no GROQ_API_KEY / OPENAI_API_KEY: faithfulness judge skipped)")
    return None


def _ms(v: float | None) -> str:
    return "n/a" if v is None else f"{v:,.0f}"


def _median(values: list[float]) -> float | None:
    from statistics import median

    return median(values) if values else None


def cmd_test(args) -> None:
    from statistics import mean

    from hindi_rag import config
    from hindi_rag.evaluate import citation_ok, judge_faithfulness, keywords_ok
    from hindi_rag.pipeline import RAGPipeline, format_answer

    gold = json.loads(config.GOLD_PATH.read_text(encoding="utf-8"))
    items = gold["required"] + (gold["extra"] + gold["unanswerable"] if args.extra else [])
    pipe = RAGPipeline(backend=args.llm)
    answers = pipe.ask_many([i["query"] for i in items], k=args.k)
    judge = _make_judge(args.judge)

    records = []
    for item, a in zip(items, answers):
        answerable = "answer_keywords" in item
        rec = {
            "id": item["id"], "lang": item["lang"], "query": item["query"], "answer": a.answer,
            "abstained": a.abstained, "answerable": answerable,
            "citations": [h.citation() for h in a.cited], "cited_chunk_ids": [h.chunk_id for h in a.cited],
            "citation_mode": a.citation_mode, "numbers_grounded": a.grounded,
            "retrieval_ms": round(a.retrieval_ms, 1), "llm_ttft_ms": a.llm_ttft_ms and round(a.llm_ttft_ms, 1),
            "ttft_ms": a.ttft_ms and round(a.ttft_ms, 1), "llm_total_ms": a.llm_total_ms and round(a.llm_total_ms, 1),
            "reference": item.get("expected_answer", "out of scope: should abstain"),
        }
        if answerable:
            rec["correct"] = not a.abstained and keywords_ok(a.answer, item["answer_keywords"])
            rec["citation_correct"] = citation_ok(a.cited, item["gold_pages"])
        else:
            rec["correct"] = a.abstained       # the right behaviour for an out-of-scope question is to refuse
            rec["citation_correct"] = None
        rec["faithfulness"], rec["claims"] = (judge_faithfulness(judge, a.query, a.retrieved, a.answer)
                                              if judge and not a.abstained else (None, []))
        records.append(rec)
        print(format_answer(a, show_retrieved=False), "\n")

    ans = [r for r in records if r["answerable"]]
    oos = [r for r in records if not r["answerable"]]
    faith = [r["faithfulness"] for r in records if r["faithfulness"] is not None]
    ret = [r["retrieval_ms"] for r in records]
    llm_ttft = [r["llm_ttft_ms"] for r in records if r["llm_ttft_ms"] is not None]
    e2e = [r["ttft_ms"] for r in records if r["ttft_ms"] is not None]
    pct = lambda xs: f"{sum(xs)}/{len(xs)} ({sum(xs) / len(xs):.0%})" if xs else "—"

    summary = {
        "answer_accuracy": pct([r["correct"] for r in ans]),
        "citation_accuracy": pct([r["citation_correct"] for r in ans]),
        "out_of_scope_abstention": pct([r["correct"] for r in oos]),
        "numbers_grounded": pct([r["numbers_grounded"] for r in records if not r["abstained"]]),
        "faithfulness_mean": round(mean(faith), 3) if faith else None,
        "retrieval_ms_median": _median(ret), "llm_ttft_ms_median": _median(llm_ttft),
        "e2e_ttft_ms_median": _median(e2e), "e2e_ttft_ms_max": max(e2e) if e2e else None,
    }

    lines = [
        "# Test query log", "",
        f"- Generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- Document: `{config.PDF_PATH.name}` · chunks indexed: {pipe.retriever.collection.count()}",
        f"- Retrieval: `{config.EMBED_MODEL}` embeddings · ChromaDB (cosine) · top-k = {args.k}",
        f"- Answer generator: `{next((r for r in answers if not r.abstained), answers[0]).backend}`",
        f"- Faithfulness judge: `{judge.name if judge else 'not run'}` (a different model from the generator)",
        "- Every answer and citation below was produced by the pipeline. page / section / chunk_id come from the "
        "metadata stored in ChromaDB. The *Reference* column is hand-written ground truth used only for scoring.", "",
        "## Scorecard", "",
        "| Metric | Result | Target / note |", "|---|---|---|",
        f"| Answer accuracy (gold keywords present) | {summary['answer_accuracy']} | |",
        f"| Citation accuracy (a cited chunk is on a gold page) | {summary['citation_accuracy']} | |",
        f"| Faithfulness (claims supported by retrieved passages, LLM judge) | "
        f"{summary['faithfulness_mean'] if faith else 'not run'} | ≥ 0.85 |",
        f"| Numbers in answer found in retrieved context | {summary['numbers_grounded']} | automatic check |",
    ]
    if oos:
        lines.append(f"| Out-of-scope questions correctly refused | {summary['out_of_scope_abstention']} | |")
    lines += [
        f"| Retrieval latency, median (query embedding + vector search) | {_ms(summary['retrieval_ms_median'])} ms | |",
        f"| LLM time to first token, median | {_ms(summary['llm_ttft_ms_median'])} ms | |",
        f"| **End-to-end TTFT, median / max** | **{_ms(summary['e2e_ttft_ms_median'])} / {_ms(summary['e2e_ttft_ms_max'])} ms** "
        "| < 420 ms (see README §4) |",
        "", "## Answers", "",
        "| # | Lang | Query | System answer | Source (citation) | Reference | ✓ | Faithf. | TTFT ms |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in records:
        mark = "✅" if r["correct"] else "❌"
        f = "—" if r["faithfulness"] is None else f"{r['faithfulness']:.2f}"
        lines.append(f"| {r['id']} | {r['lang']} | {r['query']} | {r['answer'].replace('|', '/')} | "
                     f"{'<br>'.join(r['citations']) or '—'} | {r['reference']} | {mark} | {f} | {_ms(r['ttft_ms'])} |")
    lines += ["", "## Full output per query", ""]
    for r, a in zip(records, answers):
        lines += [f"### {r['id']}. ({r['lang']})", "", "```text", format_answer(a)]
        for c in r["claims"]:
            lines.append(f"  judge: {'supported  ' if c.get('supported') else 'UNSUPPORTED'} · {c.get('claim', '')}")
        lines += ["```", ""]

    config.OUTPUT_DIR.mkdir(exist_ok=True)
    md, js = config.OUTPUT_DIR / f"{args.out}.md", config.OUTPUT_DIR / f"{args.out}.json"
    md.write_text("\n".join(lines), encoding="utf-8")
    js.write_text(json.dumps({"summary": summary, "results": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Log written to {md} and {js}")


def cmd_eval(args) -> None:
    from hindi_rag import config
    from hindi_rag.evaluate import run, to_markdown
    from hindi_rag.vectorstore import Retriever

    retriever = Retriever()
    result = run(retriever)
    label = config.EMBED_MODEL + (" (query encoder: int8)" if retriever.embedder.int8 else " (float32)")
    report = to_markdown(result, label, retriever.collection.count())
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    out = config.OUTPUT_DIR / ("retrieval_eval_int8.md" if retriever.embedder.int8 else "retrieval_eval.md")
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nReport written to {out}")


def main() -> None:
    _utf8_console()
    parser = argparse.ArgumentParser(description="Hindi RAG over the 'Agni Ki Udaan' study guide")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("ingest", help="extract, chunk, embed and store the PDF")
    p.add_argument("--pdf", help="path to the PDF (default: data/Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf)")
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("chunks", help="print the chunks")
    p.add_argument("--full", action="store_true", help="print full chunk text")
    p.set_defaults(func=cmd_chunks)

    for name, fn, helptext in (("ask", cmd_ask, "answer one question"), ("chat", cmd_chat, "interactive mode"),
                               ("test", cmd_test, "run and score the test queries")):
        p = sub.add_parser(name, help=helptext)
        if name == "ask":
            p.add_argument("question")
        if name == "test":
            p.add_argument("--extra", action="store_true", help="add 14 extra queries and 3 out-of-scope queries")
            p.add_argument("--judge", choices=("auto", "off"), default="auto", help="LLM faithfulness judge")
            p.add_argument("--out", default="test_queries_log", help="output file name in outputs/ (no extension)")
        p.add_argument("--k", type=int, default=None, help="chunks to retrieve (default: RAG_TOP_K or 4)")
        p.add_argument("--llm", default=None,
                       help="hf | groq | gemini | openai | ollama | anthropic | extractive (default: RAG_LLM or hf)")
        p.set_defaults(func=fn)

    p = sub.add_parser("eval", help="retrieval evaluation (hit@k, MRR)")
    p.set_defaults(func=cmd_eval)

    args = parser.parse_args()
    if getattr(args, "k", "x") is None:
        from hindi_rag import config
        args.k = config.TOP_K
    args.func(args)


if __name__ == "__main__":
    main()
