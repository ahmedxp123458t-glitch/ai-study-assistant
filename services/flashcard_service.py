import json
from langchain.prompts import PromptTemplate
from services.llm import get_llm, safe_invoke


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
- Cover different concepts from the text

Return ONLY a valid JSON array of objects, with no additional text.
Content: {text}
""",
)


def generate_flashcards(text: str, num_cards: int = 5) -> list:
    llm = get_llm()
    if llm is None:
        return [{"front": "API Key Required", "back": "Set OPENAI_API_KEY in Vercel Environment Variables."}]

    result = safe_invoke(llm, FLASHCARD_PROMPT, {"text": text[:3000], "num_cards": num_cards})
    try:
        parsed = json.loads(result)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict) and "error" in parsed:
            return [{"front": "Error", "back": parsed["error"]}]
    except json.JSONDecodeError:
        pass
    return [{"front": "Generation failed", "back": "Could not parse response. Try again."}]