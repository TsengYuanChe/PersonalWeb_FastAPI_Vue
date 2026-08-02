from repositories.journey_repository import read_journey_items_with_timestamps
from schemas.journey import JourneyItem


def get_journey_v1():
    journey_items, updated_at = read_journey_items_with_timestamps()
    validated = [
        JourneyItem.model_validate(journey_item).model_dump(mode="json")
        for journey_item in journey_items
    ]
    validated.sort(key=lambda item: item.get("start_date", ""), reverse=True)

    return {
        "data": {"journey": validated},
        "meta": {
            "updated_at": updated_at,
            "version": "v1",
        },
    }
