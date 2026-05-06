from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from modules.scraper.emails import extract_emails
from config import PATHS, SITEMAP_PATHS
import requests


## ---------- Get sitemap from robots.txt ----------
def get_sitemap_from_robots(base_url):
    robots_url = urljoin(base_url, "/robots.txt")

    try:
        res = requests.get(robots_url, timeout=1)

        if res.status_code != 200:
            return []

        sitemaps = []

        for line in res.text.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_url = line.split(":", 1)[1].strip()
                sitemaps.append(sitemap_url)

        return sitemaps

    except Exception:
        return []
    

# ---------- Get sitemap URLs ----------
def get_sitemap_urls(base_url):

    urls = set()

    # ---------- 1. FIRST: robots.txt ----------
    sitemap_sources = get_sitemap_from_robots(base_url)

    # ---------- 2. fallback to known paths ----------
    if not sitemap_sources:
        sitemap_sources = [
            urljoin(base_url, path)
            for path in SITEMAP_PATHS
        ]

    # ---------- 3. try each sitemap ----------
    for sitemap_url in sitemap_sources:

        try:
            response = requests.get(sitemap_url, timeout=1)

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "xml")

            for loc in soup.find_all("loc"):
                url = loc.text.strip().lower()

                if any(path in url for path in PATHS):
                    urls.add(url)

            if urls:
                print(f"[+] Sitemap found: {sitemap_url}")
                return list(urls)

        except Exception:
            continue

    return []


# ---------- Crawl website ----------
def crawl_website(website_url):

    emails = set()

    if not website_url.startswith("http"):
        website_url = "https://" + website_url

    parsed = urlparse(website_url)

    base_url = f"{parsed.scheme}://{parsed.netloc}"

    # ---------- Sitemap First ----------
    urls_to_crawl = get_sitemap_urls(base_url)

    # ---------- Fallback ----------
    if not urls_to_crawl:

        urls_to_crawl = [
            urljoin(base_url, path)
            for path in PATHS
        ]

    with ThreadPoolExecutor(max_workers=5) as executor:

        results = list(
            executor.map(
                extract_emails,
                urls_to_crawl,
            )
        )

    for result in results:
        emails.update(result)

    return emails