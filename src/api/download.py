import os
import tempfile
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


def download_export_file() -> Optional[str]:
    """
    Downloads the latest export file and saves it to a temporary location.
    Returns the file path if successful, None otherwise.
    """
    url = get_latest_export_url()
    if url is None:
        return None

    token = Config.get_token()
    if token is None:
        return None

    response = requests.get(
        url,
        headers={
            "Cookie": f"SessionToken={token}",
        },
        stream=True  # Add streaming for binary file
    )

    if response.status_code != 200:
        print(f"Failed to download export file: HTTP {response.status_code}")
        return None

    try:
        # Create temporary file for the zip
        zip_temp = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
        with zip_temp as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Create temporary file for the CSV
        csv_temp = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        
        # Extract the CSV from the zip
        import zipfile
        with zipfile.ZipFile(zip_temp.name, 'r') as zip_ref:
            # Get the first file in the zip (assuming there's only one)
            csv_filename = zip_ref.namelist()[0]
            with zip_ref.open(csv_filename) as zipped_file:
                csv_temp.write(zipped_file.read())

        # Clean up the zip file
        os.unlink(zip_temp.name)
        
        return csv_temp.name
    except Exception as e:
        print(f"Failed to process export file: {str(e)}")
        # Clean up any temporary files
        if 'zip_temp' in locals() and os.path.exists(zip_temp.name):
            os.unlink(zip_temp.name)
        if 'csv_temp' in locals() and os.path.exists(csv_temp.name):
            os.unlink(csv_temp.name)
        return None
