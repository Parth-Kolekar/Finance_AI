# app/llm_services.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
# Try to configure Gemini; if not present, we'll gracefully degrade to simple heuristics
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        print(f"Warning: could not configure Gemini model: {e}")
        model = None
else:
    model = None

def classify_sentiment(headline: str):
    """Classifies a headline as POSITIVE, NEGATIVE, or NEUTRAL."""
    if not headline:
        return "NEUTRAL"
    try:
        # If model configured, ask it; otherwise use simple keyword heuristics
        if model:
            prompt = f"""
            Analyze the sentiment of the following financial news headline.
            Classify it as strictly one of: POSITIVE, NEGATIVE, or NEUTRAL.
            Return only the single word classification (no extra text).

            Headline: "{headline}"
            Sentiment:
            """
            response = model.generate_content(prompt)
            sentiment = getattr(response, 'text', '').strip().upper()
            if sentiment in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
                return sentiment
        # Simple fallback
        low = headline.lower()
        if any(w in low for w in ['rise', 'rally', 'beat', 'gain', 'up', 'surge', 'record']):
            return 'POSITIVE'
        if any(w in low for w in ['fall', 'drop', 'miss', 'decline', 'down', 'loss', 'bear']):
            return 'NEGATIVE'
        return 'NEUTRAL'
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
        if model:
            prompt = f"""
            Act as a professional financial analyst. Based on these recent headlines for {ticker}, write a single, concise sentence (max 20 words) suitable for an 'AI Insight' label in a watchlist. Return only the sentence in html format.

            Headlines:
            {headlines}

            AI Insight:
            """
            response = model.generate_content(prompt)
            return getattr(response, 'text', '').strip()
        # Fallback: pick first headline and summarize heuristically
        first = news_items[0]['headline'] if news_items and news_items[0].get('headline') else None
        if first:
            return f"Based on recent headlines, {ticker} shows developments — see: {first[:120]}..."
        return f"No recent news found for {ticker}."
    except Exception as e:
        print(f"Error generating AI insight: {e}")
        return "Could not generate AI insight at this time."


def answer_question(query: str):
    """Answers a general financial question using the LLM."""
    try:
        # Request a Markdown-formatted answer that can be rendered on the frontend
        if model:
            prompt = f"You are an expert financial analyst. Answer the following question clearly and concisely in Markdown. Use sections or bullet points where helpful. Keep the answer under 300 words. Question: {query}"
            response = model.generate_content(prompt)
            return getattr(response, 'text', '').strip()
        # Simple fallback: return a basic text response
        return f"I don't have access to the LLM right now. Here's a brief suggestion: {query} -> Try checking recent earnings, analyst notes, and price action."
    except Exception as e:
        print(f"Error answering question: {e}")
        return "Sorry, I could not process that question at this time."