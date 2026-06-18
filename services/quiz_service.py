import json
from langchain.prompts import PromptTemplate
from services.llm import get_llm, safe_invoke


QUIZ_PROMPT = PromptTemplate(
    input_variables=["text", "num_questions"],
    template="""You are an expert quiz generator for students. Based on the following study content, generate {num_questions} multiple-choice questions.

Each question must follow this JSON format:
{{
  "question": "The question text",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_answer": "The correct option text",
  "explanation": "Brief explanation of why this is correct"
}}

Return ONLY a valid JSON array of objects, with no additional text or markdown formatting.
Content: {text}
""",
)


def generate_quiz(text: str, num_questions: int = 5) -> list:
    llm = get_llm()
    if llm is None:
        return [{"question": "API key not configured", "options": ["A) Set OPENAI_API_KEY"], "correct_answer": "A) Set OPENAI_API_KEY", "explanation": "Configure the environment variable in Vercel dashboard."}]

    result = safe_invoke(llm, QUIZ_PROMPT, {"text": text[:3000], "num_questions": num_questions})
    try:
        parsed = json.loads(result)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict) and "error" in parsed:
            return [{"question": "Error", "options": ["A) Try again"], "correct_answer": "A) Try again", "explanation": parsed["error"]}]
    except json.JSONDecodeError:
        pass
    return [{"question": "Generation failed", "options": ["A) Try again"], "correct_answer": "A) Try again", "explanation": "Could not parse response"}]