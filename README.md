# AI Study Assistant

An intelligent study companion that helps students learn faster by generating summaries, quizzes, flashcards, and study plans from their study materials.

## Features

- **PDF Upload & Text Extraction** - Upload textbook chapters, notes, or any PDF
- **AI Summarization** - Generate summaries at different detail levels (brief, standard, detailed)
- **Quiz Generation** - Create multiple-choice quizzes from your study material
- **Flashcards** - Generate front/back flashcards for active recall
- **Important Questions** - Extract key exam-relevant questions
- **Study Planner** - Create personalized study plans based on exam date and daily availability

## Tech Stack

- **Backend:** Python, FastAPI
- **AI:** LangChain + OpenAI GPT
- **PDF Parsing:** PyPDF2
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templates)
- **Database:** SQLite

## Project Structure

```
ai-study-assistant/
├── app.py                         # FastAPI main application
├── models.py                      # Pydantic data models
├── database.py                    # SQLite database setup
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore
├── uploads/                       # Temporary PDF upload directory
├── services/
│   ├── pdf_service.py             # PDF parsing & text extraction
│   ├── summary_service.py         # AI summarization (LangChain)
│   ├── quiz_service.py            # MCQ quiz generation
│   ├── flashcard_service.py       # Flashcard generation
│   ├── question_service.py        # Important questions extraction
│   └── study_planner.py           # Study plan creation
└── templates/
    └── index.html                 # Frontend interface
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-study-assistant.git
cd ai-study-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in browser

Navigate to: `http://localhost:8000`

## Project Flow

1. **Upload Material** → Upload a PDF or paste notes/text content
2. **Choose Action**:
   - **Summarize** → Select detail level (Brief / Standard / Detailed)
   - **Generate Quiz** → Specify number of MCQs needed
   - **Create Flashcards** → Specify number of cards
   - **Extract Questions** → Get important exam questions
   - **Study Planner** → Enter exam date and hours per day
3. **Review Results** → All generated content is displayed in the interface
4. **History** → Past study materials are saved and accessible

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Frontend interface |
| POST | `/api/upload` | Upload PDF file |
| POST | `/api/summarize` | Generate AI summary |
| POST | `/api/quiz` | Generate MCQs |
| POST | `/api/questions` | Extract important questions |
| POST | `/api/flashcards` | Generate flashcards |
| POST | `/api/study-plan` | Create study plan |
| GET | `/api/history` | Get study history |
