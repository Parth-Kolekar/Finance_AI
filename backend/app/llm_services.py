# app/llm_services.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

def classify_sentiment(headline: str):
    """Classifies a headline as POSITIVE, NEGATIVE, or NEUTRAL."""
    if not headline:
        return "NEUTRAL"
    try:
        prompt = f"""
        Analyze the sentiment of the following financial news headline.
        Classify it as strictly one of: POSITIVE, NEGATIVE, or NEUTRAL.
        Return only the single word classification.

        Headline: "{headline}"
        Sentiment:
        """
        response = model.generate_content(prompt)
        sentiment = response.text.strip().upper()
        if sentiment in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
            return sentiment
        return "NEUTRAL"
    except Exception as e:
        print(f"Error classifying sentiment: {e}")
        return "NEUTRAL"

def get_ai_insight_for_ticker(ticker: str, news_items: list[dict]):
    """Generates a concise AI insight based on news headlines."""
    if not news_items:
        return f"No recent news found for {ticker}."
    
    headlines = "\n".join([f"- {item['headline']}" for item in news_items if item.get('headline')])
    if not headlines:
        return f"No recent news headlines found for {ticker}."

    try:
        prompt = f"""
        Act as a financial analyst. Based on these recent headlines for {ticker}, write a single, concise sentence (max 20 words) for an "AI Insight" section on a stock watchlist.

        Headlines:
        {headlines}

        AI Insight:
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating AI insight: {e}")
        return "Could not generate AI insight at this time."


def answer_question(query: str):
    """Answers a general financial question using the LLM."""
    try:
        prompt = f"You are an expert financial analyst. Answer the following question clearly and concisely: {query}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error answering question: {e}")
        return "Sorry, I could not process that question at this time."