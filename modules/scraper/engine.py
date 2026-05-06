from concurrent.futures import ThreadPoolExecutor
from modules.scraper.crawler import crawl_website
from modules.scraper.places import get_places


# ---------- Main Scraper Function ----------
def run_scraper(search_query):
    result = get_places(search_query, max_pages=60)
    emails_found = set()
    places = result.get("places", [])
    websites = []

    for place in places:

        website = place.get("websiteUri")

        if website:
            websites.append(website)

    with ThreadPoolExecutor(max_workers=10) as executor:

        results = list(
            executor.map(
                crawl_website,
                websites,
            )
        )

    for found_emails in results:
        emails_found.update(found_emails)

    return {
        "query": search_query,
        "total_emails_found": len(emails_found),
        "emails": sorted(list(emails_found)),
    }