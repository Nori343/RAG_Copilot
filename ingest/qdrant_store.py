
from __future__ import annotations

from pickle import NONE
from turtle import distance
import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from config.settings import (
    EMBEDDING_DIM,
    QDRANT_COLLECTION,
    QDRANT_LOCAL_PATH,
    QDRANT_URL,
)
from ingest.chunking import Chunk

_client: QdrantClient | None = None

def chunk_point_id(filename: str, chunk_index: int)->str:
    name = f'{filename}#{chunk_index}'
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))

def get_client()->QdrantClient:
    global _client
    if _client is None:
        if QDRANT_URL:
            _client  = QdrantClient(url=QDRANT_URL)
        else:
            QDRANT_LOCAL_PATH.mkdir(parents=True, exist_ok=True)
            _client = QdrantClient(path=str(QDRANT_LOCAL_PATH))
    return _client

def close_client():
    global _client
    if _client:
        _client.close()
        _client = None

def ensure_collection(recreate: bool)->None:
    client = get_client()
    exists = client.collection_exists(QDRANT_COLLECTION)
    if recreate and exists:
        client.delete_collection(QDRANT_COLLECTION)
        exists = False

    if not exists:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE)
        )


def upsert_chunks(chunks:list, embeddings:list):
    client = get_client()
    points = []
    for chunk, vector in zip(chunks, embeddings):
        points.append(PointStruct(
            id=chunk_point_id(chunk.filename, chunk.chunk_index),
            vector=vector,
            payload={
                    "filename": chunk.filename,
                    "chunk_index": chunk.chunk_index,
                    "chunk_id": chunk.chunk_id,
                    "text": chunk.text,
                    "content_hash": chunk.content_hash,
                    "doc_type": chunk.doc_type,
                    "plan_tier": chunk.plan_tier,
                    "product_area": chunk.product_area,
                    "doc_version": chunk.doc_version,                
            }
        ))
    client.upsert(collection_name=QDRANT_COLLECTION, points=points)


def collection_count()->int:
    client = get_client()
    if not client.collection_exists(QDRANT_COLLECTION):
        return 0
    data = client.get_collection(QDRANT_COLLECTION)
    return data.points_count or 0
