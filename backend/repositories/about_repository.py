from repositories.common import read_json_with_timestamp

ABOUT_FILE = "portfolio/about/about.json"


def read_about_with_timestamp():
    return read_json_with_timestamp(ABOUT_FILE)
