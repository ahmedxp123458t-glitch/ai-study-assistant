import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


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
- Focus on conceptual understanding and key facts
- Questions should be the type that appear on exams
- Cover a range of difficulty levels

Return ONLY a valid JSON array of objects, with no additional text or markdown formatting.

Content:
{text}
""",
)


def generate_important_questions(text: str, num_questions: int = 5) -> list[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)
    chain = LLMChain(llm=llm, prompt=QUESTIONS_PROMPT)

    result = chain.invoke({"text": text, "num_questions": str(num_questions)})
    raw = result["text"].strip()

    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        questions = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse questions JSON: {raw[:200]}")

    if not isinstance(questions, list):
        raise ValueError("Questions data is not a list")

    return questions
