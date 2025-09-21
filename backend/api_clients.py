# api_clients.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# --- Functions from the Data Contract ---

def get_index_quotes() -> list[dict]:
    """
    Fetches quotes for major indices like S&P 500 and NIFTY 50.
    Matches: /api/dashboard/overview
    """
    indices = {
        "S&P 500": "^GSPC",
        "NIFTY 50": "^NSEI",
        "Dow Jones": "^DJI",
        "NASDAQ": "^IXIC"
    }
    index_data = []
    
    for name, symbol in indices.items():
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            index_data.append({
                "name": name,
                "symbol": symbol.replace('^',''), # Cleaner symbol for UI
                "price": data.get('c'),
                "change": data.get('d'),
                "change_percent": data.get('dp')
            })
        except Exception as e:
            print(f"Error fetching index {name}: {e}")
            continue # Skip if an index fails
            
    return index_data

def get_news_by_category(category: str, limit: int = 3) -> list[dict]:
    """
    Fetches top news articles for a specific sector (e.g., "Technology").
    Matches: /api/dashboard/analysis
    """
    query = f'"{category} sector" stocks'
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=relevancy&apiKey={NEWS_API_KEY}"
        res = requests.get(url)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        return articles[:limit]
    except Exception as e:
        print(f"Error fetching news for category {category}: {e}")
        return []

def get_latest_market_news(limit: int = 10) -> list[dict]:
    """
    Fetches general, latest market news.
    Matches: /api/news
    """
    query = '"stock market" OR "finance" OR "economy"'
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        res = requests.get(url)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        return articles[:limit]
    except Exception as e:
        print(f"Error fetching latest market news: {e}")
        return []

def get_batch_quotes(tickers: list[str]) -> dict:
    """
    Fetches real-time quotes for a list of tickers.
    Helper for: /api/watchlist
    """
    quotes = {}
    for ticker in tickers:
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={ticker.upper()}&token={FINNHUB_API_KEY}"
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            quotes[ticker] = {
                "price": data.get('c'),
                "change": data.get('d'),
                "change_percent": data.get('dp')
            }
        except Exception as e:
            print(f"Error fetching quote for {ticker}: {e}")
            quotes[ticker] = {} # Add empty dict on failure
    return quotes

def get_news_for_ticker(ticker: str, company_name: str, limit: int = 3) -> list[dict]:
    """
    Fetches the 3 most recent news articles for a specific ticker.
    Helper for: /api/watchlist
    """
    # Searching by company name gives better news results than the ticker
    query = f'"{company_name}" OR "{ticker}"'
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        res = requests.get(url)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        return articles[:limit]
    except Exception as e:
        print(f"Error fetching news for ticker {ticker}: {e}")
        return []

# Placeholder for company profile data needed for watchlist news search
def get_company_profile(ticker: str) -> dict:
    try:
        url = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={FINNHUB_API_KEY}"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error fetching profile for {ticker}: {e}")
        return {}