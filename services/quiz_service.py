import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


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

Content:
{text}
""",
)


def generate_quiz(text: str, num_questions: int = 5) -> list[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, api_key=api_key)
    chain = LLMChain(llm=llm, prompt=QUIZ_PROMPT)

    result = chain.invoke({"text": text, "num_questions": str(num_questions)})
    raw = result["text"].strip()

    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        quiz_data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse quiz JSON from LLM response: {raw[:200]}")

    if not isinstance(quiz_data, list):
        raise ValueError("Quiz data is not a list")

    return quiz_data
