# main.py — The entry point of our FastAPI backend
# Run this file to start the server: uvicorn main:app --reload
#
# FastAPI automatically generates interactive API documentation at:
#   http://localhost:8000/docs   ← Swagger UI (interactive)
#   http://localhost:8000/redoc  ← ReDoc UI (readable)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

# ── Create the FastAPI Application ───────────────────────────────────────────
app = FastAPI(
    title="QUANTUM AGENT API",
    description="Multi-Agent Financial Intelligence Platform — Technical, Fundamental & Sentiment Analysis",
    version="1.0.0",
)

# ── CORS (Cross-Origin Resource Sharing) ──────────────────────────────────────
# This is REQUIRED so our React frontend (running on port 5173) can talk to
# our FastAPI backend (running on port 8000).
# Without this, the browser will block the API calls.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev server ports
    allow_credentials=True,
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


# ── Run directly (for development) ────────────────────────────────────────────
# You can run this file directly: python main.py
# Or use uvicorn: uvicorn main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
