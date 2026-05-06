from google import genai
from utils.utils import regex_filter
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME


client = genai.Client(api_key=GEMINI_API_KEY)


# ---------- Gemini Email Extraction ----------
def gemini_extract(text):
    try:
        prompt = f"""
        Extract all business email addresses from the following website content.

        Rules:
        - Return ONLY emails
        - One email per line
        - No explanation
        - Ignore fake/example emails

        Website Content:
        {text[:12000]}
        """

        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
        )

        found = regex_filter(response.text)

        return found

    except Exception:
        return set()
    