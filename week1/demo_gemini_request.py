import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

model = genai.Client(api_key=api_key)

while True:
    prompt = input("Prompt: ")
    if prompt == "exit":
        break

    response = model.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print(response.text)