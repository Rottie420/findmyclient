import requests
import time
from config import PLACES_API_KEY

session = requests.Session()

def get_places(search_query, max_pages=60):
    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": PLACES_API_KEY,
        "X-Goog-FieldMask": "places.websiteUri,places.internationalPhoneNumber,nextPageToken",
    }

    all_places = []
    page_token = None

    for _ in range(max_pages):
        payload = {"textQuery": search_query}

        if page_token:
            payload["pageToken"] = page_token

        res = session.post(url, headers=headers, json=payload)

        if res.status_code != 200:
            break

        data = res.json()

        all_places.extend(data.get("places", []))
        page_token = data.get("nextPageToken")

        if not page_token:
            break

        time.sleep(0.5)
        
    return {"places": all_places}