from __future__ import annotations

import argparse
from fileinput import filename
import json
import sys
from pathlib import Path

from openai import OpenAI

from config.settings import (
    DATA_DIR,
    EMBEDDING_MODEL,
    INGEST_STATE_PATH,
    MANIFEST_PATH,
    OPENAI_API_KEY,
    RAW_DIR,
)
from ingest import frontmatter
from ingest.chunking import chunk_document, file_content_hash
from ingest.frontmatter import parse_frontmatter
from ingest.qdrant_store import (
    close_client,
    collection_count,
    ensure_collection,
    get_client,
    upsert_chunks,
)

def load_ingest_state()->dict:
    if INGEST_STATE_PATH.exists():
        return json.loads(INGEST_STATE_PATH.read_text(encoding="utf-8"))
    return {"files": {}}

def save_ingest_state(state:dict)->None:
    INGEST_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    INGEST_STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

def clear_ingest_state()->None:
    if INGEST_STATE_PATH.exists():
        INGEST_STATE_PATH.unlink()

def embed_texts(texts: list[str])->list[list[float]]:
    api_key = OPENAI_API_KEY
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY required for embedding during ingest")
    client = OpenAI(api_key=api_key)
    embeddings: list[list[float]] = []
    for i in range(0, len(texts), 100):
        batch = texts[i:i+100]
        response = client.embeddings.create(model=EMBEDDING_MODEL,input=batch)
        embeddings.extend([chunk.embedding for chunk in response.data])
    return embeddings

def ingest_file(
    rel_path:str,
    meta: dict,
    state:dict,
    force:bool=False
)->int:
        filename = Path(rel_path).name
        path = DATA_DIR/rel_path
        content = path.read_text(encoding="utf-8")
        fhash = file_content_hash(content)

        if state.get("files").get(filename) == fhash and not force:
            print(f'skip {filename} unchanged fhash')
            return 0

        frontmatter, body = parse_frontmatter(content)
        doc_meta = {**meta, **frontmatter}
        chunks = chunk_document(
            filename=filename,
            text=body,
            content_hash=fhash,
            doc_type=doc_meta.get("doc_type", "unkown"),
            plan_tier=doc_meta.get("plan_tier", "all"),
            product_area=doc_meta.get("product_area", "unkwown"),
            doc_version=doc_meta.get("doc_version", "1.0")
        )

        if not chunks:
            print(f"  WARN {filename}: no chunks produced")
            return 0

        chunk_text = [c.text for c in chunks]
        embeddings = embed_texts(chunk_text)
        upsert_chunks(chunks, embeddings)
        state.setdefault("files", {})[filename] = fhash
        print(f"  OK   {filename}: {len(chunks)} chunks")
        return len(chunks)

        
def run_batch(force: bool = False, recreate: bool = False)->None:
    if recreate:
        print(f'--recreate: clearing collection and ingest state')
        ensure_collection(recreate)
        clear_ingest_state()
        force = True
    else:
        ensure_collection(recreate)
    
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    metas= []
    for m in manifest.get("files"):
        metas.append({
            "doc_type": m.get("doc_type", ""),
            "plan_tier": m.get("plan_tier", ""),
            "product_area": m.get("plan_tier",""),
            "doc_version": m.get("doc_version", "")
        })
    paths = [m.get("path") for m in manifest.get("files")]
    state = load_ingest_state()
    files_changed=0
    total_chunks=0
    for i, path in enumerate(paths):
        if not (DATA_DIR / path).exists():
            print(f'Error: invalid file path {path}')
            continue
        n = ingest_file(path, metas[i], state, force)
        total_chunks += n
        if n>0:
            files_changed += 1
    save_ingest_state(state)
    final_count = collection_count()
    print(f"\nIngest complete: {files_changed} files updated, {total_chunks} chunks embedded")
    print(f"Collection total: {final_count} points")


    

def main() -> None:
    parser = argparse.ArgumentParser(description="Batch ingest RelayBoard docs into Qdrant")
    parser.add_argument("--force", action="store_true", help="Re-embed all files regardless of hash")
    parser.add_argument("--recreate", action="store_true", help="Drop collection, clear state, re-ingest all")
    args = parser.parse_args()
    try:
        get_client()  # init early
        run_batch(force=args.force, recreate=args.recreate)
    finally:
        close_client()


if __name__ == "__main__":
    main()





