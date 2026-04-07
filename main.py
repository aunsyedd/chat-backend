from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create FastAPI app
app = FastAPI()

# Enable CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- Use "*" for testing. Replace with your frontend URL later
    allow_methods=["*"],
    allow_headers=["*"],
)

# Message schema
class Message(BaseModel):
    message: str

# System prompt for Gemini
SYSTEM_PROMPT = """
You are an AI assistant. Follow these rules strictly:
1. Answer in 3–5 short sentences max.
2. Do not use bullet points or extra explanations.
3. Only provide direct, point-to-point answers.
4. If code, show only necessary code.
5. Summarize everything in 4 lines max.
"""

@app.post("/chat")
async def chat(msg: Message):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            {"prompt": SYSTEM_PROMPT + "\n" + msg.message}
        )
        return {"reply": response.text}
    except Exception as e:
        print("ERROR:", e)  # logs in Railway
        return {"error": str(e)}