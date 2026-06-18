import os
import json
from typing import Optional

def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3, api_key=api_key)

def safe_invoke(llm, prompt, input_vars):
    if llm is None:
        return json.dumps({"error": "OPENAI_API_KEY not set. Set it in Vercel dashboard."})
    try:
        chain = prompt | llm
        result = chain.invoke(input_vars)
        if hasattr(result, "content"):
            return result.content
        return str(result)
    except Exception as e:
        return json.dumps({"error": str(e)})
