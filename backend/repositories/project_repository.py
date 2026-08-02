from repositories.common import read_json_with_timestamp

PROJECT_DIR = "portfolio/projects"
PROJECT_FILES = {
    "mris": f"{PROJECT_DIR}/mris.json",
    "personal-portfolio": f"{PROJECT_DIR}/personal-portfolio.json",
    "mamatoya": f"{PROJECT_DIR}/mamatoya.json",
}


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
