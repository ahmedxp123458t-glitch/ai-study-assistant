import os
import PyPDF2
from typing import Optional


def extract_text_from_pdf(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    text_parts = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        if len(reader.pages) == 0:
            raise ValueError("PDF file has no pages")

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text.strip())

    full_text = "\n\n".join(text_parts)
    if not full_text.strip():
        raise ValueError("No text could be extracted from the PDF")

    return full_text


def extract_text_from_upload(upload_path: str) -> tuple[str, str]:
    filename = os.path.basename(upload_path)
    text = extract_text_from_pdf(upload_path)
    return filename, text
