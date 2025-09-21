# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

import api_clients
import gemini_client

app = FastAPI()

# --- CORS Middleware (Essential for Frontend) ---
origins = ["http://localhost:3000", "http://localhost:5173"] # Add frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Request Bodies ---
class WatchlistRequest(BaseModel):
    tickers: List[str]

class AskRequest(BaseModel):
    question: str

# --- API Endpoints from Data Contract ---

@app.get("/api/dashboard/overview")
def get_dashboard_overview():
    """Endpoint for the 'Market Overview' on the dashboard."""
    index_data = api_clients.get_index_quotes()
    if not index_data:
        raise HTTPException(status_code=503, detail="Could not fetch index data.")
    return {"indices": index_data}

@app.get("/api/dashboard/analysis")
def get_dashboard_analysis():
    """Endpoint for the 'Recent Analysis' on the dashboard."""
    sectors = ["Technology", "Energy", "Healthcare"] # Sectors to analyze
    analysis_results = []
    
    for sector in sectors:
        articles = api_clients.get_news_by_category(sector)
        if articles:
            headlines = [article['title'] for article in articles]
            analysis = gemini_client.generate_sector_analysis(sector, headlines)
            analysis['sector'] = sector # Add sector name to the result
            analysis_results.append(analysis)
            
    return {"sector_analysis": analysis_results}

@app.get("/api/news")
async def get_news_with_sentiment():
    """Endpoint for the 'Market News' or 'Sentiment Analysis' pages."""
    articles = api_clients.get_latest_market_news(limit=6)
    if not articles:
        raise HTTPException(status_code=503, detail="Could not fetch market news.")
    
    processed_articles = []
    for article in articles:
        # Generate AI analysis for each article
        ai_analysis = gemini_client.analyze_news_article(
            article_title=article.get('title', ''),
            article_content=article.get('description', '') or article.get('content', '')
        )
        processed_articles.append({
            "source": article['source']['name'],
            "title": article['title'],
            "url": article['url'],
            "publishedAt": article['publishedAt'],
            "summary": ai_analysis.get('summary'),
            "sentiment": ai_analysis.get('sentiment')
        })
        
    return {"articles": processed_articles}

@app.post("/api/watchlist")
def get_watchlist_data(request: WatchlistRequest):
    """Endpoint for the 'Watchlist' page."""
    watchlist_data = []
    
    # Get all quotes in a batch
    quotes = api_clients.get_batch_quotes(request.tickers)

    for ticker in request.tickers:
        profile = api_clients.get_company_profile(ticker)
        company_name = profile.get('name', ticker) # Use real name for news search

        # Get news for this specific ticker
        articles = api_clients.get_news_for_ticker(ticker, company_name)
        headlines = [article['title'] for article in articles]

        # Generate the AI insight
        ai_insight = "No recent news to generate insight."
        if headlines:
            ai_insight = gemini_client.generate_watchlist_insight(company_name, headlines)

        watchlist_data.append({
            "ticker": ticker,
            "name": company_name,
            "quote": quotes.get(ticker),
            "ai_insight": ai_insight
        })
        
    return {"watchlist": watchlist_data}

# --- Additional Endpoints (AI Assistant) ---

@app.post("/api/ai-assistant/ask")
def post_ai_assistant_question(request: AskRequest):
    """Endpoint for the AI Assistant chat feature."""
    answer = gemini_client.ask_assistant(request.question)
    return {"answer": answer}