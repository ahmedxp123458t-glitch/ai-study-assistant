import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


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
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)
    chain = LLMChain(llm=llm, prompt=SUMMARY_PROMPT)
    result = chain.invoke({"text": text, "detail_level": detail_level})
    return result["text"].strip()
