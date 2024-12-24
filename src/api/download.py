import os
import tempfile
import zipfile
from typing import Optional

import requests
from bs4 import BeautifulSoup

from ..config import Config


def get_latest_export_url() -> Optional[str]:
    """Get the URL of the latest completed export."""
    token = Config.get_token()
    if token is None:
        return None

    response = requests.get(
        "https://www.satorireader.com/review/exports",
        headers={"Cookie": f"SessionToken={token}"},
    )

    if response.status_code != 200:
        print(f"Failed to fetch exports: HTTP {response.status_code}")
        return None

    # Parse the HTML response
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the URL of the latest completed export
    completed_links = soup.find_all("a", string="Complete")
    return completed_links[0]["href"] if completed_links else None


def download_export_file() -> Optional[str]:
    """Downloads the latest export file and saves it to a temporary location."""
    url = get_latest_export_url()
    if not url or not (token := Config.get_token()):  # Use walrus operator
        return None

    response = requests.get(
        url,
        headers={"Cookie": f"SessionToken={token}"},
        stream=True,  # Add streaming for binary file
    )

    if response.status_code != 200:
        print(f"Failed to download export file: HTTP {response.status_code}")
        return None

    try:
        # Create temporary file for the zip
        with (
            tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as zip_temp,
            tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as csv_temp,
        ):
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    zip_temp.write(chunk)

            with zipfile.ZipFile(zip_temp.name, "r") as zip_ref:
                csv_filename = zip_ref.namelist()[0]
                with zip_ref.open(csv_filename) as zipped_file:
                    csv_temp.write(zipped_file.read())

            # Clean up the zip file
            os.unlink(zip_temp.name)
            return csv_temp.name

    except Exception as e:
        print(f"Failed to process export file: {e!s}")
        for temp_file in [zip_temp.name, csv_temp.name]:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        return None
