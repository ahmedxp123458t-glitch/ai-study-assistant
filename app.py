import os
import uuid
import json
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from models import (
    SummarizeRequest,
    QuizRequest,
    QuestionRequest,
    FlashcardRequest,
    StudyPlanRequest,
)
from database import init_db, save_material, save_summary, save_quiz, save_flashcards, save_questions, save_study_plan, get_history
from services.pdf_service import extract_text_from_upload
from services.summary_service import generate_summary
from services.quiz_service import generate_quiz
from services.flashcard_service import generate_flashcards
from services.question_service import generate_important_questions
from services.study_planner import create_study_plan

load_dotenv()

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    import sys
    try:
        init_db()
    except Exception as e:
        print(f"Startup DB error: {e}", file=sys.stderr)
    yield


app = FastAPI(title="AI Study Assistant", lifespan=lifespan)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        return HTMLResponse(f"<html><body><h1>Server Error</h1><p>{str(e)}</p></body></html>", status_code=500)
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    ext = Path(file.filename).suffix.lower()
    if ext != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = UPLOAD_DIR / unique_name

    content = await file.read()
    save_path.write_bytes(content)

    try:
        filename, text = extract_text_from_upload(str(save_path))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF processing failed: {str(e)}")
    finally:
        if save_path.exists():
            save_path.unlink()

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")

    material_id = save_material(filename, "pdf", text[:100000])
    return {"material_id": material_id, "filename": filename, "text": text[:100000], "length": len(text)}


@app.post("/api/summarize")
async def summarize(req: SummarizeRequest):
    try:
        summary = generate_summary(req.content, req.detail_level)
        material_id = save_material("Quick Summary", "notes", req.content[:100000])
        save_summary(material_id, summary, req.detail_level)
        return {"summary": summary, "material_id": material_id}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/quiz")
async def quiz(req: QuizRequest):
    try:
        questions = generate_quiz(req.content, req.num_questions)
        material_id = save_material("Quiz", "notes", req.content[:100000])
        save_quiz(material_id, json.dumps(questions), req.num_questions)
        return {"questions": questions, "material_id": material_id}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/questions")
async def important_questions(req: QuestionRequest):
    try:
        questions = generate_important_questions(req.content, req.num_questions)
        material_id = save_material("Important Questions", "notes", req.content[:100000])
        save_questions(material_id, json.dumps(questions))
        return {"questions": questions, "material_id": material_id}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/flashcards")
async def flashcards(req: FlashcardRequest):
    try:
        cards = generate_flashcards(req.content, req.num_cards)
        material_id = save_material("Flashcards", "notes", req.content[:100000])
        save_flashcards(material_id, json.dumps(cards), req.num_cards)
        return {"flashcards": cards, "material_id": material_id}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/study-plan")
async def study_plan(req: StudyPlanRequest):
    try:
        topics = req.topics or "General study topics"
        if req.content:
            topics = req.content[:500]
        plan = create_study_plan(req.exam_date, req.hours_per_day, topics)
        save_study_plan(req.exam_date, req.hours_per_day, json.dumps(plan))
        return plan
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def history():
    return get_history()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
