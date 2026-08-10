# ⚙️ Scalability and Enterprise Readiness Guide

This document describes the logging infrastructure, validation logic, connection retry systems, and production server settings implemented inside the **QUANTUM** platform to support concurrent enterprise environments.

---

## 📁 Centralized Logging Infrastructure

The FastAPI gateway configures a rotating logging strategy to output diagnostics to both standard output and a rolling log file located at `../quantum_system.log`.

### Logger Settings (`routes.py`):
```python
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler("../quantum_system.log", maxBytes=10*1024*1024, backupCount=5, encoding="utf-8")
    ]
)
```

### Logging Policies:
* **Log Rotation**: Individual logs are capped at **10MB** (`maxBytes=10*1024*1024`), preserving up to **5 backups** (`backupCount=5`). This prevents server disk exhaustion.
* **Audit Trail Coverage**: Captures detailed records of request arrivals, cache statuses, yfinance connections, RSS XML fallback redirections, sub-agent processing times, and master synthesis calculations.

---

## 🔄 API Retry & Network Resiliency Logic

Connections to external dependencies (Groq completions, yfinance pulls, RSS xml parsing) use retry handlers to mitigate temporary packet losses.

### 1. Exponential Backoff Resiliency (`llm_service.py`):
Completion queries to the Groq Cloud Gateway are wrapped in retry loops:
```python
max_retries = 2
backoff = 1.0

for attempt in range(max_retries + 1):
    try:
        # Enforces a strict 10s timeout
        response = client.post(GROQ_URL, json=payload, headers=headers, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        if attempt == max_retries:
            raise e
        time.sleep(backoff * (attempt + 1))
```

### 2. Request Timeout Strategy
All external data harvesters use tight timeouts (typically 8.0s to 10.0s) to prevent thread blockages:
- **yfinance**: Queries use a cached requests session to avoid rate blocks.
- **RSS Parser**: Uses `httpx.get(url, timeout=8.0)` to handle network drops.

---

## 🛡️ Pre-Flight Validations

### 1. Environment Verification
At startup, `routes.py` and `main.py` inspect variables:
- Confirms the presence of `GROQ_API_KEY`.
- Logs a diagnostic warning if keys are missing, highlighting fallback mode activation.

### 2. Input Validation
Incoming request bodies are validated using Pydantic v2. Non-compliant formats are rejected immediately (HTTP 400), protecting resources from wasteful database queries.

---

## 🌐 Enterprise Server Configuration

For production environments, the platform runs FastAPI behind **Gunicorn** to handle concurrency.

### Gunicorn Worker Options:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000
```

* `-w 4`: Spawns **4 parallel worker processes** to distribute queries.
* `-k uvicorn.workers.UvicornWorker`: Runs asynchronous Uvicorn workers.
* `--bind 0.0.0.0:10000`: Binds the port for Render routing.
* **Concurrency Profile**: Handles thousands of active connections using asynchronous loop workers, reducing server footprint.
