
from __future__ import annotations
from multiprocessing import context

from openai import OpenAI
from qdrant_client.grpc import Query

from config.settings import OPENAI_API_KEY, OPENAI_MODEL




def rewrite_query(question: str, history: list[dict]):
    if not history:
        return question
    
    context = history[-3:]
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": """Rewrite follow up question into a standalone question. Pull context from history where
                neccessary to make the question clear and complete. Return only the rewritten question. 
                """
                
            },
            {
                "role": "user",
                "content": f'question: {question} \n history: {context}'
            }
        ],
        temperature=0
    )
    rewritten = response.choices[0].message.content or question
    return rewritten.strip()

def offline_rewrite(question: str, history: list[dict]):
    if not history:
        return question
    prev = history[-1].get("question", "")
    return f"{prev} {question}"