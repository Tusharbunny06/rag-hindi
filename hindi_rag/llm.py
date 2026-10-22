"""Answer generation. The model only ever sees the retrieved passages and is told to cite them.

Backends (pick with RAG_LLM):
  hf          local Hugging Face model, no API key (default: Qwen2.5-1.5B-Instruct)
  anthropic   Claude via the Anthropic API                        needs ANTHROPIC_API_KEY
  openai      any OpenAI-compatible endpoint                       needs OPENAI_API_KEY (+ OPENAI_BASE_URL)
  groq        preset of `openai` for api.groq.com                  needs GROQ_API_KEY
  gemini      preset of `openai` for Google's OpenAI-compatible API needs GEMINI_API_KEY
  ollama      preset of `openai` for a local Ollama server          no key
  extractive  no LLM: returns the best-matching sentence from the context (offline fallback)

Every backend *streams*, so time-to-first-token (TTFT) is measured, not estimated.
"""
from __future__ import annotations

import json
import os
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

from . import config
from .vectorstore import Hit

NOT_FOUND = "NOT_FOUND"

SYSTEM_PROMPT = (
    "You are a precise question-answering assistant for a Hindi reference document about "
    "A.P.J. Abdul Kalam. Answer ONLY from the numbered context passages. The passages are in Hindi; "
    "the question may be in Hindi or English.\n"
    "Rules:\n"
    "1. Reply in the same language as the question (Hindi question -> Hindi answer, English -> English).\n"
    "2. Be brief: one or two sentences stating exactly the fact asked for (a name, year, place, role).\n"
    "3. Use no outside knowledge. If the passages do not contain the answer, reply exactly: " + NOT_FOUND + "\n"
    "4. End the answer with the numbers of the passages you used, like [2] or [1][3]."
)

# OpenAI-compatible presets. Model names change over time; override with RAG_LLM_MODEL.
# Groq default: qwen3.8-27b with reasoning switched off. Measured on the 6 test queries it answers in the
# question's language with clean [n] citations; gpt-oss-20b answered an English question in Hindi and
# gpt-oss-120b used 【n】 markers, and both spend time on hidden reasoning before the first answer token.
OPENAI_PRESETS = {
    "openai": {"base": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"), "key_env": "OPENAI_API_KEY",
               "model": "gpt-4o-mini", "extra": {}},
    "groq": {"base": "https://api.groq.com/openai/v1", "key_env": "GROQ_API_KEY",
             "model": "qwen/qwen3.8-27b", "extra": {"reasoning_effort": "none"}},
    "gemini": {"base": "https://generativelanguage.googleapis.com/v1beta/openai", "key_env": "GEMINI_API_KEY",
               "model": "gemini-2.5-flash", "extra": {}},
    "ollama": {"base": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"), "key_env": "OLLAMA_API_KEY",
               "model": "qwen2.5:7b", "extra": {}},
}


def has_devanagari(text: str) -> bool:
    return bool(re.search(r"[ऀ-ॿ]", text))


def not_found_message(question: str) -> str:
    return ("दस्तावेज़ में इस प्रश्न का उत्तर उपलब्ध नहीं है।" if has_devanagari(question)
            else "The document does not contain an answer to this question.")


def build_user_prompt(question: str, hits: list[Hit]) -> str:
    context = "\n\n".join(f"[{i}] (page {h.pages}, {h.section})\n{h.text}" for i, h in enumerate(hits, 1))
    return f"Context passages:\n{context}\n\nQuestion: {question}\nAnswer:"


@dataclass
class Generation:
    text: str
    cited: list[int]       # 0-based indices into the hit list, as stated by the model
    not_found: bool


def parse_generation(raw: str, n_hits: int) -> Generation:
    raw = raw.strip()
    if raw.upper().strip(" .[]") == NOT_FOUND or raw.upper().startswith(NOT_FOUND):
        return Generation("", [], True)
    cited = []
    for m in re.finditer(r"\[(\d+)\]", raw):
        idx = int(m.group(1)) - 1
        if 0 <= idx < n_hits and idx not in cited:
            cited.append(idx)
    text = re.sub(r"\s*\[\d+\]", "", raw).strip()
    return Generation(text, cited, False)


@dataclass
class Completion:
    text: str
    ttft_ms: float | None   # time from request to first streamed text
    total_ms: float


class _Timer:
    """Collects streamed pieces and records when the first non-empty one arrived."""

    def __init__(self):
        self.t0 = time.perf_counter()
        self.ttft_ms: float | None = None
        self.parts: list[str] = []

    def add(self, piece: str) -> None:
        if piece and self.ttft_ms is None:
            self.ttft_ms = (time.perf_counter() - self.t0) * 1000
        self.parts.append(piece)

    def done(self) -> Completion:
        return Completion("".join(self.parts), self.ttft_ms, (time.perf_counter() - self.t0) * 1000)


class ChatLLM(ABC):
    name: str

    @abstractmethod
    def complete(self, system: str, user: str) -> Completion: ...


