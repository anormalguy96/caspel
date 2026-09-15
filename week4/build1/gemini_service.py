from google import genai
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path
import os
from schemas import ResumeData

load_dotenv(Path(__file__).resolve().parent / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found.")

if not MODEL_NAME:
    raise RuntimeError("MODEL_NAME not found.")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are a resume information extraction system.

Extract only information explicitly present in the resume.

Rules:
- Do not invent information.
- If the name is missing, return null.
- If skills are missing, return an empty list.
- If experience is missing, return an empty list.
- If education is missing, return an empty list.
- Preserve the meaning of the resume."""

TEST_CV = """Ali Mammadov

Backend Developer

Skills:
Java, Spring Boot, PostgreSQL, Docker

Experience:
Backend Developer at ABC Technologies, 2023-2025.
Developed REST APIs using Java and Spring Boot.

Education:
UNEC
Bachelor of Computer Engineering
2019-2023"""

def extract_resume_data(resume_text: str) -> ResumeData:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=resume_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ResumeData,
                temperature=0.1,
            ),
        )

        if not response.text:
            raise RuntimeError("Model empty response.")
        elif response.parsed is None:
            raise RuntimeError("No parsed content returned.")
        else:
            return response.parsed

    except Exception as e:
        raise RuntimeError(f"Gemini API xətası: {str(e)}")


if __name__ == "__main__":
    print("Test CV:")
    print(TEST_CV)
    print("\n" + "="*50)
    try:
        result = extract_resume_data(TEST_CV)
        print("\nƏldə edilən məlumatlar:")
        print(f"Ad: {result.name}")
        print(f"Bacarıqlar: {', '.join(result.skills)}")
        print(f"Təcrübə: {', '.join(result.experience)}")
        print(f"Təhsil: {', '.join(result.education)}")
    except Exception as e:
        print(f"\nXəta baş verdi: {str(e)}")