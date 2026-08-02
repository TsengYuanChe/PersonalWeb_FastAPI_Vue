import json
import os
from datetime import datetime
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "data"


def read_json_with_timestamp(relative_path):
    filepath = DATA_DIR / Path(os.path.normpath(relative_path))

    with filepath.open("r", encoding="utf-8") as file:
        data = json.load(file)

    last_modified = filepath.stat().st_mtime
    updated_at = datetime.fromtimestamp(last_modified).strftime("%Y-%m-%d %H:%M:%S")
    return data, updated_at
