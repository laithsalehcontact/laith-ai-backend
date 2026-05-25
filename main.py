from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

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
        payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
        
        # 1. خطوة ذكية: نسأل جوجل ما هي النماذج المتاحة لهذا المفتاح تحديداً
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
        list_resp = requests.get(list_url)
        
        if list_resp.status_code != 200:
            return {"reply": f"API Key Error: {list_resp.text}"}
            
        models_data = list_resp.json().get('models', [])
        
        # 2. استخراج أول نموذج صالح لتوليد النصوص تلقائياً
        target_model = None
        for m in models_data:
            name = m.get("name", "")
            methods = m.get("supportedGenerationMethods", [])
            # نبحث عن نموذج يدعم النصوص ولا يحتوي على كلمة vision
            if "generateContent" in methods and "gemini" in name and "vision" not in name:
                target_model = name
                break
        
        if not target_model:
            return {"reply": "Error: Your API key doesn't have access to any Gemini text models."}
            
        # 3. إرسال الطلب للنموذج الذي وجدناه
        url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(url, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"reply": reply}
        else:
            return {"reply": f"Error with {target_model}: {data.get('error', {}).get('message', 'Unknown')}"}
            
    except Exception as e:
        return {"reply": f"System Error: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "Dynamic Backend is running!"}
