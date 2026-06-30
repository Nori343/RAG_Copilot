from __future__ import annotations

import re
from typing import Any

from config.settings import ABSTAIN_MESSAGE

# Matches [filename#chunk_index] citations
CITATION_RE = re.compile(r"\[([^\]#]+)#(\d+)\]")

def extract_citations(text: str):
    return [(m.group(1), int(m.group(2))) for m in CITATION_RE.finditer(text)]


def verify_citations(
    answer: str,
    chunks: list[dict[str, Any]],
    abstained: bool = False
):
    citations = extract_citations(answer)

    if abstained:
        if citations:
            return False, citations, "abstained must not have citations"
        if ABSTAIN_MESSAGE not in answer:
            return False, citations, "abstained must return ABSTAIN_MESSSAGE"
        return True, citations, "ok"
    
    if not citations:
        return False, citations, "No citations in answer"
    
    possible = {(c.get("filename"), c.get("chunk_index")) for c in chunks}
    for item in citations:
        if item not in possible:
            return False, citations, "hallucinatd citation"
    return True, citations, "ok"


