import os
import sys
from google import genai
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

while True:
    prompt = input("Prompt: ")
    if prompt.lower() == "exit":
        break

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print(response.text)