from __future__ import annotations

from typing import Any

from pydantic.types import T

sessions : dict[str, list[dict[str, Any]]] = {}

def get_history(thread_id: str):
    return list(sessions.get("thread_id", []))

def save_turn(thread_id:str, question: str, answer: str):
    if thread_id not in sessions:
        sessions[thread_id] = []
    sessions[thread_id].append({"question": question, "answer": answer})

def clear_session(thread_id: str):
    sessions.pop(thread_id, None)

def clear_all():
    sessions.clear()
