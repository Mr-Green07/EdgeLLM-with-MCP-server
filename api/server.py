import asyncio
import shutil
from pathlib import Path
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator.agent import SystemAgentOrchestrator

app = FastAPI(title="Multi Agent Server API", version="1.0.0")
WORKSPACE_DIR = Path(__file__).resolve().parent.parent / "workspace"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize single shared orchestrator instance (lazy-loads model on first request)
orchestrator = SystemAgentOrchestrator()

class QueryRequest(BaseModel):
    prompt: str

class ConfirmRequest(BaseModel):
    token: str
    action: str

@app.post("/api/query")
async def execute_query(req: QueryRequest):
    try:
        result = await orchestrator.execute_query(req.prompt)

        print("Result type:", type(result))
        print("Result:", repr(result))
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "model": "Qwen3.5-4BQ"}

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
        file_path = WORKSPACE_DIR / file.filename
        
        # Save file to workspace directory
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Re-index workspace chunks for the RAG engine
        num_chunks = orchestrator.rag_agent.rag.index_workspace()
        
        return {
            "status": "success",
            "summary": f"Uploaded '{file.filename}' successfully and indexed {num_chunks} total chunks.",
            "filename": file.filename,
            "indexed_chunks": num_chunks
        }
    except Exception as e:
        return {"status": "error", "summary": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)