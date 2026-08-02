from repositories.experience_repository import read_experiences_with_timestamps
from schemas.experience import ExperienceItem


def get_experience_v1():
    experiences, updated_at = read_experiences_with_timestamps()
    validated = [
        ExperienceItem.model_validate(experience).model_dump(mode="json")
        for experience in experiences
    ]
    validated.sort(key=lambda item: item.get("start_date", ""), reverse=True)

    return {
        "data": {"experience": validated},
        "meta": {
            "updated_at": updated_at,
            "version": "v1",
        },
    }
