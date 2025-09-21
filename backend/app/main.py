# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .clients import financial_data
from . import llm_services

# --- Pydantic Models for Request Bodies ---
class WatchlistRequest(BaseModel):
    tickers: list[str]

class AskRequest(BaseModel):
    query: str

# --- FastAPI App Initialization ---
app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    # Add your frontend's deployed URL here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"status": "FinanceAI Backend is running"}

@app.get("/api/dashboard/overview")
def get_dashboard_overview():
    """Endpoint for the dashboard's market overview card."""
    return financial_data.get_index_quotes()

@app.get("/api/news")
def get_market_news():
    """Endpoint for the main market news page, powered by Brave."""
    articles = financial_data.get_news_from_brave()
    for article in articles:
        # Combine headline and summary for more accurate sentiment analysis
        text_to_analyze = f"{article.get('headline', '')}. {article.get('summary', '')}"
        article['sentiment'] = llm_services.classify_sentiment(text_to_analyze)
    return articles

@app.post("/api/watchlist")
def get_watchlist_data(request: WatchlistRequest):
    """Endpoint for the user's watchlist."""
    quotes = financial_data.get_batch_quotes(request.tickers)
    for quote in quotes:
        news = financial_data.get_news_for_ticker(quote['ticker'])
        quote['news'] = news
        quote['ai_insight'] = llm_services.get_ai_insight_for_ticker(quote['ticker'], news)
    return quotes

@app.post("/api/ask")
def ask_ai_assistant(request: AskRequest):
    """Endpoint for the AI financial assistant chat."""
    answer = llm_services.answer_question(request.query)
    return {"answer": answer}