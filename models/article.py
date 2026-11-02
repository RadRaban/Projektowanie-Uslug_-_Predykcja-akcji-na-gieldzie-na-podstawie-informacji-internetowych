from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str
    source: str
    published_at: str | None = None
    url: str
    description: str | None = None

class NewsEvent(BaseModel):
    title: str
    summary: str
    category: str
    articles: list[Article]
    confirmed_facts: list[str] = Field(default_factory=list)
    unclear_information: list[str] = Field(default_factory=list)

class NewsAnalysis(BaseModel):
    events: list[NewsEvent]