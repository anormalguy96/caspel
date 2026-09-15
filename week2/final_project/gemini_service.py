from google import genai
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY tapılmadı.")

if not MODEL_NAME:
    raise RuntimeError("MODEL_NAME tapılmadı.")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="Yalnız Azərbaycan dilində cavab ver.",
            temperature=0.7,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )

    if not response.text:
        raise RuntimeError("Model boş cavab qaytardı.")

    return response.text
