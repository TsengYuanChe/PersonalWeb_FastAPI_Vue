import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROJECT_FILES = {
    "mris": "portfolio/projects/mris.json",
    "personal-portfolio": "portfolio/projects/personal-portfolio.json",
    "mamatoya": "portfolio/projects/mamatoya.json",
}


def read_json_with_timestamp(filename):
    relative_path = os.path.normpath(filename)
    filepath = os.path.join(DATA_DIR, relative_path)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    last_modified = os.path.getmtime(filepath)
    updated_at = datetime.fromtimestamp(last_modified).strftime("%Y-%m-%d %H:%M:%S")
    return data, updated_at


def read_projects_with_timestamps():
    projects = []
    timestamps = []

    for filename in PROJECT_FILES.values():
        project, updated_at = read_json_with_timestamp(filename)
        projects.append(project)
        timestamps.append(updated_at)

    return projects, max(timestamps)


def read_project_with_timestamp(slug):
    filename = PROJECT_FILES.get(slug)
    if filename is None:
        return None, None

    return read_json_with_timestamp(filename)
