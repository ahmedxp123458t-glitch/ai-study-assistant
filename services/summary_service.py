import json
from langchain.prompts import PromptTemplate
from services.llm import get_llm, safe_invoke


SUMMARY_PROMPT = PromptTemplate(
    input_variables=["text", "detail_level"],
    template="""You are an expert study assistant. Summarize the following academic content.

Detail level: {detail_level}
- "brief": 2-3 sentences covering only the main idea
- "standard": short paragraph covering key points and conclusions
- "detailed": comprehensive summary with bullet points covering all major concepts

Content to summarize:
{text}

Summary:""",
)


def generate_summary(text: str, detail_level: str = "standard") -> str:
    llm = get_llm()
    if llm is None:
        return "OPENAI_API_KEY not configured. Please set it in Vercel Environment Variables."

    result = safe_invoke(llm, SUMMARY_PROMPT, {"text": text, "detail_level": detail_level})
    try:
        parsed = json.loads(result)
        if "error" in parsed:
            return f"Error: {parsed['error']}"
    except json.JSONDecodeError:
        pass
    return result