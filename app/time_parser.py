import dateparser
from datetime import datetime

def parse_time(text: str):
    parsed = dateparser.parse(
        text,
        settings={"PREFER_DATES_FROM": "future"}
    )

    if not parsed:
        return None

    return parsed.strftime("%Y-%m-%d %H:%M:%S")
