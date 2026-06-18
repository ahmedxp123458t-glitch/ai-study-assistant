import json
from datetime import datetime, date
from langchain.prompts import PromptTemplate
from services.llm import get_llm, safe_invoke


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
  "focus_area": "Main topic for the day",
  "topics": ["specific subtopics"],
  "hours": 2,
  "activities": ["activity 1", "activity 2"],
  "resources": ["resource suggestion"],
  "status": "pending"
}}

Return ONLY a valid JSON array of day objects, with no additional text.
""",
)


def create_study_plan(exam_date: str, hours_per_day: float = 2.0, topics: str = "General study topics") -> list:
    llm = get_llm()
    if llm is None:
        return [{"day": 1, "date": exam_date, "focus_area": "API Key Required", "topics": ["Set OPENAI_API_KEY"], "hours": hours_per_day, "activities": ["Configure environment variable in Vercel"], "resources": ["Vercel Dashboard"], "status": "pending"}]

    try:
        exam = datetime.strptime(exam_date, "%Y-%m-%d").date()
        today = date.today()
        total_days = max((exam - today).days, 1)
    except ValueError:
        total_days = 30

    result = safe_invoke(llm, STUDY_PLAN_PROMPT, {
        "exam_date": exam_date,
        "total_days": str(total_days),
        "hours_per_day": str(hours_per_day),
        "topics": topics[:500],
    })
    try:
        parsed = json.loads(result)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict) and "error" in parsed:
            return [{"day": 1, "date": exam_date, "focus_area": "Error", "topics": [parsed["error"]], "hours": hours_per_day, "activities": ["Check configuration"], "resources": [], "status": "pending"}]
    except json.JSONDecodeError:
        pass
    return [{"day": 1, "date": exam_date, "focus_area": "Study Plan", "topics": [topics[:50]], "hours": hours_per_day, "activities": ["Review material", "Practice problems"], "resources": ["Course materials"], "status": "pending"}]