import re
import codecs
import dns.resolver
from config import BLOCKED_PREFIXES, BLOCKED_DOMAINS


# ---------- Regex Filter ----------
def regex_filter(text):

    text = codecs.decode(text, "unicode_escape")

    emails = re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text,
    )

    cleaned = set()

    for email in emails:

        email = email.lower()
        local, domain = email.split("@", 1)

        # block fake/test emails
        if local in BLOCKED_PREFIXES:
            continue

        if domain in BLOCKED_DOMAINS:
            continue

        # block hex/hash-like strings
        if re.fullmatch(r"[a-f0-9]{16,}", local):
            continue

        # remove extremely long garbage domains
        if len(domain) > 253:
            continue

        # basic domain sanity
        if "." not in domain:
            continue

        cleaned.add(email)

    return cleaned


# ---------- Email validation ----------
def is_valid_domain(email):
    domain = email.split("@")[-1]

    try:
        dns.resolver.resolve(domain, "MX")
        return True
    except Exception:
        return False