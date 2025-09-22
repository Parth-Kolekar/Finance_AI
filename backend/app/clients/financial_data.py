# app/clients/financial_data.py

import os
import finnhub
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from twelvedata import TDClient
import time

load_dotenv()

# --- API Clients ---
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
td_client = TDClient(apikey=os.getenv("TWELVE_DATA_API_KEY"))

def get_crypto_data(symbols: list):
    """Fetches real-time quotes and 30-day history for a list of crypto symbols."""
    data = []
    for symbol in symbols:
        try:
            quote_data = td_client.quote(symbol=symbol).as_json()
            
            ts = td_client.time_series(
                symbol=symbol,
                interval="1day",
                outputsize=30
            )
            history = ts.as_json()[::-1]

            data.append({
                "name": quote_data.get('name'),
                "symbol": quote_data.get('symbol'),
                "price": float(quote_data.get('close', 0)),
                "change": float(quote_data.get('change', 0)),
                "percent_change": float(quote_data.get('percent_change', 0)),
                "history": [float(item['close']) for item in history]
            })

            time.sleep(8)

        except Exception as e:
            print(f"Error fetching Twelve Data for crypto '{symbol}': {e}")
            # If we hit an error (like a rate limit), just skip to the next symbol
            continue
            
    return data

def get_stock_candles(ticker: str, interval: str, outputsize: int):
    """Fetches historical stock data using Twelve Data."""
    try:
        ts = td_client.time_series(symbol=ticker, interval=interval, outputsize=outputsize)
        data = ts.as_json()[::-1]
        return {
            "dates": [item['datetime'] for item in data],
            "prices": [float(item['close']) for item in data]
        }
    except Exception as e:
        print(f"Error fetching Twelve Data candles for {ticker}: {e}")
        return None

def get_single_quote(ticker: str):
    """Fetches a single real-time quote for a specific ticker from Finnhub."""
    try:
        quote = finnhub_client.quote(ticker)
        if quote.get('c') == 0: return None
        return {
            "price": quote.get('c'),
            "change": quote.get('d'),
            "change_percent": quote.get('dp')
        }
    except Exception as e:
        print(f"Error fetching Finnhub quote for {ticker}: {e}")
        return None

def get_index_quotes():
    """Fetches quotes for major indices from Finnhub."""
    indices = {'S&P 500': 'SPY', 'NASDAQ': 'QQQ', 'Dow Jones': 'DIA'}
    data = []
    for name, ticker in indices.items():
        try:
            quote = finnhub_client.quote(ticker)
            if quote.get('c') == 0: continue
            data.append({
                "name": name, "ticker": ticker, "price": quote.get('c'),
                "change": quote.get('d'), "change_percent": quote.get('dp')
            })
        except Exception as e:
            print(f"Error fetching Finnhub index {name}: {e}")
    return data

def get_batch_quotes(tickers: list[str]):
    """Fetches real-time quotes and company names for a list of tickers from Finnhub."""
    quotes = []
    for ticker in tickers:
        try:
            quote = finnhub_client.quote(ticker)
            if quote.get('c') == 0: continue
            profile = finnhub_client.company_profile2(symbol=ticker)
            company_name = profile.get('name') if profile else ticker
            quotes.append({
                "ticker": ticker, "name": company_name, "price": quote.get('c'),
                "change": quote.get('d'), "change_percent": quote.get('dp')
            })
        except Exception as e:
            print(f"Error fetching Finnhub quote for {ticker}: {e}")
    return quotes

def get_news_for_ticker(ticker: str):
    """Fetches the 3 most recent news articles for a specific ticker from Finnhub."""
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

def get_news_from_brave():
    """Fetches general market news using the Brave Search API's news endpoint."""
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        print("ERROR: BRAVE_API_KEY not found in environment.")
        return []
    url = "https://api.search.brave.com/res/v1/news/search"
    params = {'q': 'latest stock market news finance economy'}
    headers = {'Accept': 'application/json', 'X-Subscription-Token': api_key}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            return [{
                "source": item.get('meta_url', {}).get('hostname', 'Brave News'),
                "headline": item.get('title'),
                "summary": item.get('description', 'No summary available.'),
                "url": item.get('url'),
                "timestamp": item.get('page_age')
            } for item in results]
        else:
            print(f"Brave API request failed with status {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"Error fetching from Brave API: {e}")
        return []