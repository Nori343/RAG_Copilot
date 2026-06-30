
from __future__ import annotations

from typing import Any

from openai import OpenAI

from config.settings import ABSTAIN_MESSAGE, OPENAI_API_KEY, OPENAI_MODEL


SYSTEM_PROMPT = f"""
    You are a response generation system. You take a query and context(which has the top k returned chunks and their text) and 
    generate an answer to the query. . 

    Rules:
    1. For each stated fact in the answer cite the chunk where the fact came from as '[filename#index]' which 
    is provded above each chunk text
    2. Do not make up any facts, only pull from chunks
    3. Be concise and accurate
    4. If you cannot answer the query with the provided chunks return {ABSTAIN_MESSAGE}

"""


def format_chunks(chunks: list[dict[str, Any]])-> str:
    context = []
    for chunk in chunks:
        cid = f'{chunk.get("filename")}#{chunk.get("chunk_index")}'
        context.append(f"--{cid}--\n{chunk.get('text', '')}")
    return "\n\n".join(context)

def generate_answer(query:str, chunks: list[dict]):
    if not OPENAI_API_KEY:
        return offline_answer(chunks)
    
    if not chunks:
        return ABSTAIN_MESSAGE

    client = OpenAI(api_key=OPENAI_API_KEY)
    context = format_chunks(chunks)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":f'query: {query} \n context: {context}'
            }
        ],
        temperature=0
    )
    return response.choices[0].message.content or ABSTAIN_MESSAGE

def offline_answer(chunks:list[dict]):
    if not chunks:
        return ABSTAIN_MESSAGE

    c = chunks[0]
    cid = f"{c.get('filename')}#{c.get('chunk_index')}"
    text = c.get("text", "")[:300]
    return f"Based on the documentation: {text} [{cid}]"
