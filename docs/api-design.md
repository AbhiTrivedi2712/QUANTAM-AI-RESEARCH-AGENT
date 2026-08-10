# 🛰️ API Contract & Schema Design: Quantum Agent

This document outlines the REST API endpoints, validation constraints, rate limit protections, and V2 JSON schema specifications of the **QUANTUM** platform.

---

## 🚦 Security & Rate Limits
* **IP Rate Limiter**: Maximum **10 requests per 60 seconds** per client IP. Exceeding this triggers an immediate `429 Too Many Requests` response.
* **Pre-Flight Validation**: Symbol parameters are verified against standard formats (`^[A-Z0-9\.\-]{1,15}$`) to protect against injection attempts before downstream processes run.

---

## 🛰️ REST Endpoints

### 1. `POST /api/analyze`
Triggers the full multi-agent analysis sequence for a stock ticker.

* **Request Payload**:
  ```json
  {
    "symbol": "AAPL"
  }
  ```
  *(Supported formats: Standard US equities like `AAPL`, `TSLA`, and NSE tickers with `.NS` suffix like `INFY.NS`, `RELIANCE.NS`)*

* **Response Payload (200 OK)**:
  ```json
  {
    "stock": "AAPL",
    "current_price": 298.01,
    "change_pct": 0.7,
    "market_state": "REGULAR",
    "technical": {
      "trend": "Bullish",
      "confidence": 98,
      "reason": "Price is above key moving averages.",
      "summary": "Bullish technical posture supported by Price above 50d & 200d MA (Long-Term Uptrend).",
      "trend_strength": "Strong",
      "support": 290.55,
      "resistance": 315.2,
      "support_level": 290.55,
      "resistance_level": 315.2,
      "distance_to_support": 5.0,
      "distance_to_resistance": 5.0,
      "volatility": 19.1,
      "signals": [
        "Price above 50-day MA",
        "Price above 200-day MA",
        "MACD value above signal line"
      ],
      "risk_factors": [
        "Normal asset volatility"
      ],
      "timeframe_analysis": {
        "15m": "Bullish",
        "1h": "Bearish",
        "4h": "Bullish",
        "1d": "Bearish",
        "1w": "Strong Bullish"
      },
      "fallback_active": false,
      "rsi_interpretation": "RSI stands at 53.4, indicating neutral momentum with substantial room to run.",
      "macd_interpretation": "MACD histograms show bullish signal crossover indicating positive short-term momentum.",
      "moving_average_analysis": "AAPL trades above its 50d and 200d moving average thresholds, confirming an attractive long-term trend structure.",
      "key_technical_conclusion": "Strong structural breakout patterns support ongoing consolidation with an upward bias."
    },
    "fundamental": {
      "fundamental": "Strong",
      "confidence": 90,
      "reason": "Double-digit profit margins and high solvency health.",
      "summary": "Excellent fundamental posture led by high double-digit profit margins and solid capital reserve buffers.",
      "health_score": 90,
      "valuation_score": 35,
      "growth_score": 80,
      "strengths": [
        "high double-digit profit margins",
        "Significant cash reserves and low leverage"
      ],
      "weaknesses": [
        "Valuation premium risk"
      ],
      "metrics": {
        "pe_ratio": 36.5,
        "revenue_growth_pct": 16.6,
        "earnings_growth_pct": 21.8,
        "market_cap": "$4.38T",
        "total_revenue": 451442016256,
        "net_income": 122575003648
      },
      "fallback_active": false,
      "growth_outlook": "Apple's premium hardware cycles and high-margin services indicate highly sustainable growth trajectories.",
      "valuation_outlook": "PE of 36.5x is elevated vs peers, highlighting the importance of incoming hardware sales.",
      "ai_commentary": "Solvency audit suggests high solvency health, supported by a growing recurring services stream."
    },
    "sentiment": {
      "sentiment": "Neutral",
      "confidence": 78,
      "reason": "Balanced media flow with positive revision offsets.",
      "summary": "Balanced sentiment flow (1 positive, 0 negative, 7 neutral).",
      "positive_drivers": [
        "Should You Buy, Sell, or Hold AAPL Stock After a 52% Rise in One Year?"
      ],
      "negative_drivers": [
        "General macroeconomic headwinds"
      ],
      "positive_ratio": 0.12,
      "negative_ratio": 0.0,
      "events": [
        "Product Launch"
      ],
      "articles": [
        {
          "title": "Should You Buy, Sell, or Hold AAPL Stock After a 52% Rise in One Year?",
          "sentiment": "positive",
          "source": "Yahoo Finance",
          "link": "https://finance.yahoo.com/m/example",
          "publish_time": "Mon, 22 Jun 2026 12:00:00 GMT"
        }
      ],
      "fallback_active": false,
      "catalyst_type": "Product Launch",
      "most_important_event": "Introduction of AI-integrated capabilities and operating system updates.",
      "market_narrative": "Psychology remains neutral to consolidative ahead of event validations.",
      "ai_news_summary": "Media coverage is highly positive, focused on WWDC 2026 expectations and new safety tools."
    },
    "final_decision": {
      "market_bias": "Bullish",
      "confidence": 78,
      "risk": "Medium",
      "key_drivers": [
        "Technical Agent indicates Bullish trend with strong strength.",
        "Fundamental Agent reports Strong company metrics (Health: 90/100)."
      ],
      "watchlist_factors": [
        "Monitor Support boundary at $290.55 and Resistance ceiling at $315.20."
      ],
      "summary": "Orchestrated analysis indicates a Bullish market bias with an aggregated confidence score of 78% and a Medium risk profile. Technical momentum aligns as Bullish, coupled with a fundamental health index of 90/100 and sentiment drivers matching Neutral.",
      "potential_risks": [
        "Valuation multiple compression if AI implementation cycles delay."
      ],
      "future_catalysts": [
        "WWDC keynote and launch of new hardware models."
      ],
      "fallback_active": false,
      "bull_case": [
        "AI integration expected to trigger a major hardware replacement cycle.",
        "Recurring services growth offsets hardware cyclicality."
      ],
      "bear_case": [
        "Multiple compression is a core risk if hardware sales slow down."
      ],
      "risk_register": [
        {
          "category": "Valuation Risk",
          "severity": "High",
          "probability": "Medium",
          "explanation": "PE multiple of 36.5x is elevated relative to historical averages."
        }
      ],
      "catalyst_calendar": [
        {
          "event": "WWDC Keynote",
          "expected_date": "June 15, 2026",
          "importance": "High",
          "potential_impact": "Unveiling of core OS AI features."
        }
      ]
    },
    "system_status": {
      "backend_status": "Online",
      "groq_status": "Online",
      "yfinance_status": "Online",
      "news_status": "Online",
      "cache_status": "Miss",
      "cache_ttl_sec": 300,
      "execution_time_sec": 2.84
    },
    "timeline": [
      {
        "timestamp": "12:00:01",
        "event": "Request Received"
      },
      {
        "timestamp": "12:00:02",
        "event": "Market Data Ingested"
      },
      {
        "timestamp": "12:00:03",
        "event": "Technical Intel Generated"
      },
      {
        "timestamp": "12:00:03",
        "event": "Fundamental Intel Generated"
      },
      {
        "timestamp": "12:00:03",
        "event": "Sentiment Intel Generated"
      },
      {
        "timestamp": "12:00:04",
        "event": "Consensus Aggregated"
      },
      {
        "timestamp": "12:00:04",
        "event": "Report Dispatched"
      }
    ]
  }
  ```

