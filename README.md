# Hindi RAG over *अग्नि की उड़ान — अध्ययन सहायिका*

A retrieval-augmented QA pipeline over the supplied 22-page Hindi PDF. It answers **Hindi and English**
questions from the document only, and every answer carries an automatic citation
(`page · section · chunk_id · score`) read from the vector-DB metadata.

**Pipeline:** PyMuPDF extraction (text + tables) → Devanagari normalisation → section- and danda-aware
chunking → `BAAI/bge-m3` embeddings → ChromaDB → top-4 retrieval (+ small-table expansion) → LLM answer
with `[n]` passage markers → markers mapped back to chunk metadata → citation.

## Results

| # | Query | System answer (Groq `qwen3.8-27b`) | Source (top citation) |
|---|---|---|---|
| 1 | SLV-III ने किस उपग्रह को कक्षा में स्थापित किया और किस वर्ष? | SLV-III ने 1980 में रोहिणी उपग्रह को कक्षा में स्थापित किया। | page: 8 · section: "इसरो के वर्ष और SLV-III" · chunk_id: 19 · score: 0.68 |
| 2 | कलाम को भारत रत्न किस वर्ष प्राप्त हुआ? | कलाम को भारत रत्न 1997 में प्राप्त हुआ। | page: 20 · section: "संस्थाओं एवं शब्दों की शब्दावली" · chunk_id: 79 · score: 0.72 |
| 3 | पोखरण-II में कलाम की क्या भूमिका थी? | कलाम ने उस समय रक्षा मंत्री के वैज्ञानिक सलाहकार तथा डीआरडीओ के प्रमुख के रूप में परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर एक केंद्रीय संगठनात्मक भूमिका निभाई। | page: 10 · section: "पोखरण-II: 1998 के परमाणु परीक्षण" · chunk_id: 27 · score: 0.64 |
| 4 | Which institution did Kalam attend to study aeronautical engineering? | Kalam attended the Madras Institute of Technology (MIT) in Chennai to study aeronautical engineering. | page: 6 · section: "कॉलेज के वर्ष और उड़ान का आकर्षण" · chunk_id: 12 · score: 0.57 |
| 5 | Who co-wrote the autobiography, and in what year was it published? | The autobiography was co-written by Arun Tiwari and published in 1999. | page: 3 · section: "ए.पी.जे. अब्दुल कलाम कौन थे?" · chunk_id: 4 · score: 0.53 |
| 6 | How and where did Kalam die in 2015? | Kalam died on July 27, 2015, in Shillong after collapsing while delivering a lecture to students at the Indian Institute of Management. | page: 15 · section: "अंतिम क्षण तक शिक्षक (2007–2015)" · chunk_id: 46 · score: 0.55 |

Full output (all citations, retrieved chunks, judge verdicts, timings): [`outputs/test_queries_log.md`](outputs/test_queries_log.md).
The same 6 queries answered by a small **local** model with no API key (5/6 correct): [`outputs/test_queries_log_local_cpu.md`](outputs/test_queries_log_local_cpu.md).

| Evaluation (20 hand-labelled questions: 8 Hindi, 12 English, + 3 out-of-scope) | Result |
|---|---|
| Retrieval: answer evidence in top-1 / top-3 / top-5 ([`retrieval_eval.md`](outputs/retrieval_eval.md)) | 95% / 95% / 100% (required 6: 100%) |
| Cross-lingual EN→HI retrieval: a correct page ranked first | 12/12 |
| Answer accuracy · citation on a correct page | 20/20 · 20/20 |
| Faithfulness: share of answer claims supported by the retrieved passages, judged by a *different* LLM (`gpt-oss-120b`) | 1.00 (target ≥ 0.85) — the judge does catch planted errors: [`judge_negative_controls.txt`](outputs/judge_negative_controls.txt) |
| Out-of-scope questions refused ("not in the document") | 3/3 |
| End-to-end time to first token, median (2-vCPU cloud VM, no GPU) | 1.07 s; 0.88 s with the int8 query encoder (target 420 ms — **not met**, see §4) |

