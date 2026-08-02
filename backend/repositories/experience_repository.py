from repositories.common import DATA_DIR, read_json_with_timestamp

EXPERIENCE_DIR = "portfolio/experience"


def read_experiences_with_timestamps():
    experience_dir = DATA_DIR / EXPERIENCE_DIR
    experiences = []
    timestamps = []

    for filepath in experience_dir.glob("*.json"):
        relative_path = filepath.relative_to(DATA_DIR)
        experience, updated_at = read_json_with_timestamp(relative_path)
        experiences.append(experience)
        timestamps.append(updated_at)

    experiences.sort(key=lambda item: item.get("start_date", ""), reverse=True)
    return experiences, max(timestamps) if timestamps else None
