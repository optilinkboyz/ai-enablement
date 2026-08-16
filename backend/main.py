"""
AT&S AI Enablement Starter Kit — Backend
=========================================
FastAPI application entry point.
Registers all routes and configures middleware.

Author: Andrew Nelson Enoh
Version: 1.0.0
"""
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import HealthResponse
from routes.ask import router as ask_router
from routes.summarise import router as summarise_router
from routes.upload import router as upload_router

# ── Environment & Logging ─────────────────────────────────────────────────────
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ── App Initialisation ────────────────────────────────────────────────────────
app = FastAPI(
    title="AT&S AI Enablement Starter Kit",
    description="""
    A lightweight AI assistant for AT&S employees.
    
    ## Features
    - **Upload** PDF, DOCX, or TXT documents
    - **Ask** questions about uploaded documents in plain language  
    - **Summarise** documents at different detail levels
    
    ## Who is this for?
    All AT&S employees — no technical knowledge required.
    """,
    version="1.0.0",
    contact={
        "name": "Corporate IT — Digital & AI Enablement",
        "email": "it@ats.net"
    }
)

# ── CORS Middleware ───────────────────────────────────────────────────────────
# Allows the React frontend to communicate with this backend
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Route Registration ────────────────────────────────────────────────────────
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(summarise_router)

# ── Health Check ──────────────────────────────────────────────────────────────
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health check",
    description="Returns the current status of the API."
)
async def health_check():
    """Simple health check endpoint for monitoring and deployment verification."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="AT&S AI Enablement API is running."
    )


@app.get("/", tags=["System"], include_in_schema=False)
async def root():
    return {
        "message": "AT&S AI Enablement Starter Kit API",
        "docs": "/docs",
        "health": "/health"
    }


# ── Dev Server ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
