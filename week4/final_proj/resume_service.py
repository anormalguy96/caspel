from schemas import ResumeData
from pdf_service import extract_text_from_pdf
from gemini_service import extract_resume_data
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).resolve().parent / ".env")

SYSTEM_PROMPT = """
You are an expert HR assistant. Parse the following resume text.

Extract:
- name
- skills (as a list)
- experience (as a list)
- education (as a list)

If any field is missing, return null for name and [] for lists.

Return ONLY a valid JSON object matching the ResumeData schema.

Resume text:
{resume_text}
"""

def parse_raw_text(raw_text: str) -> ResumeData:
    if not raw_text.strip():
        raise ValueError("Resume text boş ola bilməz.")

    return extract_resume_data(raw_text)


def parse_resume_pdf(file_path: str) -> ResumeData:
    raw_text = extract_text_from_pdf(file_path)
    return parse_raw_text(raw_text)