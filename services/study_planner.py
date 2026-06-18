import os
import json
from datetime import datetime, date
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


STUDY_PLAN_PROMPT = PromptTemplate(
    input_variables=["exam_date", "total_days", "hours_per_day", "topics"],
    template="""You are an expert study planner. Create a personalized study plan.

Exam date: {exam_date}
Days remaining: {total_days}
Hours available per day: {hours_per_day}
Topics to cover: {topics}

For each day, provide:
{{
  "day": 1,
  "date": "YYYY-MM-DD",
  "topics": ["Topic 1", "Topic 2"],
  "hours": {hours_per_day},
  "focus": "Brief description of what to focus on"
}}

Rules:
- Distribute topics logically over the available days
- Schedule review sessions periodically
- Start from foundational topics and progress to advanced

Return ONLY a valid JSON object with the following structure (no markdown):
{{
  "plan": [day objects...],
  "tips": ["tip1", "tip2", "tip3"]
}}
""",
)


def create_study_plan(
    exam_date_str: str,
    hours_per_day: float,
    topics: str = "General study topics",
) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
    today = date.today()
    total_days = (exam_date - today).days

    if total_days <= 0:
        raise ValueError("Exam date must be in the future")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)
    chain = LLMChain(llm=llm, prompt=STUDY_PLAN_PROMPT)

    result = chain.invoke({
        "exam_date": exam_date_str,
        "total_days": total_days,
        "hours_per_day": hours_per_day,
        "topics": topics,
    })
    raw = result["text"].strip()

    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        plan_data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse study plan JSON: {raw[:200]}")

    if "plan" not in plan_data:
        raise ValueError("Study plan missing 'plan' key")

    plan_data["exam_date"] = exam_date_str
    plan_data["total_days"] = total_days
    plan_data["hours_per_day"] = hours_per_day

    return plan_data
