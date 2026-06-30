from __future__ import annotations

from typing import Any

from config.settings import ABSTAIN_MESSAGE, RETRIEVAL_CANDIDATE_K, RERANK_TOP_K
from pipeline.filters import infer_filters, merge_filters
from pipeline.generate import generate_answer
from pipeline.grade import grade_retrieval
from pipeline.rerank import rerank_chunks
from pipeline.retrieve import hybrid_search
from pipeline.rewrite import rewrite_query
from pipeline.verify import extract_citations, verify_citations
from state.session_store import get_history, save_turn

"Full RAG pipeline: rewrite → filter → retrieve → rerank → grade → generate → verify."

def answer_question(
    question: str,
    thread_id: str,
    explicit_filters: dict[str, str],
    debug: bool = False
):
    history = get_history(thread_id)
    rewrite = rewrite_query(question, history)

    filters = merge_filters(infer_filters(question), explicit_filters)

    chunks = hybrid_search(question, RETRIEVAL_CANDIDATE_K, filters)

    rerank = rerank_chunks(question, chunks, RERANK_TOP_K)

    grade, message = grade_retrieval(rerank)

    if not grade:
        print(message)
    
    answer =  generate_answer(question, rerank)

    verify, citations, v_message = verify_citations(answer, rerank)

    abstained = False
    if not verify:
        abstained = True
        answer = ABSTAIN_MESSAGE
        verify = True
    
    result: dict[str, Any] = {
        "answer": answer,
        "citations": [{"filename": f, "chunk_index": i} for f, i in citations],
        "chunks": chunks,
        "retrieval_query": rewrite,
        "filters": filters,
        "verification_passed": verify,
        "abstain": abstained
    }
    return result

    
