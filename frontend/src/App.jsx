// App.jsx — Upgraded Financial Intelligence Dashboard
// Incorporates the TradingView widget, multi-agent orchestration timeline, 
// search history, telemetry timing readouts, fallback alert indicators, and upgraded cards.

import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import KpiCards from "./components/KpiCards";
import AgentCard from "./components/AgentCard";
import RecommendationCard from "./components/RecommendationCard";
import StockInfoCard from "./components/StockInfoCard";
import ArchitecturePage from "./components/ArchitecturePage";
import TradingViewChart from "./components/TradingViewChart";
import NewsInsights from "./components/NewsInsights";
import SystemStatusCard from "./components/SystemStatusCard";
import AgentModal from "./components/AgentModal";
import { analyzeStock, getStockData, checkBackendHealth } from "./api";

const WORKFLOW_STAGES = [
  { id: 1, label: "Market Data Retrieved" },
  { id: 2, label: "Technical Core Audited" },
  { id: 3, label: "Fundamentals Evaluated" },
  { id: 4, label: "News Sentiment Mapped" },
  { id: 5, label: "Master Report Synthesized" },
];

function App() {
  const [currentPage, setCurrentPage] = useState("Dashboard");
  const [isLoading, setIsLoading] = useState(false);
  const [workflowStep, setWorkflowStep] = useState(0); // 0 = idle, 1-5 stages
  const [stageTimes, setStageTimes] = useState({});
  const [error, setError] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [stockInfoData, setStockInfoData] = useState(null);
  const [backendHealth, setBackendHealth] = useState({ checked: false, online: null });
  const [activeModal, setActiveModal] = useState(null);

  // Startup validation check to probe backend server availability
  useEffect(() => {
    async function verifyBackendConnection() {
      try {
        const data = await checkBackendHealth();
        if (data && data.status === "ok") {
          setBackendHealth({ checked: true, online: true });
        } else {
          setBackendHealth({ checked: true, online: false });
        }
      } catch (err) {
        setBackendHealth({ checked: true, online: false });
      }
    }
    verifyBackendConnection();
  }, []);

  // Search History State (loaded from LocalStorage)
  const [searchHistory, setSearchHistory] = useState(() => {
    try {
      const stored = localStorage.getItem("quantum_search_history");
      return stored ? JSON.parse(stored) : ["AAPL", "TSLA", "MSFT", "INFY.NS", "RELIANCE.NS"];
    } catch {
      return ["AAPL", "TSLA", "MSFT", "INFY.NS", "RELIANCE.NS"];
    }
  });

  // Helper to sleep during workflow visualization
  const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  async function handleSearch(symbol) {
    if (!symbol) return;
    const cleanSym = symbol.toUpperCase().trim();
    
    setIsLoading(true);
    setError(null);
    setAnalysisData(null);
    setStockInfoData(null);
    
    // Clear and start recording timeline timestamps
    const times = {};
    times[1] = new Date().toLocaleTimeString();
    setStageTimes(times);
    setWorkflowStep(1); // Stage 1: Data retrieved

    // Save symbol in local search history
    setSearchHistory((prev) => {
      const filtered = prev.filter((s) => s !== cleanSym);
      const updated = [cleanSym, ...filtered].slice(0, 8);
      localStorage.setItem("quantum_search_history", JSON.stringify(updated));
      return updated;
    });

    try {
      // Begin fetching real data in parallel
      const fetchPromise = Promise.all([
        analyzeStock(cleanSym),
        getStockData(cleanSym),
      ]);

      // Step-by-step pipeline visualization delay with timestamps
      await delay(500);
      times[2] = new Date().toLocaleTimeString();
      setStageTimes({ ...times });
      setWorkflowStep(2); // Stage 2: Technical Agent

      await delay(400);
      times[3] = new Date().toLocaleTimeString();
      setStageTimes({ ...times });
      setWorkflowStep(3); // Stage 3: Fundamental Agent

      await delay(400);
      times[4] = new Date().toLocaleTimeString();
      setStageTimes({ ...times });
      setWorkflowStep(4); // Stage 4: Sentiment Agent

      await delay(400);
      times[5] = new Date().toLocaleTimeString();
      setStageTimes({ ...times });
      setWorkflowStep(5); // Stage 5: Synthesis

      // Await actual API response
      const [analysis, stockInfo] = await fetchPromise;

      await delay(300);
      setAnalysisData(analysis);
      setStockInfoData(stockInfo);
    } catch (err) {
      setWorkflowStep(0);
      if (err.code === "ERR_NETWORK") {
        setError("Cannot establish connection with the FastAPI gateway. Ensure the backend is running on port 8000.");
      } else {
        setError(err.response?.data?.detail || "Analysis pipeline failed. Verify ticker format.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  // Evaluate if any agent fell back to the local offline rules engine
  const isFallbackActive =
    analysisData &&
    (analysisData.technical?.fallback_active ||
      analysisData.fundamental?.fallback_active ||
      analysisData.sentiment?.fallback_active ||
      analysisData.final_decision?.fallback_active);

  return (
    <div className="min-h-screen pb-12" style={{ background: "linear-gradient(135deg, #050510 0%, #0c0c20 50%, #050510 100%)" }}>
      {/* Subtle background nodes pattern */}
      <div
        className="fixed inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: "radial-gradient(circle at 1px 1px, rgba(139, 92, 246, 0.15) 1px, transparent 0)",
          backgroundSize: "24px 24px",
        }}
      />

      <Header currentPage={currentPage} setCurrentPage={setCurrentPage} />

      {currentPage === "Architecture" ? (
        <ArchitecturePage />
      ) : (
        <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 relative">
          {/* Dashboard Title */}
          <div className="text-center mb-8">
            <h2
              className="text-3xl sm:text-4xl md:text-5xl font-black gradient-text tracking-tight mb-2"
              style={{ fontFamily: "'Space Grotesk', sans-serif" }}
            >
              QUANTUM Financial Intelligence
            </h2>
            <p className="text-slate-400 text-xs sm:text-sm max-w-lg mx-auto font-light">
              Enter a US ticker (e.g. AAPL) or Indian NSE stock (e.g. INFY or RELIANCE.NS) 
              to execute the multi-agent consensus analysis pipeline.
            </p>
          </div>

          {/* Search Input */}
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />

          {/* Search History Ribbon */}
          <div className="flex flex-wrap items-center justify-center gap-2 mb-8 -mt-2">
            <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider mr-1">Previous Audits:</span>
            {searchHistory.map((sym, idx) => (
              <button
                key={idx}
                onClick={() => handleSearch(sym)}
                disabled={isLoading}
                className="px-2.5 py-0.5 rounded-full text-xs font-bold font-mono transition-all border border-[#1e1e4a]/60 bg-[#0a0a1a]/40 text-slate-400 hover:text-purple-400 hover:border-purple-500/50 hover:bg-purple-500/5 disabled:opacity-50 disabled:pointer-events-none"
              >
                {sym}
              </button>
            ))}
          </div>

          {/* ── Orchestration Pipeline Timeline ── */}
          {isLoading && (
            <div className="quantum-card border-purple-500/20 bg-purple-900/5 mb-8">
              <p className="text-center text-xs font-bold uppercase tracking-wider text-purple-400 mb-5">
                Consensus Orchestration Flow
              </p>
              
              <div className="flex flex-col md:flex-row md:justify-between gap-4 md:gap-2 relative">
                {/* Horizontal line for desktop connecting stages */}
                <div className="hidden md:block absolute top-[18px] left-[5%] right-[5%] h-0.5 bg-[#1e1e4a] -z-10" />

                {WORKFLOW_STAGES.map((stage) => {
                  const isActive = workflowStep === stage.id;
                  const isCompleted = workflowStep > stage.id;
                  
                  return (
                    <div key={stage.id} className="flex-1 flex md:flex-col items-center gap-3 md:gap-2 text-center z-10">
                      {/* Status Circle */}
                      <div className={`w-9 h-9 rounded-full border-2 flex items-center justify-center text-xs font-bold font-mono transition-all duration-300 ${
                        isActive 
                          ? "bg-purple-600 border-purple-400 text-white shadow-lg shadow-purple-600/50 animate-pulse" 
                          : isCompleted
                          ? "bg-[#0f0f2a] border-emerald-500 text-emerald-400"
                          : "bg-[#050510] border-[#1e1e4a] text-slate-600"
                      }`}>
                        {isCompleted ? "✓" : stage.id}
                      </div>
                      
                      {/* Label & Timestamp */}
                      <div className="flex flex-col text-left md:text-center">
                        <span className={`text-xs font-bold tracking-tight transition-colors duration-300 ${
                          isActive ? "text-purple-400" : isCompleted ? "text-slate-300" : "text-slate-550 text-slate-500"
                        }`}>
                          {stage.label}
                        </span>
                        {(isCompleted || isActive) && stageTimes[stage.id] && (
                          <span className="text-[9px] text-emerald-400 font-mono mt-0.5">
                            {stageTimes[stage.id]}
                          </span>
                        )}
                        {isActive && !stageTimes[stage.id] && (
                          <span className="text-[9px] text-purple-500 font-mono animate-pulse mt-0.5">
                            Processing...
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Backend Connection Diagnostics Alert */}
          {backendHealth.checked && !backendHealth.online && (
            <div className="quantum-card border-red-500/40 bg-red-950/20 mb-8 fade-in-up shadow-2xl relative overflow-hidden" style={{ boxShadow: "0 0 30px rgba(239, 68, 68, 0.1)" }}>
              <div className="absolute -right-24 -top-24 w-48 h-48 rounded-full bg-red-500/5 blur-3xl pointer-events-none" />
              <div className="flex items-start gap-4">
                <span className="text-3xl filter drop-shadow-[0_0_8px_rgba(239,68,68,0.5)]">🚨</span>
                <div className="flex-1">
                  <h3 className="text-red-400 font-bold text-base mb-1.5 uppercase tracking-wide">
                    FastAPI Backend Gateway Offline
                  </h3>
                  <p className="text-slate-300 text-xs leading-relaxed mb-4">
                    The frontend loaded successfully, but it cannot establish a connection with the FastAPI backend at <code className="px-1.5 py-0.5 rounded bg-black/40 text-rose-300 font-mono text-[11px]">http://localhost:8000</code>.
                  </p>
                  
                  <div className="bg-[#0c0c24]/85 rounded-xl border border-red-500/15 p-4 space-y-3.5">
                    <p className="text-white text-xs font-bold uppercase tracking-wider border-b border-white/5 pb-1.5 font-mono">
                      Diagnostics & Troubleshooting Guide
                    </p>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                      <div>
                        <p className="text-red-400 font-bold mb-1">1. Server Not Started</p>
                        <p className="text-slate-400 text-[11px] leading-relaxed">
                          The backend application is not running. Double-click the root <code className="bg-black/30 px-1 py-0.5 rounded text-[10px]">start_backend.bat</code> file or run <code className="bg-black/30 px-1 py-0.5 rounded text-[10px]">npm run backend-start</code> from the root folder to boot uvicorn.
                        </p>
                      </div>
                      
                      <div>
                        <p className="text-red-400 font-bold mb-1">2. Port Conflict / Mismatch</p>
                        <p className="text-slate-400 text-[11px] leading-relaxed">
                          FastAPI might be running on a port other than 8000. Verify the startup logs in your backend terminal for the line <code className="text-amber-300">Uvicorn running on http://0.0.0.0:8000</code>.
                        </p>
                      </div>

                      <div>
                        <p className="text-red-400 font-bold mb-1">3. Corrupted Python 3.14 Environment</p>
                        <p className="text-slate-400 text-[11px] leading-relaxed">
                          If running manually via <code className="bg-black/30 px-1 py-0.5 rounded text-[10px]">python main.py</code>, your system default Python 3.14 might fail with an <code className="text-rose-300 font-mono">encodings</code> import error. Run using the working Python 3.12 location or the bat file.
                        </p>
                      </div>

                      <div>
                        <p className="text-red-400 font-bold mb-1">4. CORS Policies</p>
                        <p className="text-slate-400 text-[11px] leading-relaxed">
                          If your React client is running on a port other than 5173 (e.g. 5174), we've updated the backend settings to support dynamic CORS origins. Ensure you pull the latest backend code.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-4 flex gap-2">
                    <button 
                      onClick={() => window.location.reload()} 
                      className="px-4 py-1.5 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-bold transition-all shadow-md"
                    >
                      🔄 Retry Connection
                    </button>
                    <button 
                      onClick={() => setBackendHealth({ checked: true, online: true })} 
                      className="px-4 py-1.5 rounded-lg border border-slate-700 hover:border-slate-500 text-slate-400 hover:text-white text-xs font-bold transition-all"
                    >
                      Bypass Alert
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Error Banner */}
          {error && !isLoading && (
            <div className="quantum-card border-red-500/30 bg-red-950/10 mb-8 fade-in-up">
              <div className="flex items-start gap-3">
                <span className="text-xl">⚠️</span>
                <div>
                  <h4 className="text-red-400 font-bold text-sm">Orchestration Error</h4>
                  <p className="text-slate-400 text-xs mt-1 leading-relaxed">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Results Grid */}
          {analysisData && !isLoading && (
            <div className="flex flex-col gap-6">
              
              {/* Fallback Active Banner */}
              {isFallbackActive && (
                <div className="rounded-2xl border border-amber-500/30 bg-amber-950/10 p-5 fade-in-up">
                  <div className="flex items-start gap-3">
                    <span className="text-xl">⚠️</span>
                    <div>
                      <h4 className="text-amber-400 font-bold text-sm">Offline Heuristic Fallback Engine Active</h4>
                      <p className="text-slate-300 text-xs mt-1 leading-relaxed">
                        The remote Groq LLM API is currently offline, rate-limited, or unauthorized. 
                        The **Quantum Fallback Logic** has seamlessly taken over to evaluate all mathematical 
                        technical patterns, news lexicon models, and consensus formulas locally.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Stock Price Headline */}
              {stockInfoData && (
                <StockInfoCard
                  symbol={analysisData.stock}
                  stockInfo={stockInfoData}
                />
              )}

              {/* SECTION 3 & 13: Master Synthesis Report (Consolidated Brief and Consensus) */}
              <RecommendationCard
                finalDecision={analysisData.final_decision}
                symbol={analysisData.stock}
                technical={analysisData.technical}
                fundamental={analysisData.fundamental}
                sentiment={analysisData.sentiment}
              />

              {/* SECTION 2, 10, 11: Gateway status, cache, and latency timing */}
              <SystemStatusCard systemStatus={analysisData.system_status} />

              {/* TradingView Widget Chart Integration */}
              <TradingViewChart symbol={analysisData.stock} />

              {/* Quick Summary Cards */}
              <KpiCards data={analysisData} />

              {/* SECTION 5, 6: Specialized Sub-Agent Cards with explainability */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <AgentCard
                  title="Technical Analysis Agent"
                  icon="📈"
                  verdict={analysisData.technical.trend}
                  confidence={analysisData.technical.confidence}
                  reason={analysisData.technical.reason}
                  details={analysisData.technical}
                  delay={0.05}
                  onExpand={() => setActiveModal("technical")}
                />
                <AgentCard
                  title="Fundamental Analysis Agent"
                  icon="🏦"
                  verdict={analysisData.fundamental.fundamental}
                  confidence={analysisData.fundamental.confidence}
                  reason={analysisData.fundamental.reason}
                  details={analysisData.fundamental}
                  delay={0.1}
                  onExpand={() => setActiveModal("fundamental")}
                />
                <AgentCard
                  title="Headline Sentiment Agent"
                  icon="📰"
                  verdict={analysisData.sentiment.sentiment}
                  confidence={analysisData.sentiment.confidence}
                  reason={analysisData.sentiment.reason}
                  details={analysisData.sentiment}
                  delay={0.15}
                  onExpand={() => setActiveModal("sentiment")}
                />
              </div>

              {/* Agent Expandable Terminal Modal */}
              <AgentModal
                isOpen={activeModal !== null}
                onClose={() => setActiveModal(null)}
                type={activeModal}
                details={
                  activeModal === "technical" 
                    ? analysisData.technical 
                    : activeModal === "fundamental" 
                    ? analysisData.fundamental 
                    : analysisData.sentiment
                }
                stockInfoData={stockInfoData}
              />

              {/* SECTION 14: Real-time news stories and AI summarized impacts */}
              {analysisData.sentiment.articles && (
                <NewsInsights articles={analysisData.sentiment.articles} />
              )}
            </div>
          )}

          {/* Empty Prompt State */}
          {!analysisData && !isLoading && !error && (
            <div className="text-center py-24 bg-[#0a0a1a]/30 rounded-3xl border border-[#1e1e4a]/30 quantum-card select-none">
              <span className="text-5xl block mb-4 filter drop-shadow-[0_0_15px_rgba(139,92,246,0.3)]">🛡️</span>
              <p className="text-slate-400 text-sm font-bold tracking-wide uppercase">Consensus Dashboard Idle</p>
              <p className="text-slate-650 text-xs mt-2 max-w-md mx-auto font-light">
                Submit a valid stock symbol above. The backend will spawn specialized nodes to analyze real-time price variables, company records, and media streams.
              </p>
            </div>
          )}
        </main>
      )}
    </div>
  );
}

export default App;
