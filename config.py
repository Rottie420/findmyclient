from dotenv import load_dotenv
import os

load_dotenv()


# ---------- Load environment variables ----------
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
PLACES_API_KEY = os.getenv("PLACES_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")


# ---------- Scraper Configurations ----------
PATHS = ["/", "/contact", "/contact-us", "/about",
    "/team", "/support", "/careers", "/privacy",
    "/terms", "/home", "/index", "/welcome", "/services",
    "/products", "/solutions", "/blog", "/news", "/events",
    "/about-us", "/our-team", "/help", "/customer-support",
    "/jobs", "/work-with-us", "/partners", "/partnerships",
    ]

SITEMAP_PATHS = [
    "/sitemap.xml",
    "/sitemap_index.xml",
    "/sitemap-index.xml",
]

BLOCKED_PREFIXES = {"user", "test", "example", "privacy"}

BLOCKED_DOMAINS = {"domain.com", "example.com", "test.com",
                "email.com",
            }
