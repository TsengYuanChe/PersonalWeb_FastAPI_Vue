from repositories.common import read_json_with_timestamp

TIMELINE_EVENTS_FILE = "portfolio/timeline/events.json"


def read_timeline_events_with_timestamp():
    return read_json_with_timestamp(TIMELINE_EVENTS_FILE)
