# app/clients/financial_data.py

import os
import finnhub
import requests
from dotenv import load_dotenv

load_dotenv()

# --- Finnhub Client (for stocks and indices) ---
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

def get_index_quotes():
    """Fetches quotes for major indices from Finnhub."""
    # Using different tickers that are more likely to work with Finnhub's free plan
    indices = {'S&P 500': 'SPY', 'NASDAQ': 'QQQ', 'Dow Jones': 'DIA'}
    data = []
    for name, ticker in indices.items():
        try:
            quote = finnhub_client.quote(ticker)
            if quote.get('c') == 0: continue
            data.append({
                "name": name,
                "ticker": ticker,
                "price": quote.get('c'),
                "change": quote.get('d'),
                "change_percent": quote.get('dp')
            })
        except Exception as e:
            print(f"Error fetching Finnhub index {name}: {e}")
    return data

def get_batch_quotes(tickers: list[str]):
    """Fetches real-time quotes for a list of tickers from Finnhub."""
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
            print(f"Error fetching Finnhub quote for {ticker}: {e}")
    return quotes

def get_news_for_ticker(ticker: str):
    """Fetches the 3 most recent news articles for a specific ticker from Finnhub."""
    from datetime import datetime, timedelta
    today = datetime.now()
    one_week_ago = today - timedelta(days=7)
    news = []
    try:
        news_data = finnhub_client.company_news(ticker, _from=one_week_ago.strftime('%Y-%m-%d'), to=today.strftime('%Y-%m-%d'))
        news = [{
            "headline": item.get('headline'),
            "summary": item.get('summary'),
            "url": item.get('url'),
        } for item in news_data[:3]]
    except Exception as e:
        print(f"Error fetching Finnhub company news for {ticker}: {e}")
    return news


# --- Brave Client (for general market news) ---
def get_news_from_brave():
    """Fetches general market news using the Brave Search API."""
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        print("ERROR: BRAVE_API_KEY not found in environment.")
        return []

    url = "https://api.search.brave.com/res/v1/web/search"
    params = {'q': 'latest stock market news finance economy'}
    headers = {
        'Accept': 'application/json',
        'X-Subscription-Token': api_key
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('web', {}).get('results', [])
            
            # Reformat the data to match the standard format our frontend expects
            return [{
                "source": item.get('profile', {}).get('name', 'Brave Search'),
                "headline": item.get('title'),
                "summary": item.get('description'),
                "url": item.get('url'),
                "timestamp": item.get('page_age') # Brave provides an age string
            } for item in results]
        else:
            print(f"Brave API request failed with status {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"Error fetching from Brave API: {e}")
        return []