import os
from dotenv import load_dotenv
from google import genai
import httpx
from google.genai import errors, types

def main():
    load_dotenv("week1/.env")

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("MODEL_NAME")
    language = os.getenv("LANGUAGE")

    if not api_key:
        print("GEMINI_API_KEY not found")
        return
    
    if not model_name:
        print("MODEL_NAME not found")
        return
    
    client = genai.Client(api_key=api_key)

    with open("week1/input.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    
    if not response.text:
        print("Prompt yoxdur.")
        return
    
    with open("week1/output/result.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
        
try:
    if __name__ == "__main__":
        main()

except ValueError as e:
    print(f"Konfiqurasiya xətası: {e}")

except FileNotFoundError as e:
    print(f"Fayl tapılmadı: {e.filename}")

except PermissionError:
    print("İcazə xətası: faylı oxumaq və ya yazmaq mümkün olmadı.")

except httpx.ConnectError:
    print("Şəbəkə xətası: Gemini serverinə qoşulmaq mümkün olmadı.")

except httpx.TimeoutException:
    print("Timeout: Gemini serverindən vaxtında cavab gəlmədi.")

except errors.APIError as e:
    print(f"\nGemini API xətası ({e.code}): {e.message}\n")

except RuntimeError as e:
    print(f"Runtime xətası: {e}")

except OSError as e:
    print(f"Sistem xətası: {e}")

except Exception as e:
    print(f"Gözlənilməyən xəta: {type(e).__name__}: {e}")