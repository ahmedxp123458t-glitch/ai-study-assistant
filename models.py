from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class NotesInput(BaseModel):
    text: str = Field(..., min_length=1, description="Text content to process")


class SummarizeRequest(BaseModel):
    content: str = Field(..., min_length=1)
    detail_level: str = "standard"


class QuizRequest(BaseModel):
    content: str = Field(..., min_length=1)
    num_questions: int = Field(default=5, ge=1, le=20)


class QuestionRequest(BaseModel):
    content: str = Field(..., min_length=1)
    num_questions: int = Field(default=5, ge=1, le=20)


class FlashcardRequest(BaseModel):
    content: str = Field(..., min_length=1)
    num_cards: int = Field(default=5, ge=1, le=30)


class StudyPlanRequest(BaseModel):
    exam_date: str = Field(..., description="Date of exam (YYYY-MM-DD)")
    hours_per_day: float = Field(..., gt=0, le=24)
    content: Optional[str] = None
    topics: Optional[str] = None


class QuizItem(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None


class Flashcard(BaseModel):
    front: str
    back: str


class StudyPlanDay(BaseModel):
    day: int
    date: str
    topics: List[str]
    hours: float
    focus: str


class StudyPlan(BaseModel):
    exam_date: str
    total_days: int
    hours_per_day: float
    plan: List[StudyPlanDay]
    tips: Optional[List[str]] = None
