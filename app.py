import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from agent import run_medical_agent

app = FastAPI(
    title="MediCare AI - Medical Agentic Assistant",
    description="Clinical-grade Healthcare Assistant powered by Groq LLaMA / GPT-OSS",
    version="2.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class MedicalChatRequest(BaseModel):
    message: str
    thread_id: str = "patient_session"


@app.get("/")
async def serve_home():
    return FileResponse(os.path.join(TEMPLATES_DIR, "index.html"))


@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "service": "MediCare AI Medical Assistant",
        "port": 3000,
        "engine": "Groq Medical Inference Core"
    }


@app.post("/api/chat")
async def chat_endpoint(payload: MedicalChatRequest):
    if not payload.message.strip():
        return JSONResponse(status_code=400, content={"error": "Message cannot be empty."})

    try:
        reply = run_medical_agent(payload.message, thread_id=payload.thread_id)
        return {
            "success": True,
            "response": reply,
            "thread_id": payload.thread_id
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": f"Clinical agent error: {str(e)}"}
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    print(f"\n🩺 MediCare AI Server starting on http://localhost:{port}\n")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
