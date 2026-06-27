from __future__ import annotations

import hashlib
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import CHUNK_OVERLAP, CHUNK_SIZE

@dataclass
class Chunk:
    doc_type: str
    plan_tier: str
    product_area: str
    doc_version: str
    text: str
    chunk_index: int
    filename: str
    content_hash: str

    @property
    def chunk_id(self):
        return f'{self.filename}#{self.chunk_index}'

def file_content_hash(content:str)-> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def chunk_document(
    filename: str,
    text: str,
    content_hash: str,
    doc_type: str,
    plan_tier: str,
    product_area: str,
    doc_version: str
)->list[Chunk]:
    splitter= RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    split = splitter.split_text(text)
    chunks = []
    for i, chunk in enumerate(split):
        chunks.append(Chunk(
            doc_type=doc_type,
            plan_tier=plan_tier,
            product_area=product_area,
            doc_version=doc_version,
            filename=filename,
            content_hash=content_hash,
            chunk_index=i,
            text=chunk
        ))
    return chunks