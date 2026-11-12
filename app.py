import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from agent import run_agent

app = FastAPI(
    title="Nexus AI - Professional Agentic Chatbot",
    description="Enterprise-grade AI Assistant powered by Groq LLaMA-3.1-8B",
    version="2.0.0"
)

# Setup directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_session"


@app.get("/")
async def serve_home():
    return FileResponse(os.path.join(TEMPLATES_DIR, "index.html"))


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "engine": "Groq LLaMA-3.1-8B-Instant",
        "port": 3000,
        "mode": "Production Enterprise"
    }


@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    if not payload.message.strip():
        return JSONResponse(status_code=400, content={"error": "Message cannot be empty"})

    try:
        reply = run_agent(payload.message, thread_id=payload.thread_id)
        return {
            "success": True,
            "response": reply,
            "thread_id": payload.thread_id
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": f"Agent error: {str(e)}"}
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    print(f"\n🚀 Nexus AI Enterprise Server starting on http://localhost:{port}\n")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
