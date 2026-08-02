from repositories.about_repository import read_about_with_timestamp
from schemas.about import AboutData


def get_about_v1():
    data, updated_at = read_about_with_timestamp()
    validated = AboutData.model_validate(data)

    return {
        "data": validated.model_dump(mode="json"),
        "meta": {
            "updated_at": updated_at,
            "version": "v1",
        },
    }
