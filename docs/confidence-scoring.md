# 📐 Explainable Confidence Scoring: Quantum Agent

This document explains the mathematical consensus scoring methodology used by the Master Agent to determine the overall **Consensus Confidence** score.

---

## 📐 Weighted Consensus Model

To ensure transparency and prevent LLM confidence score drift or inflation, the Master Agent calculates the overall **Consensus Confidence** mathematically in Python code prior to LLM prompting, using the following weighting matrix:

$$\text{Master Confidence} = (C_{\text{tech}} \times 0.40) + (C_{\text{fund}} \times 0.35) + (C_{\text{sent}} \times 0.25)$$

* **$C_{\text{tech}}$**: Technical conviction score (based on moving average positions and multi-timeframe checks).
* **$C_{\text{fund}}$**: Fundamental conviction score (based on valuation safety, growth rates, and health scores).
* **$C_{\text{sent}}$**: Sentiment conviction score (based on keyword analysis and media story counts).

---

## 📊 Weight Distribution Rationale

The weights are allocated according to institutional risk management guidelines, reflecting the reliability and latency of each analysis layer:

| Agent Specialty | Weight | Core Contribution | Rationale |
| :--- | :---: | :--- | :--- |
| **Technical Analysis** | **40%** | Dictates short-term trend structures, support boundaries, momentum indices, and entry/exit coordinates. | Technical data represents live market pricing and immediate flows, making it the highest priority for timing-sensitive entries. |
| **Fundamental Analysis** | **35%** | Evaluates long-term balance sheet health, solvency ratios, YoY revenue/earnings growth, and P/E multiples. | Fundamentals determine the underlying business quality, establishing a solid floor for valuation and long-term trend direction. |
| **News Sentiment** | **25%** | Analyzes real-time news headlines, corporate events, and sentiment ratio anomalies. | Media flow acts as a catalyst indicator, introducing short-term volatility or reinforcing current trend directions. |

---

## ⚙️ Hallucination Prevention & Integrity Controls

### 1. Pre-Execution Calculation
LLMs are prone to "sentiment drift" and "hallucination"—often generating random confidence numbers (e.g. 95% in one run, 60% in another on the exact same dataset) based on minor changes in prompt phrasing.
- **Fixed Variable Enforcement**: The backend calculates the consensus confidence programmatically in Python **before** calling the LLM.
- **Strict Prompt Guidelines**: The calculated confidence value is passed to the LLM prompt as a read-only variable, instructing the LLM:
  > *Keep the confidence score exactly at `{calculated_confidence}` and do not modify it.*
This guarantees that the displayed score is mathematically driven, explainable, and reproducible.

### 2. Local Fallback Consistency
If the Groq API fails or is offline:
- The backend's heuristic rules engine runs the exact same mathematical formula.
- The user dashboard receives the same confidence score, ensuring consistent reporting regardless of API availability.
