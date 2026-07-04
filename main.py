import os
import sys
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import JSONResponse, FileResponse # type: ignore
from pydantic import BaseModel, Field # type: ignore
from dotenv import load_dotenv # type: ignore

# pyrefly: ignore [missing-import]
from models import WhisperModelManager, get_model_manager, initialize_model_manager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== CONFIGURATION ====================

API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '8000'))
API_PREFIX = os.getenv('API_PREFIX', '/api/v1')

# File upload configuration
TEMP_UPLOAD_DIR = Path(os.getenv('TEMP_UPLOAD_DIR', './data/temp'))
OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', './output'))
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '500'))
ALLOWED_FORMATS = os.getenv('ALLOWED_FORMATS', 'mp3,wav,m4a,flac,ogg,webm').split(',')

# Create necessary directories
TEMP_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==================== PYDANTIC MODELS ====================

class TranscriptionRequest(BaseModel):
    """Request model for transcription."""
    language: Optional[str] = Field(None, description="Language code (e.g., 'en')")
    output_format: str = Field('json', description="Output format: json, txt, vtt, srt")


class TranscriptionResponse(BaseModel):
    """Response model for transcription."""
    success: bool
    message: str
    transcript: Optional[str] = None
    segments: Optional[list] = None
    language: Optional[str] = None
    duration: Optional[float] = None
    processing_time: Optional[float] = None
    timestamp: str


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str
    model_loaded: bool
    model_info: dict
    device_info: dict


class ModelInfoResponse(BaseModel):
    """Response model for model information."""
    model_size: str
    approximate_size: str
    parameters: int
    device: str
    language: str
    model_dir: str
    model_loaded: bool


# ==================== LIFESPAN EVENTS ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
  
    # Startup
    logger.info("="*60)
    logger.info("PHASE 1: Offline Speech Recognition System - Starting")
    logger.info("="*60)
    
    try:
        manager = initialize_model_manager()
        model = manager.load_model()
        logger.info("✓ Whisper model loaded successfully")
        logger.info(f"✓ Device: {manager.device}")
        logger.info(f"✓ Model Size: {manager.model_size}")
        logger.info(f"✓ API Server running on {API_HOST}:{API_PORT}{API_PREFIX}")
    except Exception as e:
        logger.error(f"✗ Failed to initialize model: {str(e)}")
        sys.exit(1)
    
    yield
    
    # Shutdown
    logger.info("="*60)
    logger.info("PHASE 1: Shutting down...")
    logger.info("="*60)
    manager.unload_model()
    logger.info("✓ Model unloaded, resources freed")


# ==================== FASTAPI APP ====================

app = FastAPI(
    title="Offline Speech Recognition System",
    description="Phase 1: Speech-to-Text Transcription API",
    version="1.0.0",
    docs_url="/docs" if os.getenv('ENABLE_DOCS', 'true').lower() == 'true' else None,
    lifespan=lifespan
)

# ==================== MIDDLEWARE ====================

# Add CORS middleware
if os.getenv('ENABLE_CORS', 'true').lower() == 'true':
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8000').split(',')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# ==================== ROUTES ====================

@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    
    manager = get_model_manager()
    
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        model_loaded=manager.model is not None,
        model_info=manager.get_model_info(),
        device_info=manager.get_device_info()
    )


@app.get(f"{API_PREFIX}/status", tags=["System"])
async def get_status():
  
    manager = get_model_manager()
    
    return {
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "api_prefix": API_PREFIX,
        "model_config": manager.get_model_info(),
        "features": {
            "transcription": os.getenv('FEATURE_TRANSCRIPTION', 'true').lower() == 'true',
            "caching": os.getenv('FEATURE_CACHING', 'false').lower() == 'true',
            "sentiment_analysis": os.getenv('FEATURE_SENTIMENT_ANALYSIS', 'false').lower() == 'true',
            "ner": os.getenv('FEATURE_NER', 'false').lower() == 'true',
            "question_answering": os.getenv('FEATURE_QUESTION_ANSWERING', 'false').lower() == 'true'
        }
    }


