
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

#Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
MANIFEST_PATH = DATA_DIR / "manifest.json"
INGEST_STATE_PATH = DATA_DIR / "ingest_state.json"
QDRANT_LOCAL_PATH = DATA_DIR / "qdrant"

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIM = 1536  # text-embedding-3-small

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL", "")  # empty → local path mode
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "relayboard_docs")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIM = 1536  # text-embedding-3-small

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100