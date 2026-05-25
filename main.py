from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# السماح للموقع بالاتصال بالسيرفر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class MessageRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_ai(req: MessageRequest):
    try:
        full_prompt = f"""
        You are the official AI assistant for Laith Saleh, a CIS student and AI Developer. 
        Your job is to answer questions about Laith's skills, projects (like LON Automation System), and career goals.
        Be professional, convincing, and concise. Answer in the language the user speaks.
        
        User message: {req.message}
        """
        
        # الاتصال المباشر بسيرفرات جوجل (أضمن طريقة)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"reply": reply}
        else:
            err_msg = data.get("error", {}).get("message", "Unknown API error")
            return {"reply": f"API Error: {err_msg}"}
            
    except Exception as e:
        return {"reply": f"System Error: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "Backend is running!"}
