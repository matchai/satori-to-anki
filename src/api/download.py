import requests
from typing import Optional
from bs4 import BeautifulSoup

from ..config import Config


def get_latest_export_url() -> Optional[str]:
    """Get the URL of the latest completed export."""
    token = Config.get_token()
    if token is None:
        return None

    response = requests.get(
        "https://www.satorireader.com/review/exports",
        headers={
            "Cookie": f"SessionToken={token}",
        },
    )

    if response.status_code != 200:
        print(f"Failed to fetch exports: HTTP {response.status_code}")
        return None

    # Parse the HTML response
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all table rows except the header
    rows = soup.find_all("tr")[1:]  # Skip header row
    if not rows:
        print("No export rows found in response")
        return None

    # Find first completed export
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 2:
            print(f"Unexpected number of columns: {len(cols)}")
            continue

        status_col = cols[1]
        link = status_col.find("a")

        if not link:
            print("No download link found in status column")
            continue

        if "Complete" in status_col.text:
            return link["href"]

    print("No completed exports found")
    return None
