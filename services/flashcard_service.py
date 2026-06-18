import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


FLASHCARD_PROMPT = PromptTemplate(
    input_variables=["text", "num_cards"],
    template="""You are an expert at creating study flashcards. Based on the following content, generate {num_cards} flashcards.

Each flashcard must follow this JSON format:
{{
  "front": "The term, question, or concept name",
  "back": "The definition or answer"
}}

Rules:
- Make front concise and specific
- Make back clear and informative
- Cover distinct concepts (no duplicates)

Return ONLY a valid JSON array of objects, with no additional text or markdown formatting.

Content:
{text}
""",
)


def generate_flashcards(text: str, num_cards: int = 5) -> list[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, api_key=api_key)
    chain = LLMChain(llm=llm, prompt=FLASHCARD_PROMPT)

    result = chain.invoke({"text": text, "num_cards": str(num_cards)})
    raw = result["text"].strip()

    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        cards = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse flashcards JSON: {raw[:200]}")

    if not isinstance(cards, list):
        raise ValueError("Flashcard data is not a list")

    return cards
