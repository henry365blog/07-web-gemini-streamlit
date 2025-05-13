import os
import json
from datetime import datetime

# 📂 Thư mục lưu lịch sử
HISTORY_DIR = "history"

def save_history_json(prompt, result, temperature, username="unknown"):
    """Lưu prompt và kết quả vào file JSON theo từng user, từng ngày."""

    if not prompt or not result:
        # Nếu thiếu prompt hoặc không có kết quả thì không lưu
        return

    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_dir = os.path.join(HISTORY_DIR, username)
    os.makedirs(user_dir, exist_ok=True)

    file_path = os.path.join(user_dir, f"{today}.json")

    # Đọc dữ liệu cũ (nếu có)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            # Nếu file bị lỗi format, reset file
            data = []
    else:
        data = []

    # Thêm bản ghi mới
    entry = {
        "timestamp": timestamp,
        "prompt": prompt,
        "result": result,
        "temperature": temperature,
    }
    data.append(entry)

    # Ghi lại vào file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_history_json(username, date_str):
    """Đọc lịch sử theo user và ngày."""

    file_path = os.path.join(HISTORY_DIR, username, f"{date_str}.json")

    if not os.path.exists(file_path):
        return []  # Không có file thì trả về list trống

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        return []  # File lỗi thì trả về list trống
