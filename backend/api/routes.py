# routes.py
# This file defines all the FastAPI API endpoints (URL routes).
# It's separated from main.py to keep code organized.
# Think of routes as the "menu" of what our API can do.

from fastapi import APIRouter, HTTPException

# Import our schemas (data shapes)
from models.schemas import AnalyzeRequest, AnalyzeResponse

# Import all our agents
from agents import technical_agent, fundamental_agent, sentiment_agent, master_agent

# Import our services
from services import stock_service, news_service, cache_service

# APIRouter is like a mini FastAPI app — we attach it to the main app in main.py
router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_stock(request: AnalyzeRequest):
    """
    POST /analyze
    The main endpoint. The frontend sends { "symbol": "AAPL" }
    and we run all 4 agents and return the combined analysis.

    Steps:
      1. Check cache (avoid re-running analysis for same symbol)
      2. Fetch stock data and news
      3. Run Technical, Fundamental, Sentiment agents
      4. Run Master Agent to combine results
      5. Cache and return the response
    """

    symbol = request.symbol.upper().strip()

    # ── Step 1: Check Cache ───────────────────────────────────────────────────
    cached = cache_service.get_from_cache(symbol)
    if cached:
        # We already analyzed this stock recently — return saved result
        return cached

    # ── Step 2: Fetch Data ────────────────────────────────────────────────────
    try:
        stock_data = stock_service.get_stock_data(symbol)
        news_data = news_service.get_news(symbol)
    except Exception as e:
        # If data fetching fails, return a 500 error with details
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")

    # ── Step 3: Run Individual Agents ─────────────────────────────────────────
    technical_result = technical_agent.analyze(stock_data)
    fundamental_result = fundamental_agent.analyze(stock_data)
    sentiment_result = sentiment_agent.analyze(news_data)

    # ── Step 4: Run Master Agent ──────────────────────────────────────────────
    final_decision = master_agent.analyze(technical_result, fundamental_result, sentiment_result)

    # ── Step 5: Build Response ────────────────────────────────────────────────
    response = {
        "stock": symbol,
        "technical": technical_result,
        "fundamental": fundamental_result,
        "sentiment": sentiment_result,
        "final_decision": final_decision,
    }

    # Save to cache so we don't recompute for 5 minutes
    cache_service.set_in_cache(symbol, response)

    return response


@router.get("/health")
async def health_check():
    """
    GET /health
    Simple health check endpoint to verify the backend is running.
    The frontend can ping this to confirm the server is up.
    """
    return {"status": "ok", "message": "QUANTUM AGENT backend is running"}


@router.get("/stock/{symbol}")
async def get_stock_info(symbol: str):
    """
    GET /stock/AAPL
    Returns raw stock data for a symbol — useful for debugging or charts.
    """
    symbol = symbol.upper().strip()
    stock_data = stock_service.get_stock_data(symbol)
    timeframe_data = stock_service.get_multiple_timeframes(symbol)

    return {
        "stock": stock_data,
        "timeframes": timeframe_data,
    }
