import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "study_assistant.db")


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content_type TEXT NOT NULL DEFAULT 'notes',
            raw_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            summary_text TEXT NOT NULL,
            detail_level TEXT DEFAULT 'standard',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES study_materials(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            quiz_data TEXT NOT NULL,
            num_questions INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES study_materials(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            card_data TEXT NOT NULL,
            num_cards INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES study_materials(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS important_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            questions_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES study_materials(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_date TEXT NOT NULL,
            hours_per_day REAL NOT NULL,
            plan_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_material(title: str, content_type: str, raw_text: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO study_materials (title, content_type, raw_text) VALUES (?, ?, ?)",
        (title, content_type, raw_text),
    )
    conn.commit()
    material_id = cursor.lastrowid
    conn.close()
    return material_id


def save_summary(material_id: int, summary_text: str, detail_level: str = "standard"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO summaries (material_id, summary_text, detail_level) VALUES (?, ?, ?)",
        (material_id, summary_text, detail_level),
    )
    conn.commit()
    conn.close()


def save_quiz(material_id: int, quiz_data: str, num_questions: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quizzes (material_id, quiz_data, num_questions) VALUES (?, ?, ?)",
        (material_id, quiz_data, num_questions),
    )
    conn.commit()
    conn.close()


def save_flashcards(material_id: int, card_data: str, num_cards: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO flashcards (material_id, card_data, num_cards) VALUES (?, ?, ?)",
        (material_id, card_data, num_cards),
    )
    conn.commit()
    conn.close()


def save_questions(material_id: int, questions_data: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO important_questions (material_id, questions_data) VALUES (?, ?)",
        (material_id, questions_data),
    )
    conn.commit()
    conn.close()


def save_study_plan(exam_date: str, hours_per_day: float, plan_data: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO study_plans (exam_date, hours_per_day, plan_data) VALUES (?, ?, ?)",
        (exam_date, hours_per_day, plan_data),
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, content_type, created_at FROM study_materials ORDER BY created_at DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
