# app/llm_services.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def get_sentiment_and_summary_for_news(articles: list[dict]):
    # [Implementation of this function]...
    pass # We will build this out

def get_ai_insight_for_ticker(news_headlines: list[str]):
    # [Implementation of this function]...
    pass # We will build this out

def answer_question(query: str):
    prompt = f"You are an expert financial analyst. Answer the following question clearly and concisely: {query}"
    response = model.generate_content(prompt)
    return response.text

def classify_sentiment(headline: str):
    """Classifies a headline as POSITIVE, NEGATIVE, or NEUTRAL."""
    prompt = f"""
    Analyze the sentiment of the following financial news headline.
    Classify it as strictly one of: POSITIVE, NEGATIVE, or NEUTRAL.
    Return only the single word classification.

    Headline: "{headline}"
    Sentiment:
    """
    response = model.generate_content(prompt)
    # Clean up the response
    sentiment = response.text.strip().upper()
    if sentiment in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
        return sentiment
    return "NEUTRAL" # Default fallback


# app/llm_services.py
def get_ai_insight_for_ticker(ticker: str, news_items: list[dict]):
    headlines = "\n".join([f"- {item['headline']}" for item in news_items])
    prompt = f"""
    Act as a financial analyst. Based on these recent headlines for {ticker}, write a single, concise sentence (max 20 words) for an "AI Insight" section on a stock watchlist.

    Headlines:
    {headlines}

    AI Insight:
    """
    response = model.generate_content(prompt)
    return response.text.strip()