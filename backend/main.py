# main.py
# main.py (at the top)
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
    
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Important for frontend
import data_fetcher
import gemini_client

app = FastAPI()

# --- CORS Middleware ---
# This is crucial for allowing Person A's frontend (on a different domain)
# to communicate with your backend.
origins = [
    "http://localhost:3000",  # SvelteKit/Next.js default
    # Add Vercel deployment URL of Person A here when it's ready
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------

@app.get("/")
def read_root():
    return {"Hello": "Backend Brains"}

@app.get("/market-summary")
def get_market_summary():
    try:
        headlines = data_fetcher.get_top_indian_market_headlines()
        if not headlines:
            raise HTTPException(status_code=404, detail="No headlines found.")
        
        summary = gemini_client.generate_market_summary(headlines)
        return {"market_summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# main.py (add this endpoint)

@app.post("/ask")
def ask_question(request: AskRequest):
    try:
        answer = gemini_client.ask_gemini(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))