def _total_ram_gb() -> float:
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1e9
    except (AttributeError, ValueError, OSError):  # e.g. Windows
        return 0.0


class HFChat(ChatLLM):
    def __init__(self, model_name: str = config.HF_LLM_MODEL):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if torch.cuda.is_available():
            self.device, default_dtype = "cuda", "float16"
        elif torch.backends.mps.is_available():
            self.device, default_dtype = "mps", "float16"
        else:
            # float32 is fastest on most CPUs but needs ~4 bytes/parameter (≈6.5 GB for 1.5B);
            # bfloat16 halves the RAM and is the safe choice on 8 GB machines.
            self.device, default_dtype = "cpu", ("float32" if _total_ram_gb() >= 15 else "bfloat16")
        dtype_name = os.getenv("RAG_HF_DTYPE", default_dtype)
        self.name = f"hf:{model_name} ({self.device}, {dtype_name})"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        kwargs = {"low_cpu_mem_usage": True}
        try:
            self.model = AutoModelForCausalLM.from_pretrained(model_name, dtype=getattr(torch, dtype_name), **kwargs)
        except TypeError:  # older transformers used the torch_dtype keyword
            self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=getattr(torch, dtype_name), **kwargs)
        self.model.to(self.device).eval()

    def complete(self, system: str, user: str) -> Completion:
        from threading import Thread

        from transformers import TextIteratorStreamer

        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        timer = _Timer()
        # greedy decoding: deterministic, reproducible answers
        worker = Thread(target=self.model.generate, kwargs={**inputs, "streamer": streamer, "do_sample": False,
                                                            "max_new_tokens": config.MAX_NEW_TOKENS})
        worker.start()
        for piece in streamer:
            timer.add(piece)
        worker.join()
        return timer.done()


class AnthropicChat(ChatLLM):
    def __init__(self, model: str = ""):
        import anthropic

        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
        self.model = model or "claude-haiku-5-5"
        self.name = f"anthropic:{self.model}"

    def complete(self, system: str, user: str) -> Completion:
        timer = _Timer()
        with self.client.messages.stream(
            model=self.model, max_tokens=config.MAX_NEW_TOKENS, temperature=0, system=system,
            messages=[{"role": "user", "content": user}],
        ) as stream:
            for text in stream.text_stream:
                timer.add(text)
        return timer.done()


class OpenAICompatChat(ChatLLM):
    def __init__(self, preset: str = "openai", model: str = ""):
        import requests

        p = OPENAI_PRESETS[preset]
        self.base = p["base"].rstrip("/")
        self.key = os.getenv(p["key_env"]) or os.getenv("OPENAI_API_KEY") or "not-needed"  # Ollama ignores the key
        self.model = model or p["model"]
        self.extra = p["extra"] if not model or model == p["model"] else {}
        self.name = f"{preset}:{self.model}"
        # one keep-alive HTTPS connection for all questions: a new TLS handshake costs ~100-400 ms per request
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {self.key}"

    def warmup(self) -> None:
        """Open the connection before the first real question (called once at start-up)."""
        try:
            self.session.get(f"{self.base}/models", timeout=10)
        except Exception:  # warm-up is best-effort; the real request will surface any error
            pass

    def complete(self, system: str, user: str, max_tokens: int | None = None) -> Completion:
        timer = _Timer()
        for attempt in range(6):
            resp = self.session.post(
                f"{self.base}/chat/completions", timeout=120, stream=True,
                json={"model": self.model, "temperature": 0, "max_tokens": max_tokens or config.MAX_NEW_TOKENS,
                      "stream": True, **self.extra,
                      "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
            )
            if resp.status_code != 429 or attempt == 5:
                break
            # free-tier rate limit: wait as instructed, then retry (the wait is not counted in TTFT)
            wait = float(resp.headers.get("retry-after") or 2 ** attempt)
            resp.close()
            time.sleep(min(wait, 60))
            timer = _Timer()
        with resp:
            if resp.status_code >= 400:
                raise RuntimeError(f"{self.name}: HTTP {resp.status_code}: {resp.text[:300]}")
            resp.encoding = "utf-8"
            for line in resp.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                choices = json.loads(data).get("choices") or []
                if choices:
                    timer.add((choices[0].get("delta") or {}).get("content") or "")
        return timer.done()


def get_llm(backend: str | None = None) -> ChatLLM | None:
    """Return a chat backend, or None for the extractive (no-LLM) mode."""
    backend = (backend or config.LLM_BACKEND).lower()
    if backend == "extractive":
        return None
    if backend == "hf":
        return HFChat()
    if backend == "anthropic":
        return AnthropicChat(config.LLM_MODEL)
    if backend in OPENAI_PRESETS:
        return OpenAICompatChat(backend, config.LLM_MODEL)
    raise ValueError(f"Unknown RAG_LLM backend: {backend!r} "
                     f"(use hf | anthropic | {' | '.join(OPENAI_PRESETS)} | extractive)")
