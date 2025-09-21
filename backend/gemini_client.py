# gemini_client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_news_article(article_title: str, article_content: str) -> dict:
    """
    Analyzes a single news article to generate a summary and a sentiment.
    Returns a dictionary with 'summary' and 'sentiment'.
    """
    prompt = f"""
    Analyze the following financial news article.
    
    Instructions:
    1.  Provide a 1-2 sentence "AI Analysis" summarizing the key insight for an investor.
    2.  Provide a sentiment classification: "POSITIVE", "NEUTRAL", or "NEGATIVE".
    3.  Return the result as a single, valid JSON object with keys "summary" and "sentiment".
    
    Article Title: {article_title}
    Article Content: {article_content[:500]}
    
    JSON Output:
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up and parse the JSON response
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Error analyzing article '{article_title}': {e}")
        return {"summary": "AI analysis could not be generated.", "sentiment": "NEUTRAL"}

def generate_sector_analysis(sector_name: str, headlines: list[str]) -> dict:
    """
    Generates a brief analysis for a market sector based on recent headlines.
    """
    prompt = f"""
    Analyze these headlines for the {sector_name} sector.
    
    Instructions:
    1. Write a 2-3 sentence summary of the current trend.
    2. Provide a brief title for the trend (e.g., "Strong Q4 Earnings Momentum").
    3. Classify the overall trend as "BULLISH", "BEARISH", or "NEUTRAL".
    4. Return a single, valid JSON object with keys "title", "summary", and "trend".
    
    Headlines:
    - {"\n- ".join(headlines)}

    JSON Output:
    """
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Error analyzing sector {sector_name}: {e}")
        return {"title": f"{sector_name} Analysis", "summary": "Could not generate analysis.", "trend": "NEUTRAL"}

def generate_watchlist_insight(company_name: str, headlines: list[str]) -> str:
    """
    Generates a short, sharp "AI Insight" for a stock in the watchlist based on its latest news.
    """
    prompt = f"""
    You are a financial analyst. Write a concise, one-sentence "AI Insight" for {company_name} based on these recent headlines.
    Focus on the most impactful news for a potential investor.
    
    Headlines:
    - {"\n- ".join(headlines)}
    
    AI Insight:
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating insight for {company_name}: {e}")
        return "Could not generate AI insight."

def ask_assistant(question: str) -> str:
    """
    Handles questions for the AI Assistant chat feature.
    """
    prompt = f"You are a helpful financial AI assistant. Answer the following question: {question}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error in ask_assistant: {e}")
        return "Sorry, I couldn't process that question right now."