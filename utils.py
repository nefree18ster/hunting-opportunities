import os
from datetime import datetime

def read_stock_list(filepath="stocks.txt"):
    with open(filepath, "r") as file:
        return [line.strip() for line in file if line.strip()]

def log_result(msg, log_file):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        file.write(f"{timestamp} - {msg}\n")