@app.post(f"{API_PREFIX}/transcribe", response_model=TranscriptionResponse, tags=["Transcription"])
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = None,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    
    import time
    
    start_time = time.time()
    
    try:
        # Validate file format
        # pyrefly: ignore [bad-argument-type]
        file_ext = Path(file.filename).suffix.lower().lstrip('.')
        if file_ext not in ALLOWED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format: {file_ext}. "
                       f"Allowed formats: {', '.join(ALLOWED_FORMATS)}"
            )
        
        # Check file size
        # pyrefly: ignore [unsupported-operation]
        file_size_mb = file.size / (1024 * 1024)
        if MAX_UPLOAD_SIZE > 0 and file_size_mb > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large: {file_size_mb:.1f}MB. "
                       f"Maximum: {MAX_UPLOAD_SIZE}MB"
            )
        
        # Save temporary file
        # pyrefly: ignore [unsupported-operation]
        temp_file_path = TEMP_UPLOAD_DIR / file.filename
        with open(temp_file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Processing file: {file.filename}")
        
        # Get model manager and perform transcription
        manager = get_model_manager()
        model = manager.model
        
        if model is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Server not ready."
            )
        
        # Perform transcription
        logger.info(f"Transcribing: {file.filename}...")
        result = model.transcribe(
            str(temp_file_path),
            language=language or manager.language,
            verbose=False
        )
        
        processing_time = time.time() - start_time
        
        # Extract response data
        response_data = {
            "success": True,
            "message": "Transcription completed successfully",
            "transcript": result.get("text", ""),
            "segments": result.get("segments", []),
            "language": result.get("language", manager.language),
            "duration": result.get("duration", 0),
            "processing_time": round(processing_time, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(
            f"✓ Transcription completed in {processing_time:.2f}s for {file.filename}"
        )
        
        # Clean up temporary file in background
        background_tasks.add_task(temp_file_path.unlink, missing_ok=True)
        
        return TranscriptionResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Transcription failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )


@app.get(f"{API_PREFIX}/model-info", response_model=ModelInfoResponse, tags=["System"])
async def get_model_info():
   
    manager = get_model_manager()
    return ModelInfoResponse(**manager.get_model_info())


@app.get(f"{API_PREFIX}/supported-formats", tags=["System"])
async def get_supported_formats():
  
    return {
        "supported_formats": ALLOWED_FORMATS,
        "max_file_size_mb": MAX_UPLOAD_SIZE,
        "max_file_size_description": "Unlimited" if MAX_UPLOAD_SIZE == 0 else f"{MAX_UPLOAD_SIZE}MB"
    }


@app.get(f"{API_PREFIX}/languages", tags=["System"])
async def get_supported_languages():
    """
    Get list of supported languages.
    
    Returns:
        dict: Supported language codes
    """
    # Whisper supports 99+ languages
    return {
        "auto_detect": True,
        "default_language": "en",
        "note": "Whisper supports 99+ languages. "
                "Specify language code for better accuracy or leave empty for auto-detection."
    }


@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: API information and available endpoints
    """
    return {
        "name": "Offline Speech Recognition System",
        "phase": "Phase 1 - Speech-to-Text Transcription",
        "version": "1.0.0",
        "description": "OpenAI Whisper based offline speech recognition",
        "api_prefix": API_PREFIX,
        "endpoints": {
            "health": "/health",
            "status": f"{API_PREFIX}/status",
            "transcribe": f"{API_PREFIX}/transcribe (POST)",
            "model_info": f"{API_PREFIX}/model-info",
            "supported_formats": f"{API_PREFIX}/supported-formats",
            "supported_languages": f"{API_PREFIX}/languages",
            "docs": "/docs"
        }
    }


# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "detail": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "status_code": 500,
            "detail": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )


# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting FastAPI application...")
    logger.info(f"Server: {API_HOST}:{API_PORT}")
    logger.info(f"Reload: {os.getenv('RELOAD', 'true').lower() == 'true'}")
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=os.getenv('RELOAD', 'true').lower() == 'true',
        log_level=os.getenv('LOG_LEVEL', 'info').lower()
    )
