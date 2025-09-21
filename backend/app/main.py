# app/main.py
# At top of app/main.py
from pydantic import BaseModel

class WatchlistRequest(BaseModel):
    tickers: list[str]


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .clients import financial_data
from . import llm_services

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:3000",  # For local React development
    # "https://your-frontend-deployment-url.vercel.app", # Person A's Vercel URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "FinanceAI Backend"}

# in app/main.py

@app.get("/api/news")
def get_market_news():
    # OLD way using Finnhub:
    # articles = financial_data.get_latest_market_news()

    # NEW way using NewsAPI:
    articles = financial_data.get_news_from_newsapi()

    # The sentiment analysis part remains the same
    for article in articles:
        article['sentiment'] = llm_services.classify_sentiment(article['headline'])
    return articles

@app.get("/api/dashboard/overview")
def get_dashboard_overview():
    """
    Endpoint to get the market overview data for the dashboard indices.
    """
    index_data = financial_data.get_index_quotes()
    return index_data


# app/main.py
@app.post("/api/watchlist")
def get_watchlist_data(request: WatchlistRequest):
    quotes = financial_data.get_batch_quotes(request.tickers)
    # In a real app, you'd merge this data more robustly.
    for quote in quotes:
        news = financial_data.get_news_for_ticker(quote['ticker'])
        quote['news'] = news
        if news:
            quote['ai_insight'] = llm_services.get_ai_insight_for_ticker(quote['ticker'], news)
        else:
            quote['ai_insight'] = f"No recent news found for {quote['ticker']}."
    return quotes


# app/main.py
class AskRequest(BaseModel):
    query: str

@app.post("/api/ask")
def ask_ai_assistant(request: AskRequest):
    answer = llm_services.answer_question(request.query)
    return {"answer": answer}