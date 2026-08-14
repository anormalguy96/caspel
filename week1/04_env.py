import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("API_KEY"))
print(os.getenv("MODEL_NAME"))