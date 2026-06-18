import json
from langchain.prompts import PromptTemplate
from services.llm import get_llm, safe_invoke


QUESTIONS_PROMPT = PromptTemplate(
    input_variables=["text", "num_questions"],
    template="""You are an expert academic tutor. Based on the following content, extract the {num_questions} most important exam-style questions.

Each question must follow this JSON format:
{{
  "question": "The important question text",
  "answer": "A concise model answer or key points to include",
  "difficulty": "easy/medium/hard",
  "topics": ["topic1", "topic2"]
}}

Rules:
- Cover different aspects of the content
- Mix easy, medium, and hard questions
- Provide clear, accurate model answers

Return ONLY a valid JSON array of objects, with no additional text.
Content: {text}
""",
)


def generate_important_questions(text: str, num_questions: int = 5) -> list:
    llm = get_llm()
    if llm is None:
        return [{"question": "API Key Required", "answer": "Set OPENAI_API_KEY in Vercel Environment Variables.", "difficulty": "easy", "topics": ["configuration"]}]

    result = safe_invoke(llm, QUESTIONS_PROMPT, {"text": text[:3000], "num_questions": num_questions})
    try:
        parsed = json.loads(result)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict) and "error" in parsed:
            return [{"question": "Error", "answer": parsed["error"], "difficulty": "easy", "topics": ["error"]}]
    except json.JSONDecodeError:
        pass
    return [{"question": "Generation failed", "answer": "Could not parse response.", "difficulty": "easy", "topics": ["error"]}]