import dotenv
from agno.agent import Agent
from agno.models.xai import xAI

from models.article import NewsAnalysis

dotenv.load_dotenv()

news_agent = Agent(
    name="NewsAPIAgent",
    model=xAI(id="grok-4.20"),
    output_schema=NewsAnalysis,
    instructions=[
        "Analizuj wyłącznie artykuły przekazane przez aplikację.",
        "Nie wykonuj wyszukiwań ani nie pobieraj dodatkowych danych.",
        "Grupuj artykuły dotyczące tego samego wydarzenia.",
        "Porównuj relacje różnych źródeł.",
        "Nie traktuj samego dopasowania słowa kluczowego jako "
        "dowodu, że artykuły opisują to samo wydarzenie.",
        "Nie wymyślaj faktów, źródeł ani adresów URL.",
        "Wskazuj sprzeczności i informacje, których nie da się "
        "ustalić na podstawie dostarczonych artykułów.",
        "Odpowiadaj po polsku.",
    ],
    debug_mode=True,
)