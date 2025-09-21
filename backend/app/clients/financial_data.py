# app/clients/financial_data.py
import os
import finnhub
from dotenv import load_dotenv

load_dotenv()

# Configure Finnhub client
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

def get_index_quotes():
    """Fetches quotes for major indices."""
    indices = {'S&P 500': '^GSPC', 'NASDAQ': '^IXIC', 'Dow Jones': '^DJI'}
    data = []
    for name, ticker in indices.items():
        try:
            # Note: Finnhub uses different symbols for indices. You might need to adjust or use a different provider.
            # For this example, we'll use common stock tickers to ensure it works.
            quote = finnhub_client.quote(ticker.replace('^', '')) # A hack for demo tickers
            if quote['c'] == 0: continue # Skip if no data
            data.append({
                "name": name,
                "ticker": ticker.replace('^', ''),
                "price": quote.get('c'),
                "change": quote.get('d'),
                "change_percent": quote.get('dp')
            })
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    return data

def get_latest_market_news():
    """Fetches general market news."""
    # Category: 'general', 'forex', 'crypto', 'merger'
    news = finnhub_client.general_news('general', min_id=0)
    # Return the top 10 articles in a clean format
    return [{
        "source": item.get('source'),
        "headline": item.get('headline'),
        "summary": item.get('summary'),
        "url": item.get('url'),
        "timestamp": item.get('datetime')
    } for item in news[:10]]

def get_batch_quotes(tickers: list[str]):
    """Fetches real-time quotes for a list of tickers."""
    quotes = []
    for ticker in tickers:
        try:
            quote = finnhub_client.quote(ticker)
            if quote.get('c') == 0: continue
            quotes.append({
                "ticker": ticker,
                "price": quote.get('c'),
                "change": quote.get('d'),
                "change_percent": quote.get('dp')
            })
        except Exception as e:
            print(f"Error fetching quote for {ticker}: {e}")
    return quotes

def get_news_for_ticker(ticker: str):
    """Fetches the 3 most recent news articles for a specific ticker."""
    # Finnhub requires a date range for company news
    from datetime import datetime, timedelta
    today = datetime.now()
    one_week_ago = today - timedelta(days=7)
    news = finnhub_client.company_news(ticker, _from=one_week_ago.strftime('%Y-%m-%d'), to=today.strftime('%Y-%m-%d'))
    return [{
        "headline": item.get('headline'),
        "summary": item.get('summary'),
        "url": item.get('url'),
    } for item in news[:3]]


# Add this function to app/clients/financial_data.py
import requests # Add to top imports

def get_news_from_newsapi():
    """Fetches general market news from NewsAPI."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return [] # Return empty list if no key

    url = "https://newsapi.org/v2/everything"
    params = {
        'q': 'finance OR market OR stocks OR economy', # A broader query
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            # Reformat the data to match what our frontend expects
            return [{
                "source": item.get('source', {}).get('name'),
                "headline": item.get('title'),
                "summary": item.get('description'),
                "url": item.get('url'),
                "timestamp": item.get('publishedAt') # Note: Different format than finnhub
            } for item in articles]
        return []
    except Exception as e:
        print(f"Error fetching from NewsAPI: {e}")
        return []