---

### 2. `GET /api/stock/{symbol}`
Fetches raw market statistics and resampled timeframe price points for charting.

* **Response Payload (200 OK)**:
  ```json
  {
    "stock": {
      "symbol": "AAPL",
      "price": 298.01,
      "change": 2.07,
      "change_pct": 0.7,
      "volume": 52345600,
      "market_cap": "$4.38T",
      "pe_ratio": 36.5,
      "revenue_growth": 16.6,
      "earnings_growth": 21.8,
      "rsi": 53.4,
      "macd": 7.41,
      "moving_avg_50": 282.06,
      "moving_avg_200": 265.14,
      "support": 290.55,
      "resistance": 315.2,
      "volatility": 19.1,
      "source": "Yahoo Finance (Real-Time)"
    },
    "timeframes": {
      "15m": [295.4, 296.8, 298.01],
      "1h": [292.1, 294.5, 298.01],
      "4h": [288.4, 291.2, 298.01],
      "1d": [280.5, 282.1, 298.01],
      "1w": [265.2, 274.8, 298.01]
    }
  }
  ```

---

### 3. `GET /api/health`
Verifies backend server state and environment configuration status.

* **Response Payload (200 OK)**:
  ```json
  {
    "status": "ok",
    "message": "QUANTUM AGENT Backend is fully operational",
    "environment": {
      "groq_api_key_configured": true,
      "gemini_api_key_configured": true
    }
  }
  ```

---

## 🚫 Standard Error Responses

### `400 Bad Request` — Invalid Ticker Format
Returned if the ticker fails standard format validation or does not exist on yfinance.
```json
{
  "detail": "INVALID_TICKER"
}
```

### `429 Too Many Requests` — Rate Limit Exceeded
Returned if a client IP exceeds rate constraints.
```json
{
  "detail": "RATE_LIMIT_EXCEEDED"
}
```

### `500 Internal Server Error` — Service Failure
Returned if a subprocess or external dependency fails.
```json
{
  "detail": "Analytical sub-agent failure: Groq connection failed after retries."
}
```
