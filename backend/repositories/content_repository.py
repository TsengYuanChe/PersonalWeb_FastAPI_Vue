import json
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROJECT_FILES = {
    "mris": "portfolio/projects/mris.json",
    "personal-portfolio": "portfolio/projects/personal-portfolio.json",
    "mamatoya": "portfolio/projects/mamatoya.json",
}
EXPERIENCE_DIR = "portfolio/experience"


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


def read_experiences_with_timestamps():
    experience_dir = Path(DATA_DIR) / EXPERIENCE_DIR
    experiences = []
    timestamps = []

    for filepath in experience_dir.glob("*.json"):
        relative_path = filepath.relative_to(DATA_DIR).as_posix()
        experience, updated_at = read_json_with_timestamp(relative_path)
        experiences.append(experience)
        timestamps.append(updated_at)

    experiences.sort(key=lambda item: item.get("start_date", ""), reverse=True)
    return experiences, max(timestamps) if timestamps else None
