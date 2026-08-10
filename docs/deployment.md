# 🚀 Deployment Guide: Quantum Agent

This document explains step-by-step instructions to deploy the **QUANTUM** multi-agent financial platform on **Vercel** (frontend React application) and **Render** (backend FastAPI application).

---

## 🖥️ Frontend: Vercel Hosting

Vercel is the recommended hosting platform for static React (Vite) websites.

### 📋 Prerequisites
* A [Vercel account](https://vercel.com/) linked to your GitHub profile.
* Your repository pushed to GitHub.

### 🚀 Deploy Steps
1. Navigate to the **Vercel Dashboard** and click **Add New** ➔ **Project**.
2. Select and import your `QUANTAM-AI-RESEARCH-AGENT` repository.
3. Configure the following project parameters:
   * **Framework Preset**: `Vite`
   * **Root Directory**: `frontend`
   * **Build Command**: `npm run build`
   * **Output Directory**: `dist`
4. Click **Deploy**. Vercel will build and host your frontend React application.

### 🔧 React Router (SPA) Fallback Configuration
To prevent `404 Not Found` errors when refreshing sub-pages (due to React's client-side routing), create a `vercel.json` file inside the `frontend` folder with the following configuration:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## ⚙️ Backend: Render Web Service

Render is the recommended hosting platform for Python web applications.

### 🚀 Deploy Steps
1. Log in to the **Render Dashboard** and click **New** ➔ **Web Service**.
2. Connect your GitHub repository.
3. Configure the service settings:
   * **Language**: `Python`
   * **Root Directory**: `backend`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000`
     *(Note: Render dynamically assigns a port, usually binding to port `10000` or via `$PORT` environment variable)*

4. Set the following under **Environment Variables**:

| Variable Name | Required | Description |
| :--- | :---: | :--- |
| `GROQ_API_KEY` | **Yes** | Your Groq Cloud API key (used for Llama 3.3 synthesis). |
| `GEMINI_API_KEY` | No | Your Gemini API key (optional fallback for sentiment analysis). |
| `DEMO_MODE` | No | Set to `true` to immediately serve pre-cached analysis reports for supported tickers without invoking LLM/Yfinance. |
| `ALLOWED_ORIGINS` | No | Comma-separated list of approved frontend URLs for CORS compliance. Defaults to local Vite ports if empty. |

5. Click **Deploy Web Service**.

---

## 🔗 Connection Hook (CORS & Base URL)

### 1. Update Frontend API Endpoint
Once Render finishes deployment, note the public web service URL (e.g. `https://quantum-agent-api.onrender.com`).
Update the `BASE_URL` in [frontend/src/api.js](file:///c:/Users/singh/QUANTAM-AI-RESEARCH-AGENT/frontend/src/api.js) to point to your live backend endpoint.

### 2. Configure CORS Allowance
On Render, configure the `ALLOWED_ORIGINS` environment variable to include your live Vercel URL:
```env
ALLOWED_ORIGINS=https://quantum-agent.vercel.app,http://localhost:5173
```
This ensures browser requests from your hosted frontend are accepted by the backend server.
