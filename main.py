from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# السماح للجميع بالاتصال
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

# تم تغيير اسم النموذج هنا إلى gemini-pro لضمان التوافق التام
model = genai.GenerativeModel(model_name="gemini-pro")

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
        
        response = model.generate_content(full_prompt)
        return {"reply": response.text}
        
    except Exception as e:
        return {"reply": f"Google API Error: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "Laith AI Backend is running smoothly."}
