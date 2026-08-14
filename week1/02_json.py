import json

model_result = {
    "model": "Qwen",
    "response": "Azərbaycanın paytaxtı Bakıdır.",
    "correct": True
}

json_string = json.dumps(model_result, ensure_ascii=False, indent=2)
print(json_string)

parsed = json.loads(json_string)
print(parsed['response'])

with open("week1/output/result.json", "w", encoding="utf-8") as f:
    json.dump(model_result, f, ensure_ascii=False, indent=2)