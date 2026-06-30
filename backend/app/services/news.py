import requests
import os
from dotenv import load_dotenv

# Load .env file for local development (won't affect Render environment variables)
load_dotenv()

# Read NEWS_API_KEY from environment - will use Render's env vars in production
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(query: str = "latest", page_size: int = 10) -> dict:
    try:
        # Get the API key - check if it exists
        api_key = os.getenv("NEWS_API_KEY")
        
        if not api_key:
            return {
                "success": False, 
                "error": "NEWS_API_KEY environment variable is not set",
                "articles": []
            }
        
        params = {
            "apiKey": api_key,
            "q": query if query != "latest" else "world OR kenya OR africa OR technology OR health OR sports OR business",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
        }
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = []
        for article in data.get("articles", []):
            if article.get("title") and article.get("description"):
                articles.append({
                    "title":       article.get("title", ""),
                    "description": article.get("description", ""),
                    "url":         article.get("url", ""),
                    "source":      article.get("source", {}).get("name", ""),
                    "publishedAt": article.get("publishedAt", ""),
                    "content":     f"{article.get('title','')} {article.get('description','')} {article.get('content','') or ''}"
                })

        return {"success": True, "articles": articles, "total": len(articles)}

    except Exception as e:
        return {"success": False, "error": str(e), "articles": []}
