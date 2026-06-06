import React, { useState, useEffect } from "react";

function LandingPage({ onStartResearch, onViewArchitecture }) {
  // Counters states
  const [agentsCount, setAgentsCount] = useState(0);
  const [indicatorsCount, setIndicatorsCount] = useState(0);
  const [newsCount, setNewsCount] = useState(0);

  // Animated counters trigger on load
  useEffect(() => {
    const duration = 2000;
    const steps = 50;
    const intervalTime = duration / steps;

    let step = 0;
    const timer = setInterval(() => {
      step++;
      setAgentsCount(Math.min(4, Math.round((4 / steps) * step)));
      setIndicatorsCount(Math.min(50, Math.round((50 / steps) * step)));
      setNewsCount(Math.min(100, Math.round((100 / steps) * step)));

      if (step >= steps) {
        clearInterval(timer);
      }
    }, intervalTime);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="relative min-h-screen bg-[#060816] text-[#f3f4f6] font-sans overflow-hidden">
      {/* ── Background Patterns ── */}
      <div className="absolute inset-0 financial-grid opacity-30 pointer-events-none" />
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] rounded-full bg-blue-500/5 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-10 right-1/4 w-[600px] h-[600px] rounded-full bg-blue-600/5 blur-[150px] pointer-events-none" />

      {/* ── HERO SECTION ── */}
      <section className="max-w-7xl mx-auto px-6 pt-16 pb-20 relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        {/* Left: Headline & Callouts */}
        <div className="lg:col-span-7 flex flex-col gap-6 text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold tracking-wide w-fit font-mono">
            <span>🛡️</span> AGENTIFAI PLATFORM DEEP DIVE
          </div>
          
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-[1.08] text-white" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            AI-Powered <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-blue-300 to-blue-500">
              Financial Research Intelligence
            </span>
          </h1>

          <p className="text-slate-400 text-sm sm:text-base leading-relaxed max-w-xl font-light">
            Institutional-grade market analysis powered by specialized AI agents that evaluate technical trends, company fundamentals, and real-time news sentiment to generate actionable investment research.
          </p>

          <div className="flex flex-wrap gap-4 mt-2">
            <button onClick={onStartResearch} className="btn-primary flex items-center gap-2">
              <span>🚀</span> Start Research
            </button>
            <button onClick={onViewArchitecture} className="btn-secondary flex items-center gap-2">
              <span>📊</span> View Architecture
            </button>
          </div>

          {/* Floating metric widgets */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5 mt-8 border-t border-white/5 pt-8">
            <div className="bg-white/2 border border-white/5 rounded-xl p-3 backdrop-blur-md">
              <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider block">Consensus</span>
              <span className="text-white text-lg font-black font-mono block mt-0.5">92%</span>
              <span className="text-slate-400 text-[10px] font-light">Research Conviction</span>
            </div>
            <div className="bg-white/2 border border-white/5 rounded-xl p-3 backdrop-blur-md">
              <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider block">Orchestrator</span>
              <span className="text-white text-lg font-black font-mono block mt-0.5">4 Nodes</span>
              <span className="text-slate-400 text-[10px] font-light">Specialist AI Agents</span>
            </div>
            <div className="bg-white/2 border border-white/5 rounded-xl p-3 backdrop-blur-md">
              <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider block">Ingestion</span>
              <span className="text-white text-lg font-black font-mono block mt-0.5">Real-Time</span>
              <span className="text-slate-400 text-[10px] font-light">Market Intelligence</span>
            </div>
            <div className="bg-white/2 border border-white/5 rounded-xl p-3 backdrop-blur-md">
              <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider block">Timeframes</span>
              <span className="text-white text-lg font-black font-mono block mt-0.5">15m - 1w</span>
              <span className="text-slate-400 text-[10px] font-light">Multi-Timeframe Audits</span>
            </div>
          </div>
        </div>

        {/* Right: Mockup Panel Visual */}
        <div className="lg:col-span-5 relative flex items-center justify-center">
          <div className="absolute inset-0 bg-blue-500/10 rounded-3xl filter blur-3xl -z-10 animate-pulse" />
          
          <div className="w-full max-w-sm rounded-2xl border border-white/10 bg-slate-950/80 backdrop-blur-xl p-5 shadow-2xl relative overflow-hidden transition-all hover:border-blue-500/30">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-white/5 pb-3.5 mb-4">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-500 shadow-lg shadow-blue-500/50" />
                <span className="text-white font-bold text-xs tracking-wider uppercase font-mono">Quantum Memo Mockup</span>
              </div>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.5 rounded uppercase">AAPL</span>
            </div>

            {/* Core parameters mock */}
            <div className="space-y-3.5">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-500 font-medium">Consensus Bias</span>
                <span className="text-emerald-400 font-bold uppercase tracking-wider bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded text-[10px]">Bullish</span>
              </div>

              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-500 font-medium">Consensus Conviction</span>
                <span className="text-white font-mono font-bold">78%</span>
              </div>

              {/* Progress indicator */}
              <div className="confidence-bar">
                <div className="confidence-fill" style={{ width: "78%" }} />
              </div>

              {/* Agents status layout */}
              <div className="border-t border-white/5 pt-3 mt-2 space-y-2.5 text-[11px] font-mono text-slate-400">
                <div className="flex justify-between items-center bg-white/2 p-2 rounded border border-white/5">
                  <span className="flex items-center gap-1.5">📈 <span className="font-semibold text-white">Technical Node</span></span>
                  <span className="text-emerald-400 font-bold uppercase">Bullish (98%)</span>
                </div>
                <div className="flex justify-between items-center bg-white/2 p-2 rounded border border-white/5">
                  <span className="flex items-center gap-1.5">🏦 <span className="font-semibold text-white">Fundamental Node</span></span>
                  <span className="text-emerald-400 font-bold uppercase">Strong (90%)</span>
                </div>
                <div className="flex justify-between items-center bg-white/2 p-2 rounded border border-white/5">
                  <span className="flex items-center gap-1.5">📰 <span className="font-semibold text-white">Sentiment Node</span></span>
                  <span className="text-slate-400 font-bold uppercase">Neutral (60%)</span>
                </div>
              </div>

              {/* Narrative highlight */}
              <div className="bg-[#050512] rounded-xl border border-white/5 p-3 text-[10px] leading-relaxed text-slate-400 font-light mt-4">
                <span className="text-purple-400 font-bold block mb-0.5 font-mono">🧠 Executive Brief</span>
                Consolidated analysis indicates a bullish posture supported by SMA crossover signals and high profit margins, with balanced media sentiment flow.
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── SECTION 2: HOW IT WORKS ── */}
      <section className="bg-slate-950/40 border-y border-white/5 py-20 relative z-10">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <div className="mb-12">
            <span className="text-blue-400 text-xs font-bold uppercase tracking-wider font-mono block">Workflow In Action</span>
            <h2 className="text-3xl font-black tracking-tight text-white mt-1" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              Consensus Orchestration Flow
            </h2>
            <p className="text-slate-500 text-xs sm:text-sm max-w-md mx-auto mt-2 font-light">
              See the multi-agent consensus validation cycle execute step-by-step to compile institutional market briefs.
            </p>
          </div>

          {/* Steps Timeline Layout */}
          <div className="grid grid-cols-1 md:grid-cols-6 gap-6 relative mt-16 max-w-5xl mx-auto">
            {/* Desktop Connector Line */}
            <div className="hidden md:block absolute top-[28px] left-[8%] right-[8%] h-0.5 bg-slate-800 -z-10" />

            {[
              { num: "01", name: "Market Ingest", icon: "📡", desc: "yfinance stats + Google News RSS feed search" },
              { num: "02", name: "Technical core", icon: "📈", desc: "Local extrema support/resistance, RSI & MA metrics" },
              { num: "03", name: "Fundamentals", icon: "🏦", desc: "Balance sheet safety checks and valuation safety scores" },
              { num: "04", name: "Headline Sentiment", icon: "📰", desc: "Lexicon sentiment ratios and news events filters" },
              { num: "05", name: "Master consensus", icon: "🧠", desc: "40-35-25 weighted scoring matrix aggregation" },
              { num: "06", name: "Executive Report", icon: "🎯", desc: "Downside risks, future catalysts, and market brief outputs" },
            ].map((step, idx) => (
              <div key={idx} className="flex-1 flex flex-col items-center gap-2 group text-center">
                {/* Node circle */}
                <div className="w-14 h-14 rounded-full border border-white/10 bg-slate-950 flex items-center justify-center text-xl font-bold font-mono group-hover:border-blue-500/40 transition-all duration-300 shadow-lg relative">
                  <span>{step.icon}</span>
                  <span className="absolute -bottom-1 -right-1 bg-blue-600 text-[8px] px-1 py-0.5 rounded text-white font-mono">{step.num}</span>
                </div>
                <h4 className="text-white text-xs font-bold mt-2">{step.name}</h4>
                <p className="text-slate-500 text-[10px] max-w-[130px] font-light leading-normal">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── SECTION 3: FEATURES ── */}
      <section className="max-w-7xl mx-auto px-6 py-20 relative z-10">
        <div className="text-center mb-12">
          <span className="text-blue-400 text-xs font-bold uppercase tracking-wider font-mono block">Platform Capabilities</span>
          <h2 className="text-3xl font-black tracking-tight text-white mt-1" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            Platform Feature Set
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {/* Feature 1 */}
          <div className="quantum-card flex flex-col gap-3">
            <span className="text-2xl">📈</span>
            <h3 className="text-white font-bold text-sm tracking-wide">Technical Intelligence</h3>
            <p className="text-slate-400 text-xs font-light leading-relaxed">
              Multi-timeframe trend analysis (15m to 1w) using RSI, MACD, Moving Averages, and rolling local extrema support and resistance bounds.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="quantum-card flex flex-col gap-3">
            <span className="text-2xl">🏦</span>
            <h3 className="text-white font-bold text-sm tracking-wide">Fundamental Intelligence</h3>
            <p className="text-slate-400 text-xs font-light leading-relaxed">
              Automatic valuation scoring, compound growth index evaluations, solvency reviews, and financial health audits.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="quantum-card flex flex-col gap-3">
            <span className="text-2xl">📰</span>
            <h3 className="text-white font-bold text-sm tracking-wide">Sentiment Intelligence</h3>
            <p className="text-slate-400 text-xs font-light leading-relaxed">
              Real-time Google News RSS search crawling with heuristic keyword events and tagged positive/negative sentiment ratio flows.
            </p>
          </div>

          {/* Feature 4 */}
          <div className="quantum-card flex flex-col gap-3">
            <span className="text-2xl">🧠</span>
            <h3 className="text-white font-bold text-sm tracking-wide">Consensus Engine</h3>
            <p className="text-slate-400 text-xs font-light leading-relaxed">
              Aggregates specialized agent outputs using a 40-35-25 weighted average math consensus, mapping risk flags and key catalysts.
            </p>
          </div>
        </div>
      </section>

      {/* ── SECTION 4: LIVE RESEARCH PREVIEW ── */}
      <section className="bg-slate-950/40 border-y border-white/5 py-20 relative z-10">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <div className="mb-12">
            <span className="text-blue-400 text-xs font-bold uppercase tracking-wider font-mono block">Demo Previews</span>
            <h2 className="text-3xl font-black tracking-tight text-white mt-1" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              Live Research Previews
            </h2>
            <p className="text-slate-500 text-xs sm:text-sm max-w-md mx-auto mt-2 font-light">
              Select one of the sample tickers below to jump directly into its live multi-agent consensus report.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
            {[
              { sym: "AAPL", name: "Apple Inc.", desc: "Consolidated Bullish bias supported by 50/200 MA long uptrends.", price: "$307.34", return: "-1.25%", risk: "Medium" },
              { sym: "TSLA", name: "Tesla Inc.", desc: "High volatility parameters counterbalanced by moderate sentiment flows.", price: "$224.50", return: "+2.40%", risk: "High" },
              { sym: "RELIANCE.NS", name: "Reliance Industries", desc: "Indian blue-chip trading near rolling support structures.", price: "₹2,450.15", return: "+0.15%", risk: "Low" },
              { sym: "INFY.NS", name: "Infosys Limited", desc: "Fair value PE valuation scores counter balancing bearish tech trends.", price: "₹1,197.50", return: "-0.32%", risk: "Medium" },
            ].map((stock) => (
              <div 
                key={stock.sym} 
                onClick={() => onStartResearch(stock.sym)}
                className="quantum-card cursor-pointer hover:border-blue-500/40 text-left group flex flex-col justify-between"
              >
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-white font-black font-mono text-sm tracking-wide">{stock.sym}</span>
                    <span className={`text-[9px] font-bold font-mono px-1.5 py-0.5 rounded ${
                      stock.return.startsWith("+") ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/25" : "bg-red-500/10 text-red-400 border border-red-500/25"
                    }`}>
                      {stock.return}
                    </span>
                  </div>
                  <h4 className="text-slate-300 text-xs font-semibold">{stock.name}</h4>
                  <p className="text-slate-500 text-[10px] leading-relaxed font-light mt-2">{stock.desc}</p>
                </div>
                
                <div className="flex justify-between items-center border-t border-white/5 pt-3 mt-4 text-[10px] font-mono">
                  <div>
                    <span className="text-slate-600 block text-[8px] uppercase font-bold">Risk</span>
                    <span className="text-slate-400 font-bold">{stock.risk}</span>
                  </div>
                  <div className="text-right">
                    <span className="text-slate-600 block text-[8px] uppercase font-bold">Price</span>
                    <span className="text-slate-200 font-black">{stock.price}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── SECTION 5: SYSTEM ARCHITECTURE ── */}
      <section className="max-w-7xl mx-auto px-6 py-20 relative z-10 text-center">
        <div className="mb-12">
          <span className="text-blue-400 text-xs font-bold uppercase tracking-wider font-mono block">System Design</span>
          <h2 className="text-3xl font-black tracking-tight text-white mt-1" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            Platform Architecture
          </h2>
        </div>

        <div className="quantum-card max-w-4xl mx-auto p-8 relative">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 items-center font-mono text-xs">
            {/* Frontend */}
            <div className="bg-slate-900/80 p-3 rounded-lg border border-white/5 shadow-md">
              <span className="text-slate-500 text-[8px] uppercase font-bold block">Client UI</span>
              <span className="text-white font-bold block mt-1">React + Tailwind</span>
            </div>
            
            <span className="text-slate-600 text-center select-none font-bold">➔</span>

            {/* API Layer */}
            <div className="bg-slate-900/80 p-3 rounded-lg border border-white/5 shadow-md">
              <span className="text-slate-500 text-[8px] uppercase font-bold block">Backend API</span>
              <span className="text-blue-400 font-bold block mt-1">FastAPI Gateway</span>
            </div>

            <span className="text-slate-600 text-center select-none font-bold">➔</span>

            {/* Agents orchestrator */}
            <div className="bg-[#120b24] p-3 rounded-lg border border-purple-500/25 shadow-md">
              <span className="text-purple-400 text-[8px] uppercase font-bold block">Orchestrator</span>
              <span className="text-purple-300 font-bold block mt-1">Consensus Nodes</span>
            </div>
          </div>

          <div className="flex justify-center my-3 text-slate-600 select-none font-bold">▼</div>

          <div className="grid grid-cols-3 gap-3 font-mono text-[10px] text-slate-400 max-w-xl mx-auto">
            <div className="bg-white/2 p-2.5 rounded border border-white/5">
              <span>📈 Technical Node</span>
            </div>
            <div className="bg-white/2 p-2.5 rounded border border-white/5">
              <span>🏦 Fundamental Node</span>
            </div>
            <div className="bg-white/2 p-2.5 rounded border border-white/5">
              <span>📰 Sentiment Node</span>
            </div>
          </div>

          <div className="flex justify-center my-3 text-slate-600 select-none font-bold">▼</div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center font-mono text-xs max-w-xl mx-auto">
            {/* Consensus */}
            <div className="bg-slate-900/80 p-3 rounded-lg border border-white/5 shadow-md md:col-span-2">
              <span className="text-slate-500 text-[8px] uppercase font-bold block">Consensus Master</span>
              <span className="text-emerald-400 font-bold block mt-1">40-35-25 Consensus Synthesis</span>
            </div>

            <span className="hidden md:block text-slate-650 text-center select-none font-bold">➔</span>

            {/* Output */}
            <div className="bg-[#0b1c18] p-3 rounded-lg border border-emerald-500/25 shadow-md">
              <span className="text-emerald-400 text-[8px] uppercase font-bold block">Output</span>
              <span className="text-emerald-300 font-bold block mt-1">Market Brief Report</span>
            </div>
          </div>
        </div>
      </section>

      {/* ── SECTION 6: WHY QUANTUM AI ── */}
      <section className="bg-slate-950/40 border-t border-white/5 py-20 relative z-10">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <div className="mb-12">
            <span className="text-blue-400 text-xs font-bold uppercase tracking-wider font-mono block font-black">Consensus Statistics</span>
            <h2 className="text-3xl font-black tracking-tight text-white mt-1" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              Quantifiable Intelligence scale
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-4xl mx-auto font-mono">
            <div className="bg-white/2 border border-white/5 p-6 rounded-2xl backdrop-blur-md">
              <span className="text-blue-400 text-4xl font-black block">{agentsCount} Nodes</span>
              <span className="text-slate-500 text-xs font-semibold uppercase tracking-wider block mt-2">AI Agent Nodes</span>
            </div>
            <div className="bg-white/2 border border-white/5 p-6 rounded-2xl backdrop-blur-md">
              <span className="text-blue-400 text-4xl font-black block">{indicatorsCount}+ indicators</span>
              <span className="text-slate-500 text-xs font-semibold uppercase tracking-wider block mt-2">Calculated parameters</span>
            </div>
            <div className="bg-white/2 border border-white/5 p-6 rounded-2xl backdrop-blur-md">
              <span className="text-blue-400 text-4xl font-black block">{newsCount}+ articles</span>
              <span className="text-slate-500 text-xs font-semibold uppercase tracking-wider block mt-2">Daily Feeds Harvester</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-8 text-center text-xs text-slate-600 relative z-10">
        <p>© 2026 QUANTUM AI Financial Intelligence. Built for Capgemini Agentic AI Buildathon.</p>
        <p className="mt-1">For educational demo purposes only. Quantitative analysis contains investment risks.</p>
      </footer>
    </div>
  );
}

export default LandingPage;
