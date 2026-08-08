from repositories.common import DATA_DIR, read_json_with_timestamp

PROJECT_DIR = "portfolio/projects"
EXCLUDED_PROJECT_FILES = {"sample.json"}
EXCLUDED_PROJECT_PREFIXES = (".", "_")


def _discover_project_files():
    project_dir = DATA_DIR / PROJECT_DIR
    return sorted(
        (
            filepath
            for filepath in project_dir.glob("*.json")
            if filepath.name not in EXCLUDED_PROJECT_FILES
            and not filepath.name.startswith(EXCLUDED_PROJECT_PREFIXES)
        ),
        key=lambda filepath: filepath.name.casefold(),
    )


def read_projects_with_timestamps():
    projects = []
    timestamps = []

    for filepath in _discover_project_files():
        relative_path = filepath.relative_to(DATA_DIR)
        project, updated_at = read_json_with_timestamp(relative_path)
        projects.append(project)
        timestamps.append(updated_at)

    projects.sort(
        key=lambda project: project.get("title", "").strip().casefold(),
        reverse=True,
    )
    return projects, max(timestamps) if timestamps else None


def read_project_with_timestamp(slug):
    for filepath in _discover_project_files():
        relative_path = filepath.relative_to(DATA_DIR)
        project, updated_at = read_json_with_timestamp(relative_path)
        if project.get("slug") == slug:
            return project, updated_at

    return None, None
