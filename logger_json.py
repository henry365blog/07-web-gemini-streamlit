import json
from datetime import datetime
import os

def save_history_json(prompt: str, response: str, temperature: float = 0.7, username="default", folder="logs"):
    os.makedirs(folder, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    safe_username = username.replace(" ", "_").lower()
    filename = f"{folder}/{safe_username}_{today}.json"

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt,
        "response": response,
        "temperature": temperature,
        "user": username
    }

    data = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

    data.append(record)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