## 1. Chunking strategy
- **Structure first.** A chunk never crosses a numbered section (`5 · …`) or sub-heading. Whole paragraphs are packed up to
  **200 tokens**, counted with bge-m3's own tokenizer: Devanagari is about 3.5 characters per token, so character counts mislead.
- **Why 200 / 40.** In this PDF the median paragraph is 21 tokens and the longest is 169; a section's narrative is about 270 tokens.
  At 200 tokens a chunk holds one idea, so citations point at the exact page and passage. The result is 95 chunks
  (mean 65 tokens, max 194). A paragraph longer than 200 tokens would be split **only at a danda (।), `?` or `!`**,
  carrying ≤ 40 tokens of whole sentences forward as overlap. No paragraph in this PDF needs that, so overlap is a safety
  net and never cuts a fact in half.
- **Tables.** Each row becomes a self-contained chunk (`वर्ष: 1997; सम्मान: भारत रत्न; …`), which makes lookups precise. When a
  row of a *small* table (≤ 8 rows) is retrieved, its sibling rows are added to the context with their own scores. That makes
  "list all IGMDP missiles" answerable. Without it, that question failed.
- **Metadata filtering.** The contents page and the end-of-guide question list are indexed but tagged
  `answerable=False` and filtered out at query time. They echo the questions almost word for word, so they would otherwise
  outrank the passages that actually contain the answer.
- The section title is prepended to the text that gets embedded, so a sentence like "उन्होंने इसे स्वीकार किया" still knows its topic.

## 2. Why ChromaDB (not Qdrant)
A ~100-chunk corpus does not need a server. Chroma runs in-process, persists to a folder, needs one `pip install` and no Docker,
and supports the metadata filters used here (`answerable`, `table_id`). Collections are named per embedding model, so vectors
from different models are never mixed. Qdrant would be the choice once the corpus needs a network service, payload indexes,
hybrid sparse+dense search or sharding.

## 3. Hindi text handling
- **Extraction.** PyMuPDF, chosen after comparing pdfplumber, pdfium and poppler: the others broke conjuncts, inserted
  stray spaces or duplicated matras. As a cross-check, PyMuPDF's characters were compared with poppler's on all 22 pages,
  ignoring whitespace: no differences remain after normalisation. Tables are found by their geometry (`find_tables`), and
  each cell's text is read by clipping to the cell.
- **Normalisation** (one function, applied to the document *and* every query): Unicode **NFC**; removal of zero-width and
  invisible characters; Devanagari digits converted to ASCII (`१९९७` = `1997`); collapse of matras the PDF layer emits twice
  (`अब्दुुल` → `अब्दुल`); one audited fix for a letter dropped in extraction (`पूर्वर्ती` → `पूर्ववर्ती`, found by the cross-check).
  Everything is UTF-8 end to end, including the console on Windows.
- **Segmentation** on danda `।`, double danda `॥`, `?` and `!`, with closing quotes kept on their sentence. A Latin `.` is
  *not* a sentence boundary: it would split `ए.पी.जे.` and `3.5`.
- **Embeddings: `BAAI/bge-m3`.** It is trained for multilingual and *cross-lingual* retrieval, so an English question lands next
  to the Hindi passage that answers it. English-only models place Devanagari almost at random. E5-family models would need
  `query:`/`passage:` prefixes, which the code adds automatically; bge-m3 needs none.

## 4. Generation, grounding, latency
The LLM sees only the numbered passages. It is told to answer in the question's language, use no outside knowledge, reply
`NOT_FOUND` when the answer is absent, and end with `[n]` markers. The markers are mapped back to the chunks' stored
metadata, so citations are produced by code, not written by the model. Any number in an answer that does not appear in the
retrieved text is flagged. Backends: Groq (`qwen3.8-27b`, reasoning off; chosen after comparing the Groq models on test
queries), Gemini, OpenAI, Anthropic, Ollama, a local Hugging Face model (no key), or `extractive` (no LLM at all).

