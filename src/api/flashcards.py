from aqt.utils import showWarning
import requests

from ..config import Config


def request_flashcard_export() -> None:
    token = Config.get("token")
    if token is None:
        showWarning("Please login before exporting flashcards")
        return None

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
    )

    if response.status_code != 200 or not response.json().get("success"):
        error_msg = _extract_error(response)
        showWarning(f"Failed to export flashcards: {error_msg}")
        return None

    print(f"Flashcards export requested: {response.text}")


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
