"""Deterministic retrieval grading."""

from __future__ import annotations

from typing import Any

# Minimum combined score proxy: at least one chunk with substantive text
MIN_CHUNK_TEXT_LEN = 50


def grade_retrieval(chunks: list[dict[str, Any]]) -> tuple[bool, str]:
    """
    Grade whether retrieved chunks are sufficient for answering.
    Returns (passed, reason).
    """
    if not chunks:
        return False, "no_chunks_retrieved"

    substantive = [c for c in chunks if len(c.get("text", "")) >= MIN_CHUNK_TEXT_LEN]
    if not substantive:
        return False, "chunks_too_short"

    if len(substantive) < 1:
        return False, "insufficient_substantive_chunks"

    return True, "ok"
