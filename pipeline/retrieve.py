from __future__ import annotations

from typing import Any

from openai import OpenAI
from rank_bm25 import BM25Okapi

from config.settings import (
    EMBEDDING_MODEL,
    OPENAI_API_KEY,
    QDRANT_COLLECTION,
    RETRIEVAL_CANDIDATE_K,
    RRF_K,
)
from ingest.qdrant_store import build_qdrant_filter, get_client, scroll_all_points

_bm25: BM25Okapi | None = None
_courpus_chunks: list[dict[str, Any]]  = []
_index_loaded = False

def tokenize(text:str)->list[str]:
    return text.lower().split()


def reload_index():
    global _bm25, _courpus_chunks, _index_loaded
    _courpus_chunks = scroll_all_points()
    if not _courpus_chunks:
        _bm25 = None
        _index_loaded = True
        return
    tokenized = [tokenize(chunk.get("text", "")) for chunk in _courpus_chunks]
    if not any(tokenized):
        _bm25 = None
        _index_loaded = True
        return
    _bm25 = BM25Okapi(tokenized)
    _index_loaded = True
    return 

def ensure_index():
    if _index_loaded:
        return
    reload_index()
    return

def apply_payload_filter(filters: dict, chunks: list[dict]):
    if not filters:
        return chunks
    filtered = []
    for chunk in chunks:
        match = True
        for key, val in filters.items():
            if key == 'plan_tier':
                if chunk.get("plan_tier","") not in [val, "all"]:
                    match = False
                    break
            else:
                if chunk.get(key) != val:
                    match = False
                    break
        if match:
            filtered.append(chunk)
    return filtered


def embed_query(query: str)->list[float]:
    if not OPENAI_API_KEY:
        raise  RuntimeError("OPENAI_API_KEY required for dense retrieval")
    client = OpenAI(api_key=OPENAI_API_KEY)
    vector = client.embeddings.create(model=EMBEDDING_MODEL, input=[query])
    return vector.data[0].embedding

def _dense_search(query: str, top_k: int, filters: dict):
    if not query or query == " ":
        raise RuntimeError("query empty cannot retrieve")
    
    vector = embed_query(query)
    qdrant_filter = build_qdrant_filter(filters)
    client = get_client()
    response = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=vector,
        limit=top_k,
        query_filter=qdrant_filter,
        with_payload=True
    )
    return [dict(p.payload) for p in response.points if p.payload is not None]

def _bm25_search(query: str, top_k:int, filters:dict):
    q = tokenize(query)
    ensure_index()
    if _bm25 is None:
        return []
    filtered = apply_payload_filter(filters, _courpus_chunks)
    filtered_ids = {c.get("chunk_id") for c in filtered}
    indices = [i for i, c in enumerate(_courpus_chunks) if c.get("chunk_id", "") in filtered_ids]
    results = _bm25.get_scores(q)
    valid_results = [(results[i], _courpus_chunks[i]) for i in indices]
    valid_results.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in valid_results[:top_k]]

def _rrf_merge(dense_chunks: list[dict], bm_25_chunks:list[dict], k:int = RRF_K):
    chunk_map = {}
    scores = {}
    for rank, chunk in enumerate(dense_chunks):
        cid = chunk.get("chunk_id")
        chunk_map[cid] = chunk
        scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank + 1.0)
    for rank, chunk in enumerate(bm_25_chunks):
        cid = chunk.get("chunk_id")
        chunk_map[cid] = chunk
        scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank + 1.0)
    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [chunk_map[cid] for cid in sorted_ids]

def hybrid_search(query: str, top_k: int = RRF_K, filters: dict | None = None):
    active_filters = filters if filters is not None else {}
    dense = _dense_search(query, top_k, active_filters)
    bm25 = _bm25_search(query, top_k, active_filters)
    result = _rrf_merge(dense, bm25, top_k)
    return result[:top_k]