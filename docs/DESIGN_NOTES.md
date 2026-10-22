# Design notes — the measurements behind each decision

All numbers were measured on the machine that produced `outputs/`: a 2-vCPU cloud VM, 8 GB RAM, about 6 GB usable per
process, no GPU.

## 1. PDF extraction
| Extractor | Result on this PDF |
|---|---|
| **PyMuPDF** (chosen) | Clean conjuncts; tables detected by geometry. One letter family dropped (`पूर्ववर्ती`) and some doubled matras, both fixed in `normalize()` |
| pdfplumber / pdfium | Broken conjuncts and stray spaces inside words |
| poppler `pdftotext` | Stray spaces and layout artefacts; used only as the independent cross-check |

Cross-check: after `normalize()`, PyMuPDF's text and poppler's text, with whitespace removed, are identical on all 22 pages.
Output: 146 blocks (140 paragraphs, 6 tables). Paragraph reconstruction: a line ending in a hyphen is joined to the next,
and a new paragraph starts at a vertical gap larger than 0.6 × the line height or after a short line. Table cells are read
by clipping to each cell's rectangle with the same text extraction as paragraphs, so tables and prose go through identical
Devanagari handling.

## 2. Chunking statistics
| | |
|---|---|
| Sentences / mean length | 219 / 25 tokens (bge-m3 tokenizer) |
| Paragraph length | median 21, max 169 tokens |
| Chunks | 95 = 42 text + 49 table rows + 2 contents page + 2 question list |
| Chunk length | mean 65, max 194 tokens (ceiling 200) |
| Tables (rows) | missiles p9 (5) · mentors p12 (5) · awards p16 (5) · timeline p17 (13) · glossary p20 (9) · quick facts p22 (12) |

Small-table expansion uses the first three tables (≤ 8 rows each). The timeline, glossary and quick-facts tables are lookup
tables, so their rows stay individually addressable. Expanding them would add 9–13 rows of noise to most prompts.

## 3. Choosing the LLM
**Local models** (no key; same 4-passage prompt; Qwen2.5's tokenizer turns it into about 1,600 tokens because Hindi tokenises poorly):

| Model | Result |
|---|---|
| Qwen2.5-1.5B, bfloat16 | Correct, cites `[1][4]`; **TTFT 100 s** (this CPU has no bf16 instructions) |
| Qwen2.5-1.5B, float32 | Killed for exceeding the ~6 GB memory limit |
| Qwen2.5-1.5B, int8 (dynamic) | Garbage output: Qwen's outlier activations do not survive per-tensor int8 |
| Qwen2.5-0.5B, float32 | TTFT 12 s, but **wrong**: named Kalam as the co-author instead of Arun Tiwari, and gave no citation |

The local backend therefore defaults to 1.5B, bfloat16 on machines under 15 GB RAM and float32 above that, float16 on a GPU.

**Groq models** (two test queries each, warm connection):

| Model | TTFT | Issue |
|---|---|---|
| **`qwen/qwen3.8-27b`, `reasoning_effort=none`** (chosen) | 705–820 ms | none: right language, clean `[n]` citations |
| `openai/gpt-oss-120b`, low reasoning | 760–920 ms | used `【1】` instead of `[1]` |
| `openai/gpt-oss-20b`, low reasoning | 905–915 ms | answered an English question in Hindi |

## 4. Latency decomposition (Groq backend)
| Component | Measured |
|---|---|
| bge-m3 query embedding, float32 / int8 | 356–361 ms / 92 ms |
| ChromaDB search (95 vectors, filter) | about 5 ms |
| New TLS connection to Groq | 86–377 ms, avoided with a keep-alive session warmed at start-up |
| Groq first token, 24-token prompt, warm connection | about 490 ms median, the floor from this machine |
| Groq first token, real 4-passage prompt (925 tokens) | about 665–690 ms median |

The 420 ms TTFT target is therefore not reachable from this machine with a hosted LLM, whatever the code does. The
retrieval part (100 ms with int8) fits comfortably; the remaining cost is the LLM's location.

**int8 query encoder trade-off** (passages are always stored in float32):

| | float32 | int8 |
|---|---|---|
| Evidence hit@1 / @3 / @5 | 95% / 95% / 100% | 84% / 95% / 100% |
| End-to-end answer accuracy (20 questions) | 20/20 | 20/20 |
| Retrieval median | 395 ms | 100 ms |

float32 stays the default because it ranks the evidence first more often. int8 is a one-variable switch
(`RAG_QUERY_INT8=1`) for latency-sensitive deployments.

## 5. Evaluation method
- `eval/gold.json`: 20 questions (the 6 required + 14 more, 8 Hindi and 12 English) plus 3 out-of-scope, each labelled with
  the pages holding the answer, evidence strings and answer keywords in both scripts.
- **Retrieval** (`rag.py eval`): *evidence hit@k* means a top-k chunk contains all the evidence strings; *page hit@k* means a
  top-k chunk is on a gold page. Table expansion is off here, so this measures ranking only.
- **Answers** (`rag.py test --extra`): accuracy means every keyword group appears in the answer; citation accuracy means a
  cited chunk is on a gold page.
- **Faithfulness** follows the RAGAS idea: a judge LLM splits the answer into atomic claims and checks each against the
  retrieved passages; the score is the fraction supported. The judge (`gpt-oss-120b`) is a different model from the
  generator, so the system is not grading itself. **Negative controls**
  ([`outputs/judge_negative_controls.txt`](../outputs/judge_negative_controls.txt)): planted wrong or partly made-up answers
  score 0.00, 0.75 and 0.50, and every planted falsehood is flagged.
- **Refusal threshold.** Top-1 similarity of the answerable questions is at least 0.48; for the out-of-scope ones it is
  0.37–0.43. That gap is too small for a safe score cut-off, so `MIN_SCORE = 0.30` only catches clearly irrelevant
  questions, and refusal relies on the LLM's `NOT_FOUND` instruction (3/3 refused).
