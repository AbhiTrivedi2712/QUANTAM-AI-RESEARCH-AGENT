# 🔒 Security and Safety Controls: Quantum Agent

This document explains the security mechanisms, validation rules, CORS protections, and secret isolation guidelines implemented on the **QUANTUM** platform.

---

## 🔒 Secret Isolation (No Client Keys)

The React client application contains **zero credentials or API keys**:
- **Backend Proxying**: All integration tasks (fetching Yahoo Finance data, news feed scraping, and Groq API calls) run on the backend server.
- **Server Environment Isolation**: API keys (`GROQ_API_KEY`, `GEMINI_API_KEY`) are kept isolated on the server-side environment block. The client calls a unified relative endpoint `/api/analyze` using its base URL, keeping secrets secure.

---

## 🛡️ Input Validation & Sanitization

To protect downstream processing against execution errors or injection vectors, the backend employs a multi-tiered validation approach:

### 1. Schema Validation (Pydantic v2)
FastAPI uses Pydantic schemas (`AnalyzeRequest`) to validate payload shapes. Empty symbols or non-string values are rejected automatically (HTTP 422).

### 2. Regex Format Validation
Before calling yfinance or executing analysis tasks, the server verifies the symbol format using a strict regular expression:
```python
import re

def is_valid_symbol_format(symbol: str) -> bool:
    """Checks for standard equity tickers (1-15 Alphanumerics, optional NSE dot or suffix)."""
    return bool(re.match(r"^[A-Z0-9\.\-]{1,15}$", symbol))
```
- **Constraints**: Restricts symbols to standard letters, numbers, dots, and hyphens. Length is capped at 15 characters.
- **Rejection**: Tickers failing regex validation are rejected with an HTTP 400 (`INVALID_TICKER` error).

---

## 🌐 CORS Constraints

FastAPI's `CORSMiddleware` limits access to approved origins:
* **Development Defaults**: Allows typical local ports: `http://localhost:5173`, `http://localhost:3000`.
* **Dynamic Production Origins**: Production origins can be loaded from the `ALLOWED_ORIGINS` environment variable.
* **Safe Credentials Configuration**: If the wildcard `"*"` origin is configured, the server automatically disables `allow_credentials=True` to comply with CORS security standards and prevent browser exploits.

---

## 📜 System Diagnostics & Safe Health Checks

The backend provides a `/api/health` diagnostics check:
- **No Secret Leaks**: The endpoint checks for keys without printing the keys themselves. It returns a boolean flag indicating if the key is loaded in memory:
  ```json
  "environment": {
      "groq_api_key_configured": true,
      "gemini_api_key_configured": true
  }
  ```
- **Error Masks**: Exceptions from sub-processes or external connections are caught, logged internally, and returned as generic messages to prevent internal paths or system details from leaking.
