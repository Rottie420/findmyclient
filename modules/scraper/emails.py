import requests
from utils.utils import regex_filter, is_valid_domain
from modules.scraper.gemini import gemini_extract
from bs4 import BeautifulSoup


# ---------- Extract emails from URL ----------
def extract_emails(url):
    emails = set()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

        if response.status_code != 200:
            return emails

        text = response.text

        emails.update(regex_filter(text))

        soup = BeautifulSoup(text, "html.parser")

        visible_text = soup.get_text(
            separator=" ",
            strip=True,
        )

        emails.update(gemini_extract(visible_text))

        validated = set()

        for email in emails:
            email = email.lower()

            if is_valid_domain(email):
                validated.add(email)

        return validated

    except requests.RequestException:
        return emails