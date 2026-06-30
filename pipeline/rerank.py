from __future__ import annotations

from tkinter import N, NO
from typing import Any

from config.settings import RERANK_ENABLED, RERANK_TOP_K

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import CrossEncoder
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _model

def rerank_chunks(
    query:str,
    chunks: list[dict[str, Any]],
    top_k: int | None = None
):
    k = top_k or RERANK_TOP_K
    if not RERANK_ENABLED or not chunks:
        return chunks[:k]
    
    model = _get_model()
    pairs = [(query, c.get("text", "")) for c in chunks]
    scores = model.predict(pairs)
    scored = list(zip(scores, chunks))
    scored.sort(key=lambda x:x[0], reverse=True)
    return [chunk for _, chunk in scored[:k]]
