from datetime import datetime, timedelta, timezone

import requests
from aqt.utils import showWarning

from src.config import Config


def request_flashcard_export() -> None:
    # Only request flashcards every 30+ minutes
    last_export_time = Config.get_last_export_time()
    # Only request flashcards every 150 minutes, preventing the 10 times in the
    # 24 hour limit
    if last_export_time is not None and datetime.now(
        tz=timezone.utc,
    ) - last_export_time < timedelta(
        minutes=150,
    ):
        print(f"Flashcards exported {last_export_time}, skipping")
        return

    token = Config.get_token()
    if token is None:
        showWarning("Please login before exporting flashcards")
        return

    response = requests.post(
        "https://www.satorireader.com/api/studylist/export",
        headers={
            "Cookie": f"SessionToken={token}",
        },
        json={
            "format": "csv",
            "whenCreatedRangeStartLocal": "2000-01-01T00:00:00.000Z",
            "whenCreatedRangeEndLocal": "2099-01-01T00:00:00.000Z",
            "cardTypes": ["JE"],
            "furiganaNotationFormat": "Anki",
        },
        timeout=10,
    )

    if did_hit_rate_limit(response):
        Config.set_last_export_time(datetime.now(tz=timezone.utc))
        print("Hit rate limit, skipping export")
        return

    if response.status_code == requests.codes.ok or not response.json().get("success"):
        error_msg = _extract_error(response)
        showWarning(f"Failed to export flashcards: {error_msg}")
        return

    print(f"Flashcards export requested: {response.text}")
    Config.set_last_export_time(datetime.now(tz=timezone.utc))


def _extract_error(response: requests.Response) -> str:
    try:
        data = response.json()
        return (
            data.get("exception")
            or data.get("message")
            or f"Status code: {response.status_code}"
        )
    except requests.JSONDecodeError:
        return f"Status code: {response.status_code}"


def did_hit_rate_limit(response: requests.Response) -> bool:
    return (
        response.status_code == requests.codes.ok
        and response.json().get("success") is False
    )
