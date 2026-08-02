from repositories.content_repository import read_timeline_events_with_timestamp
from schemas.content import TimelineEventsData


def get_timeline_events_v1():
    data, updated_at = read_timeline_events_with_timestamp()
    validated = TimelineEventsData.model_validate(data)
    timeline_events = [
        event.model_dump(mode="json") for event in validated.timeline_events
    ]

    return {
        "data": {"timeline_events": timeline_events},
        "meta": {
            "updated_at": updated_at,
            "version": "v1",
        },
    }
