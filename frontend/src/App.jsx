// App.jsx — The main application component
// This is the root of our React app.
// It manages the main state and decides which page to show.
// We use simple useState hooks — no Redux needed!

import React, { useState } from "react";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import KpiCards from "./components/KpiCards";
import AgentCard from "./components/AgentCard";
import RecommendationCard from "./components/RecommendationCard";
import StockInfoCard from "./components/StockInfoCard";
import ArchitecturePage from "./components/ArchitecturePage";
import { analyzeStock, getStockData } from "./api";

function App() {
  // ── State Variables ────────────────────────────────────────────────────────
  const [currentPage, setCurrentPage] = useState("Dashboard"); // "Dashboard" or "Architecture"
  const [isLoading, setIsLoading]     = useState(false);       // Show loading spinner
  const [error, setError]             = useState(null);         // Error message string
  const [analysisData, setAnalysisData] = useState(null);      // Full analysis response
  const [stockInfoData, setStockInfoData] = useState(null);    // Raw stock + chart data

  // ── Main Search Handler ────────────────────────────────────────────────────
  async function handleSearch(symbol) {
    // Reset state before new search
    setIsLoading(true);
    setError(null);
    setAnalysisData(null);
    setStockInfoData(null);

    try {
      // Fire both requests at the same time using Promise.all
      // This is faster than waiting for one then the other
      const [analysis, stockInfo] = await Promise.all([
        analyzeStock(symbol),    // POST /api/analyze
        getStockData(symbol),    // GET  /api/stock/{symbol}
      ]);

      setAnalysisData(analysis);
      setStockInfoData(stockInfo);
    } catch (err) {
      // Show a friendly error message
      if (err.code === "ERR_NETWORK") {
        setError("Cannot connect to backend. Make sure the FastAPI server is running on port 8000.");
      } else {
        setError(err.response?.data?.detail || "Analysis failed. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen" style={{ background: "linear-gradient(135deg, #0a0a1a 0%, #0d0d25 50%, #0a0a1a 100%)" }}>
      {/* Subtle animated background dots */}
      <div
        className="fixed inset-0 opacity-30 pointer-events-none"
        style={{
          backgroundImage: "radial-gradient(circle at 1px 1px, rgba(124,58,237,0.15) 1px, transparent 0)",
          backgroundSize: "32px 32px",
        }}
      />

      {/* ── Navigation Header ───────────────────────────────────────────── */}
      <Header currentPage={currentPage} setCurrentPage={setCurrentPage} />

      {/* ── Page Content ────────────────────────────────────────────────── */}
      {currentPage === "Architecture" ? (
        <ArchitecturePage />
      ) : (
        <main className="max-w-7xl mx-auto px-6 py-8 relative">

          {/* ── Hero Section ─────────────────────────────────────────────── */}
          <div className="text-center mb-10">
            <h2
              className="text-4xl md:text-5xl font-extrabold gradient-text mb-3"
              style={{ fontFamily: "'Space Grotesk', sans-serif" }}
            >
              AI-Powered Stock Intelligence
            </h2>
            <p className="text-slate-400 text-lg max-w-xl mx-auto">
              Enter any stock symbol to get instant multi-agent analysis from Technical,
              Fundamental, and Sentiment AI agents.
            </p>
          </div>

          {/* ── Search Bar ───────────────────────────────────────────────── */}
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />

          {/* ── Loading State ─────────────────────────────────────────────── */}
          {isLoading && (
            <div className="text-center py-16">
              <div className="inline-flex flex-col items-center gap-4">
                {/* Spinning outer ring */}
                <div className="relative w-16 h-16">
                  <div className="absolute inset-0 rounded-full border-2 border-purple-500/20" />
                  <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-purple-500 spin-slow" />
                  <div className="absolute inset-2 rounded-full border-2 border-transparent border-t-cyan-400 spin-slow" style={{ animationDirection: "reverse" }} />
                </div>
                <div>
                  <p className="text-white font-semibold">Agents Analyzing...</p>
                  <p className="text-slate-500 text-sm mt-1">Running Technical · Fundamental · Sentiment analysis</p>
                </div>
              </div>
            </div>
          )}

          {/* ── Error State ────────────────────────────────────────────────── */}
          {error && !isLoading && (
            <div className="quantum-card border-red-500/30 bg-red-900/10 mb-6">
              <div className="flex items-start gap-3">
                <span className="text-2xl">⚠️</span>
                <div>
                  <p className="text-red-400 font-semibold">Analysis Failed</p>
                  <p className="text-slate-400 text-sm mt-1">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* ── Results ────────────────────────────────────────────────────── */}
          {analysisData && !isLoading && (
            <>
              {/* Stock Info + Chart */}
              {stockInfoData && (
                <StockInfoCard
                  symbol={analysisData.stock}
                  stockInfo={stockInfoData}
                />
              )}

              {/* KPI Summary Cards */}
              <KpiCards data={analysisData} />

              {/* Agent Analysis Cards — 3 columns on large screens */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <AgentCard
                  title="Technical Analysis"
                  icon="📈"
                  verdict={analysisData.technical.trend}
                  confidence={analysisData.technical.confidence}
                  reason={analysisData.technical.reason}
                  delay={0.1}
                />
                <AgentCard
                  title="Fundamental Analysis"
                  icon="🏦"
                  verdict={analysisData.fundamental.fundamental}
                  confidence={analysisData.fundamental.confidence}
                  reason={analysisData.fundamental.reason}
                  delay={0.2}
                />
                <AgentCard
                  title="Sentiment Analysis"
                  icon="📰"
                  verdict={analysisData.sentiment.sentiment}
                  confidence={analysisData.sentiment.confidence}
                  reason={analysisData.sentiment.reason}
                  delay={0.3}
                />
              </div>

              {/* Final Recommendation — full width */}
              <RecommendationCard
                finalDecision={analysisData.final_decision}
                symbol={analysisData.stock}
              />
            </>
          )}

          {/* ── Empty State (no search yet) ──────────────────────────────── */}
          {!analysisData && !isLoading && !error && (
            <div className="text-center py-20">
              <div className="text-6xl mb-4">🤖</div>
              <p className="text-slate-400 text-lg font-medium">Ready to Analyze</p>
              <p className="text-slate-600 text-sm mt-2">
                Enter a stock symbol above or click a quick-select chip to begin
              </p>
            </div>
          )}

        </main>
      )}
    </div>
  );
}

export default App;