**Latency, honestly.** Every backend streams, so time to first token (TTFT) is measured, not estimated. On this 2-vCPU VM:
- **Retrieval:** 395 ms median, almost all of it the bge-m3 query embedding (the Chroma search takes about 5 ms).
  `RAG_QUERY_INT8=1` cuts it to **100 ms**. Rank-1 evidence drops from 95% to 84%, but top-3 and top-5 are unchanged, and
  end-to-end answer accuracy stays at 20/20 ([log](outputs/test_queries_log_int8.md)).
- **Groq first token:** about 690 ms median. Even a 24-token prompt over a warm connection takes about 490 ms from this
  machine, so most of it is network distance and the provider's queue, not prompt size.
- **Reaching < 420 ms** needs an LLM endpoint close to the user, or self-hosted on GPU, plus the int8 or a GPU query encoder.
  The code side already uses a keep-alive connection that is warmed at start-up and streams the answer.
- The local CPU model (Qwen2.5-1.5B, no key) got 5/6 required queries right with every citation on a correct page
  (faithfulness 0.92). Its miss misspelled Shillong and invented an institute name, which the judge flagged. It took 100–260 s to
  the first token on 2 cores, so it suits offline use or a GPU ([log](outputs/test_queries_log_local_cpu.md)).

## 5. What I'd improve with more time
- **Hybrid retrieval and re-ranking.** Add BM25 over the normalised Hindi and a `bge-reranker-v2-m3` cross-encoder. Exact-match
  terms (`SLV-III`, years) would rank first more often, and the 0.43-vs-0.48 score gap between out-of-scope and real
  questions would widen enough for a reliable score cut-off. Today refusal is done by the LLM.
- **Bigger, independent evaluation set.** The 20 questions and their gold labels were written by the same person who built
  the system, and an LLM judge has its own biases. I would add questions from other people, romanised-Hindi queries
  ("kalam ka janm kab hua"), and human spot-checks of the judge.
- **Latency.** Move query encoding to ONNX or a GPU, and serve the LLM from a nearby region or self-hosted with vLLM.
- **Generality.** The extraction fix-up list is specific to this PDF. Any new PDF should first get the same
  two-extractor cross-check.

## 6. How to run
```bash
python -m venv .venv
.venv\Scripts\activate             # Windows   (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env             # optional: paste a free Groq key (console.groq.com) into .env  (macOS/Linux: cp)

python rag.py ingest               # PDF -> chunks -> embeddings -> ChromaDB (first run downloads bge-m3, ~2.3 GB)
python rag.py test                 # the 6 required queries -> outputs/test_queries_log.md (+ .json)
python rag.py test --extra         # + 14 extra and 3 out-of-scope queries, scored
python rag.py eval                 # retrieval evaluation (hit@k, MRR) -> outputs/retrieval_eval.md
python rag.py ask "कलाम का जन्म कहाँ हुआ?"     # any question, Hindi or English
python rag.py chat                 # interactive
python rag.py chunks               # inspect the 95 chunks and their metadata
python -m pytest                   # 15 unit tests (no model download needed)
```
With no API key, the local model is used automatically (~3 GB download; slow on CPU). Add `--llm extractive` to answer
without any LLM. All settings can be overridden by environment variables, listed in `.env.example` and `hindi_rag/config.py`.
No keys are stored in the repository.

```
rag.py                 CLI
hindi_rag/             pdf_extract · textutil · chunker · embedder · vectorstore · llm · pipeline · evaluate · config
eval/gold.json         hand-labelled questions: gold pages, evidence strings, answer keywords
outputs/               test logs (md + json), retrieval evaluation, judge negative controls
docs/DESIGN_NOTES.md   the measurements behind each decision
tests/                 unit tests
```
