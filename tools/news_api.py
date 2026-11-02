import os
import json
import httpx
import dotenv

dotenv.load_dotenv()

def search_newsapi(query: str, language: str = "en", page_size: int = 10) -> str:
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        raise ValueError("NEWS_API_KEY not set")

    page_size = max(1, min(page_size, 5))

    response = httpx.get(
        "https://newsapi.org/v2/everything",
    params={
        "q": query,
        "language": language,
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "apiKey": api_key
    },
    timeout=20
    )

    response.raise_for_status()
    data = response.json()

    if data.get("status") != "ok":
        raise RuntimeError(f"NewsAPI error: {data}")

    articles = []

    for item in data.get("articles", []):
        articles.append({
            "source_api": "newsapi",
            "source": (item.get("source") or {}).get("name"),
            "title": item.get("title"),
            "description": (item.get("description") or "")[:200],
            "url": item.get("url"),
            "published_at": item.get("publishedAt"),
            "author": item.get("author"),
            "language": language,
            "categories": [],
        })

    return json.dumps(articles, ensure_ascii=False)

def search_eventregistry(query: str, page_size: int = 10) -> str:
    api_key = os.getenv("EVENT_REGISTRY_API_KEY")

    if not api_key:
        raise ValueError("EVENT_REGISTRY_API_KEY not set")

    page_size = max(1, min(page_size, 5))

    response = httpx.get(
        "https://eventregistry.org/api/v1/article/getArticles",
        params={
            "keyword": query,
            "articlesPage": 1,
            "articlesCount": page_size,
            "articlesSortBy": "date",
            "articlesSortByAsc": "false",
            "resultType": "articles",
            "apiKey": api_key,
        },
        timeout=20,
    )

    response.raise_for_status()
    data = response.json()

    article_data = data.get("articles") or {}
    results = (article_data.get("results") or [])[:30]

    articles = []

    for item in results:
        source = item.get("source") or {}
        authors = item.get("authors") or []

        articles.append({
            "source_api": "eventregistry",
            "source": source.get("title"),
            "title": (item.get("title") or "")[:200],
            "description": (item.get("body") or "")[:1000],
            "url": item.get("url"),
            "published_at": item.get("dateTimePub") or item.get("dateTime"),
            "author": authors[0].get("name") if authors else None,
            "language": item.get("lang"),
            "categories": [
                category.get("label")
                for category in (item.get("categories") or [])
                if category.get("label")
            ],
        })

    return json.dumps(articles, ensure_ascii=False)
