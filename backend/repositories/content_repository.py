import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def read_json_with_timestamp(filename):
    relative_path = os.path.normpath(filename)
    filepath = os.path.join(DATA_DIR, relative_path)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    last_modified = os.path.getmtime(filepath)
    updated_at = datetime.fromtimestamp(last_modified).strftime("%Y-%m-%d %H:%M:%S")
    return data, updated_at
