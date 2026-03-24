from repositories.content_repository import read_json_with_timestamp


def get_legacy_content(filename):
    data, updated_at = read_json_with_timestamp(filename)
    data["updated_at"] = updated_at
    return data


def get_v1_content(filename):
    data, updated_at = read_json_with_timestamp(filename)
    return {
        "data": data,
        "meta": {
            "updated_at": updated_at,
            "version": "v1",
        },
    }


def get_about_legacy():
    return get_legacy_content("profile/about.json")


def get_experience_legacy():
    return get_legacy_content("profile/experience.json")


def get_projects_legacy():
    return get_legacy_content("portfolio/projects.json")


def get_about_v1():
    return get_v1_content("profile/about.json")


def get_experience_v1():
    return get_v1_content("profile/experience.json")


def get_projects_v1():
    return get_v1_content("portfolio/projects.json")
