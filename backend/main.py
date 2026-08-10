# main.py — The entry point of our FastAPI backend
# Run this file to start the server: uvicorn main:app --reload
#
# FastAPI automatically generates interactive API documentation at:
#   http://localhost:8000/docs   ← Swagger UI (interactive)
#   http://localhost:8000/redoc  ← ReDoc UI (readable)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from dotenv import load_dotenv

# Load environment variables at server start
load_dotenv()

# ── Create the FastAPI Application ───────────────────────────────────────────
app = FastAPI(

    title="QUANTUM AGENT API",
    description="Multi-Agent Financial Intelligence Platform — Technical, Fundamental & Sentiment Analysis",
    version="1.0.0",
)

# ── CORS (Cross-Origin Resource Sharing) ──────────────────────────────────────
# This is REQUIRED so our React frontend can talk to our FastAPI backend.
# We read from ALLOWED_ORIGINS env variable, splitting by commas.
import os
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
else:
    origins = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:3000",
    ]

# Spec check: if "*" is present, we must not pass allow_credentials=True
allow_all_origins = "*" in origins or len(origins) == 0

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all_origins else origins,
    allow_credentials=not allow_all_origins,
    allow_methods=["*"],   # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],   # Allow all headers
)

# ── Register Routes ────────────────────────────────────────────────────────────
# All routes defined in api/routes.py are now available under /api/
# Example: POST /api/analyze, GET /api/health
app.include_router(router, prefix="/api")


# ── Root Endpoint ─────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    """Welcome message for the API root."""
    return {
        "message": "Welcome to QUANTUM AGENT API",
        "docs": "Visit /docs for interactive API documentation",
        "endpoints": {
            "analyze": "POST /api/analyze",
            "health": "GET /api/health",
            "stock": "GET /api/stock/{symbol}",
        },
    }


@app.get("/health")
async def root_health():
    """Service health check endpoint returning status ok."""
    return {"status": "ok"}


# ── Run directly (for development) ────────────────────────────────────────────
# You can run this file directly: python main.py
# Or use uvicorn: uvicorn main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
