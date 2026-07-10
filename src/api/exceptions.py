from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def custom_http_exception_handler(request: Request, exc: Exception):
    """
    Catch-all exception handler to ensure the API never returns a raw HTML traceback,
    but instead always returns a clean JSON structure that the frontend can parse.
    """
    logger.error(f"HTTP Error on {request.method} {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "An internal server error occurred.", "details": str(exc)},
    )

async def validation_exception_handler(request: Request, exc: Exception):
    """
    Handles Pydantic validation errors (e.g. missing fields in the JSON payload)
    """
    return JSONResponse(
        status_code=422,
        content={"error": True, "message": "Invalid request payload.", "details": exc.errors()},
    )
