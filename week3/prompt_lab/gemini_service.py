import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parent / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.6-flash")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY tapılmadı.")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(prompt: str, system_prompt: str, temperature: float = 0.7, retries: int = 3) -> str:
    """Gemini modelinə sorğu göndərir və cavab qaytarır."""
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    ),
                ),
            )

            if not response.text:
                raise RuntimeError("Model boş cavab qaytardı.")

            return response.text
        except Exception as e:
            if "429" in str(e) and attempt < retries - 1:
                time.sleep(6)
            else:
                raise e
