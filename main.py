from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# Load .env
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create app FIRST
app = FastAPI()

# THEN add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

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
            
            msg.message)
        return {"reply": response.text}
    except Exception as e:
        return {"error": str(e)}