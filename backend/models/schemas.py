# schemas.py
# This file defines the data shapes (schemas) for our API
# Pydantic automatically validates that incoming data matches these shapes

from pydantic import BaseModel
from typing import Optional


# ─── Request Schema ───────────────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    """
    What the frontend sends us when the user searches for a stock.
    Example: { "symbol": "AAPL" }
    """
    symbol: str  # e.g. "AAPL", "TSLA", "INFY"


# ─── Agent Output Schemas ─────────────────────────────────────────────────────

class TechnicalResult(BaseModel):
    """Output from the Technical Analysis Agent"""
    trend: str          # e.g. "Bullish", "Bearish", "Neutral"
    confidence: int     # 0–100 score
    reason: str         # Human-readable explanation


class FundamentalResult(BaseModel):
    """Output from the Fundamental Analysis Agent"""
    fundamental: str    # e.g. "Strong", "Weak", "Average"
    confidence: int
    reason: str


class SentimentResult(BaseModel):
    """Output from the Sentiment Analysis Agent"""
    sentiment: str      # e.g. "Positive", "Negative", "Neutral"
    confidence: int
    reason: str


class FinalDecision(BaseModel):
    """Output from the Master Agent that combines all signals"""
    recommendation: str  # "BUY", "HOLD", or "SELL"
    confidence: int
    risk: str            # "Low", "Medium", "High"
    summary: str         # One-line explanation


# ─── Full Response Schema ─────────────────────────────────────────────────────

class AnalyzeResponse(BaseModel):
    """
    The complete response we send back to the frontend.
    Contains results from all 4 agents.
    """
    stock: str
    technical: TechnicalResult
    fundamental: FundamentalResult
    sentiment: SentimentResult
    final_decision: FinalDecision
