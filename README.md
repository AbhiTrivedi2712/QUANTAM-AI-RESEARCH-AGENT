# QUANTUM AGENT 🤖
## Institutional Multi-Agent Financial Intelligence Platform

A beginner-friendly MVP that uses **4 AI agents** to analyze stocks and produce a **BUY / HOLD / SELL** recommendation.

---

## 📁 Folder Structure

```
Stock research Agent/
│
├── backend/                    ← FastAPI Python backend
│   ├── main.py                 ← App entry point
│   ├── requirements.txt        ← Python dependencies
│   ├── agents/
│   │   ├── technical_agent.py  ← RSI, MACD, Moving Average analysis
│   │   ├── fundamental_agent.py← PE ratio, Revenue, EPS analysis
│   │   ├── sentiment_agent.py  ← News sentiment analysis
│   │   └── master_agent.py     ← Combines all agent signals
│   ├── services/
│   │   ├── stock_service.py    ← Mock stock data provider
│   │   ├── news_service.py     ← Mock news headlines provider
│   │   └── cache_service.py    ← In-memory result caching
│   ├── models/
│   │   └── schemas.py          ← Pydantic data models
│   └── api/
│       └── routes.py           ← FastAPI endpoint definitions
│
└── frontend/                   ← React + Vite + Tailwind frontend
    ├── src/
    │   ├── main.jsx            ← React entry point
    │   ├── App.jsx             ← Main app component
    │   ├── api.js              ← Axios API client
    │   ├── index.css           ← Global styles + animations
    │   └── components/
    │       ├── Header.jsx          ← Navigation header
    │       ├── SearchBar.jsx       ← Stock symbol search
    │       ├── KpiCards.jsx        ← Summary metric cards
    │       ├── AgentCard.jsx       ← Individual agent result card
    │       ├── RecommendationCard.jsx ← Final BUY/HOLD/SELL card
    │       ├── StockInfoCard.jsx   ← Stock price + chart
    │       ├── MiniChart.jsx       ← SVG line chart
    │       └── ArchitecturePage.jsx← System architecture diagram
    └── tailwind.config.js      ← Tailwind theme configuration
```

---

## ⚡ Quick Start

### Step 1 — Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Start the FastAPI Backend

```bash
cd backend
python main.py
```

The backend will start at: **http://localhost:8000**  
Visit **http://localhost:8000/docs** for interactive API documentation.

### Step 3 — Install Frontend Dependencies

Open a **new terminal** (keep backend running):

```bash
cd frontend
npm install
```

### Step 4 — Start the React Frontend

```bash
cd frontend
npm run dev
```

The frontend will start at: **http://localhost:5173**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Welcome message |
| `GET`  | `/api/health` | Health check |
| `POST` | `/api/analyze` | Run full multi-agent analysis |
| `GET`  | `/api/stock/{symbol}` | Get raw stock data + chart |

### Example: Analyze AAPL

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'
```

---

## 🤖 How the Agents Work

```
User Input (e.g. "AAPL")
       ↓
Market Data Service (price, RSI, MACD, news)
       ↓
┌──────────────────┬──────────────────┬──────────────────┐
│ Technical Agent  │Fundamental Agent │ Sentiment Agent  │
│ RSI + MACD + MA  │ PE + Revenue+EPS │  News Headlines  │
└──────────────────┴──────────────────┴──────────────────┘
       ↓
Master Agent (combines all signals)
       ↓
Final Decision: BUY / HOLD / SELL
```

---

## 🎨 UI Features

- **Dark Theme** — Deep navy/purple background
- **Purple + Cyan Accents** — Gradient text and borders
- **Animated Cards** — Fade-in with stagger delays
- **Confidence Bars** — Animated progress bars
- **SVG Mini Chart** — Pure SVG, zero dependencies
- **Architecture Page** — Interactive workflow diagram

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite |
| Styling | Tailwind CSS v3 |
| HTTP Client | Axios |
| Backend | FastAPI (Python) |
| Server | Uvicorn |
| Validation | Pydantic v2 |

---

## 🔑 Adding a Real AI (OpenRouter)

To use a real AI model instead of mock data, add this to your `.env`:

```env
OPENROUTER_API_KEY=your-key-here
```

Then in any agent file, replace the scoring logic with an API call:

```python
import os, httpx

async def call_ai(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "Mock response — add OPENROUTER_API_KEY to enable AI"
    
    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()["choices"][0]["message"]["content"]
```

---

> ⚠️ **Disclaimer**: For educational purposes only. Not financial advice.
