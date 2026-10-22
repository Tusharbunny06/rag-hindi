"""ChromaDB persistence, ingestion and retrieval.

Why ChromaDB (over Qdrant): this is a ~100-chunk local corpus. Chroma runs in-process with a
single `pip install`, persists to a folder, and supports the metadata filtering we need
(`answerable=True`) -- no server or Docker needed, which keeps "clone and run" friction at zero.
Qdrant would be the pick once the corpus needs a network service, payload indexes or sharding.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import chromadb

from . import config
from .chunker import build_chunks
from .embedder import Embedder
from .pdf_extract import extract_blocks
from .textutil import normalize


@dataclass
class Hit:
    chunk_id: int
    page: int
    page_end: int
    section: str
    subsection: str
    kind: str
    text: str
    score: float            # cosine similarity, 1.0 = identical direction
    table_id: int = -1
    table_rows: int = 0

    @property
    def pages(self) -> str:
        return str(self.page) if self.page == self.page_end else f"{self.page}-{self.page_end}"

    def citation(self) -> str:
        return f'page: {self.pages} · section: "{self.section}" · chunk_id: {self.chunk_id} · score: {self.score:.2f}'


def open_collection(reset: bool = False):
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    name = config.collection_name()
    if reset:
        try:
            client.delete_collection(name)
        except Exception:  # collection did not exist yet
            pass
    # cosine space: embeddings are L2-normalised, so distance = 1 - cosine similarity
    return client.get_or_create_collection(name=name, configuration={"hnsw": {"space": "cosine"}})


def ingest(pdf_path: Path = config.PDF_PATH, embedder: Embedder | None = None, reset: bool = True) -> dict:
    """PDF -> blocks -> chunks -> embeddings -> Chroma, with page/section/chunk_id stored as metadata."""
    embedder = embedder or Embedder(int8=False)  # stored vectors are always full precision
    blocks = extract_blocks(pdf_path)
    chunks = build_chunks(blocks, embedder.count_tokens)
    vectors = embedder.embed_passages([c.embed_text for c in chunks], progress=True)

    collection = open_collection(reset=reset)
    collection.upsert(
        ids=[f"chunk-{c.chunk_id:04d}" for c in chunks],
        embeddings=vectors.tolist(),
        documents=[c.text for c in chunks],
        metadatas=[c.metadata(Path(pdf_path).name) for c in chunks],
    )
    kinds: dict[str, int] = {}
    for c in chunks:
        kinds[c.kind] = kinds.get(c.kind, 0) + 1
    return {"pages": max(b.page for b in blocks), "chunks": len(chunks), "kinds": kinds,
            "collection": collection.name, "embed_model": embedder.model_name, "chroma_dir": str(config.CHROMA_DIR)}


class Retriever:
    def __init__(self, embedder: Embedder | None = None):
        self.embedder = embedder or Embedder(int8=config.QUERY_INT8)
        self.collection = open_collection()
        if self.collection.count() == 0:
            raise RuntimeError("The vector store is empty. Run:  python rag.py ingest")

    def search(self, query: str, k: int = config.TOP_K, answerable_only: bool = True,
               expand_tables: bool = config.EXPAND_TABLES) -> list[Hit]:
        """Embed the (normalised) query and return the top-k chunks. Works for Hindi or English queries.

        Small-table expansion: every table row is its own chunk (precise for "which year...?" lookups), but a
        question such as "name all the IGMDP missiles" needs the whole table. So when a top-k hit is a row of a
        *small* table (<= TABLE_EXPAND_MAX rows), its sibling rows are appended after the top-k, each with its
        own similarity score. Large lookup tables (timeline, glossary) stay row-addressable."""
        vector = self.embedder.embed_queries([normalize(query)])[0].tolist()
        hits = self._query(vector, k, {"answerable": True} if answerable_only else None)
        if expand_tables:
            seen = {h.chunk_id for h in hits}
            for table_id in dict.fromkeys(h.table_id for h in hits if 0 < h.table_rows <= config.TABLE_EXPAND_MAX):
                rows = self._query(vector, config.TABLE_EXPAND_MAX, {"table_id": table_id})
                hits += [r for r in rows if r.chunk_id not in seen]
                seen.update(r.chunk_id for r in rows)
        return hits

    def _query(self, vector: list[float], n: int, where: dict | None) -> list[Hit]:
        result = self.collection.query(
            query_embeddings=[vector], n_results=n, include=["documents", "metadatas", "distances"], where=where,
        )
        return [
            Hit(chunk_id=meta["chunk_id"], page=meta["page"], page_end=meta["page_end"], section=meta["section"],
                subsection=meta["subsection"], kind=meta["kind"], text=doc, score=1.0 - dist,
                table_id=meta.get("table_id", -1), table_rows=meta.get("table_rows", 0))
            for doc, meta, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0])
        ]
