# gemini_client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() # This loads the .env file

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash') # Use a fast model for hackathons

def generate_market_summary(headlines: list[str]) -> str:
    # This is the prompt from the project plan. It's excellent.
    prompt = f"""
    Act as a financial analyst. Based on these headlines, write a 4-5 sentence 'Market Summary' for the day.
    Start with a general sentiment (e.g., 'Broad Indices Down on Policy Shock...'), then explain the key sector movements and the reasons why.
    Maintain a professional, analytical tone.

    Headlines:
    - {"\n- ".join(headlines)}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Could not generate market summary at this time."

# gemini_client.py (add this function)

def ask_gemini(question: str) -> str:
    """A simple passthrough to the Gemini model."""
    prompt = f"Please answer the following finance-related question: {question}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error in ask_gemini: {e}")
        return "I am sorry, I couldn't process that question."