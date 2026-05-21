import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def scrape_article(url: str) -> dict:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts, styles, nav, footer
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Try to get title
        title = ""
        if soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)
        elif soup.find("title"):
            title = soup.find("title").get_text(strip=True)

        # Extract paragraphs
        paragraphs = soup.find_all("p")
        body = " ".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 40)

        content = f"{title} {body}".strip()

        if len(content) < 100:
            return {"success": False, "error": "Could not extract enough content from URL", "content": ""}

        return {"success": True, "content": content, "title": title}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out", "content": ""}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Could not connect to URL", "content": ""}
    except Exception as e:
        return {"success": False, "error": str(e), "content": ""}