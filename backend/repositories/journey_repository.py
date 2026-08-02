from repositories.common import DATA_DIR, read_json_with_timestamp

JOURNEY_DIR = "portfolio/journey"


def read_journey_items_with_timestamps():
    journey_dir = DATA_DIR / JOURNEY_DIR
    journey_items = []
    timestamps = []

    for filepath in journey_dir.glob("*.json"):
        relative_path = filepath.relative_to(DATA_DIR)
        journey_item, updated_at = read_json_with_timestamp(relative_path)
        journey_items.append(journey_item)
        timestamps.append(updated_at)

    journey_items.sort(key=lambda item: item.get("start_date", ""), reverse=True)
    return journey_items, max(timestamps) if timestamps else None
