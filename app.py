"""SAMYOJANA — Autonomous Agentic AI for Indian Banking
FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.orchestrator import AgentOrchestrator
import pathlib

app = FastAPI(title="SAMYOJANA", version="5.0.0", description="Autonomous Agentic AI for Indian Banking")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

orchestrator = AgentOrchestrator()

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

@app.get("/health")
async def health():
    return {"status": "ok", "version": "5.0.0", "agents": ["acquisition", "engagement", "guardian"]}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    result = orchestrator.process_request(req.message, req.session_id)
    return JSONResponse(content=result)

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    html_path = pathlib.Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
