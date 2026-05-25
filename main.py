from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# السماح للجميع بالاتصال مؤقتاً لتجنب أي مشاكل حظر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# جلب المفتاح
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# استخدام النموذج الأساسي بدون إعدادات معقدة لتجنب تعارض الإصدارات
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

class MessageRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_ai(req: MessageRequest):
    try:
        # دمج التعليمات مع رسالة المستخدم مباشرة
        full_prompt = f"""
        You are the official AI assistant for Laith Saleh, a CIS student and AI Developer. 
        Your job is to answer questions about Laith's skills, projects (like LON System), and career goals.
        Be professional and concise. Answer in the language the user speaks.
        
        User message: {req.message}
        """
        
        response = model.generate_content(full_prompt)
        return {"reply": response.text}
        
    except Exception as e:
        # هذا السطر سيعرض لك سبب المشكلة الحقيقي من سيرفرات جوجل
        return {"reply": f"Google API Error: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "Laith AI Backend is running smoothly."}
