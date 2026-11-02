import json

from models.article import NewsAnalysis
from agents.news_agent import news_agent
from tools.news_api import search_newsapi
from tools.news_api import search_eventregistry


def get_news(keyword: str, limit: int = 5, language: str = "en") -> NewsAnalysis:
    newsapi_data = json.loads(
        search_newsapi(
            query=keyword,
            language=language,
            page_size=limit,
        )
    )

    eventregistry_data = json.loads(
        search_eventregistry(
            query=keyword,
            page_size=limit,
        )
    )

    articles = newsapi_data + eventregistry_data
    print(articles)

    unique_articles = []
    seen_urls = set()

    for article in articles:
        url = (article.get("url") or "").strip()

        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        unique_articles.append(article)

    unique_articles = unique_articles[:limit]

    if not unique_articles:
        return NewsAnalysis(events=[])

    articles_json = json.dumps(unique_articles, ensure_ascii=False)

    print(articles_json)

    prompt = f"""
    Przeanalizuj artykuły znalezione dla tematu: {keyword}.

    Dane zostały pobrane przez aplikację z NewsAPI i Event Registry.
    Analizuj wyłącznie poniższe artykuły.
    Nie wykonuj dodatkowych wyszukiwań.

    {articles_json}
    """

    response = news_agent.run(prompt)
    return response.content

print(get_news("AI", limit=30, language="en"))