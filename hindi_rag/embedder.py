"""Thin wrapper around a multilingual sentence-embedding model (default: BAAI/bge-m3).

Why bge-m3: it is trained for *cross-lingual* retrieval, so an English query and a Hindi passage
that mean the same thing land close together in the vector space -- exactly what queries 4-6 need.
English-only models (e.g. all-MiniLM) place Devanagari text almost arbitrarily.
"""
from __future__ import annotations

import gc

import numpy as np

from . import config


def _prefixes(model_name: str) -> tuple[str, str]:
    """E5-family models were trained with explicit "query: " / "passage: " prefixes; BGE-M3 needs none."""
    return ("query: ", "passage: ") if "e5" in model_name.lower() else ("", "")


class Embedder:
    def __init__(self, model_name: str = config.EMBED_MODEL, int8: bool = False):
        self.model_name = model_name
        self.query_prefix, self.passage_prefix = _prefixes(model_name)
        self.int8 = int8
        self._model = None

    @property
    def model(self):
        """Loaded lazily, and reloadable after unload() so a big LLM can use the RAM in between."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            self._model.max_seq_length = 512  # our chunks are <= ~200 tokens; skip the 8k-token default
            if self.int8:
                self._quantize()
        return self._model

    def _quantize(self) -> None:
        """int8 dynamic quantisation of the Linear layers: ~4x faster query encoding on CPU.
        Only used at query time; the stored passage vectors are always computed in full precision."""
        import warnings

        import torch
        from torch import nn

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                torch.ao.quantization.quantize_dynamic(self._model, {nn.Linear}, dtype=torch.qint8, inplace=True)
        except Exception as exc:  # API missing in a future torch: fall back to full precision
            warnings.warn(f"int8 quantisation unavailable ({exc}); using float32 query encoder")
            self.int8 = False

    def unload(self) -> None:
        self._model = None
        gc.collect()

    def count_tokens(self, text: str) -> int:
        return len(self.model.tokenizer(text, add_special_tokens=False)["input_ids"])

    def _encode(self, texts: list[str], prefix: str, progress: bool = False) -> np.ndarray:
        vectors = self.model.encode(
            [prefix + t for t in texts], batch_size=16, normalize_embeddings=True,
            show_progress_bar=progress, convert_to_numpy=True,
        )
        return np.asarray(vectors, dtype="float32")

    def embed_passages(self, texts: list[str], progress: bool = False) -> np.ndarray:
        return self._encode(texts, self.passage_prefix, progress)

    def embed_queries(self, texts: list[str]) -> np.ndarray:
        return self._encode(texts, self.query_prefix)
