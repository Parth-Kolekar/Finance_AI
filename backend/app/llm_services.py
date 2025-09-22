# app/llm_services.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# --- Word List Loading ---
def load_word_list(file_path: str) -> set:
    """
    Loads a list of words from a text file into a set.
    It tries multiple encodings to handle common file format issues.
    """
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: Word list file not found at '{file_path}'.")
        return set()
    
    for encoding in ['utf-8', 'latin-1', 'utf-8-sig']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                words = {line.strip().lower() for line in f if line.strip()}
            print(f"✅ Loaded {len(words)} words from '{file_path}' (using {encoding} encoding).")
            return words
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error loading word list from '{file_path}' with encoding '{encoding}': {e}")
            return set()
            
    print(f"Error: Could not decode the file '{file_path}' with any of the attempted encodings.")
    return set()

base_dir = os.path.dirname(os.path.abspath(__file__))
positive_words = load_word_list(os.path.join(base_dir, 'positive-words.txt'))
negative_words = load_word_list(os.path.join(base_dir, 'negative-words.txt'))

# --- Gemini Model Configuration ---
model = None
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini model configured successfully.")
    except Exception as e:
        print(f"⚠️ Warning: could not configure Gemini model: {e}")
else:
    print("⚠️ Warning: GOOGLE_API_KEY not found. Using fallback methods.")

def classify_sentiment(headline: str):
    """Classifies a headline as POSITIVE, NEGATIVE, or NEUTRAL."""
    if not headline or not headline.strip():
        return "NEUTRAL"

    if model:
        try:
            prompt = f"""
            Analyze the sentiment of the following financial news item.
            Your response must be a single word: POSITIVE, NEGATIVE, or NEUTRAL.
            Do not include any other text, punctuation, or explanations.

            News: "{headline}"
            Sentiment:
            """
            response = model.generate_content(prompt)
            sentiment = response.text.strip().upper()
            
            if sentiment in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
                return sentiment
        except Exception:
            pass # Fall through to keyword analysis on error
    
    low = headline.lower()
    if any(word in low for word in positive_words):
        return 'POSITIVE'
    if any(word in low for word in negative_words):
        return 'NEGATIVE'
    
    return 'NEUTRAL'

def get_ai_insight_for_ticker(ticker: str, news_items: list[dict]):
    """Generates a concise AI insight based on news headlines."""
    if not news_items:
        return f"No recent news found for {ticker}."
    
    headlines = "\n".join([f"- {item['headline']}" for item in news_items if item.get('headline')])
    if not headlines:
        return f"No recent news headlines found for {ticker}."

    if model:
        try:
            prompt = f"""
            Act as a professional financial analyst. Based on these recent headlines for {ticker}, write a single, concise sentence (max 20 words) suitable for an 'AI Insight' label in a watchlist. Return only the sentence.

            Headlines:
            {headlines}

            AI Insight:
            """
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating AI insight: {e}")

    # Fallback if model fails
    first_headline = news_items[0].get('headline', 'recent developments')
    return f"Key headline for {ticker}: {first_headline[:100]}..."

def answer_question(query: str):
    """Answers a general financial question using the LLM."""
    if model:
        try:
            prompt = f"You are an expert financial analyst. Answer the following question clearly and concisely in Markdown. Use sections or bullet points where helpful. Keep the answer under 300 words. Question: {query}"
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error answering question: {e}")
            return "Sorry, I could not process that question at this time."
            
    # Fallback if model is not available
    return "The AI Assistant is currently unavailable. Please try again later."