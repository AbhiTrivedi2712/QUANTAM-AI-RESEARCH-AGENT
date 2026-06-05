// ArchitecturePage.jsx — Shows the agent workflow diagram
// This is a pure CSS/SVG architecture visualization — no external libraries needed.
// Users can understand how data flows through the system.

import React from "react";

// Node definitions for the workflow diagram
const NODES = [
  {
    id: "input",
    label: "User Input",
    sublabel: "Stock Symbol",
    icon: "👤",
    color: "from-slate-700 to-slate-800",
    border: "border-slate-500/40",
  },
  {
    id: "data",
    label: "Market Data",
    sublabel: "Price + News",
    icon: "📊",
    color: "from-blue-900 to-blue-950",
    border: "border-blue-500/40",
  },
  {
    id: "technical",
    label: "Technical Agent",
    sublabel: "RSI · MACD · MA",
    icon: "📈",
    color: "from-purple-900 to-purple-950",
    border: "border-purple-500/40",
  },
  {
    id: "fundamental",
    label: "Fundamental Agent",
    sublabel: "PE · Revenue · EPS",
    icon: "🏦",
    color: "from-indigo-900 to-indigo-950",
    border: "border-indigo-500/40",
  },
  {
    id: "sentiment",
    label: "Sentiment Agent",
    sublabel: "News · Headlines",
    icon: "📰",
    color: "from-cyan-900 to-cyan-950",
    border: "border-cyan-500/40",
  },
  {
    id: "master",
    label: "Master Agent",
    sublabel: "Signal Aggregator",
    icon: "🧠",
    color: "from-violet-900 to-violet-950",
    border: "border-violet-500/40",
  },
  {
    id: "output",
    label: "Final Decision",
    sublabel: "BUY / HOLD / SELL",
    icon: "🎯",
    color: "from-emerald-900 to-emerald-950",
    border: "border-emerald-500/40",
  },
];

// Arrow component — simple SVG down arrow
function Arrow() {
  return (
    <div className="flex justify-center my-1">
      <div className="flex flex-col items-center text-purple-500/60">
        <div className="w-px h-4 bg-gradient-to-b from-purple-500/60 to-purple-500/20" />
        <span className="text-xs">▼</span>
      </div>
    </div>
  );
}

// Node card component
function Node({ node, delay = 0 }) {
  return (
    <div
      className={`rounded-xl border ${node.border} bg-gradient-to-br ${node.color}
                  px-5 py-3 flex items-center gap-3 node-float`}
      style={{
        animationDelay: `${delay}s`,
        boxShadow: "0 0 20px rgba(124, 58, 237, 0.1)",
      }}
    >
      <span className="text-2xl">{node.icon}</span>
      <div>
        <p className="text-white font-semibold text-sm">{node.label}</p>
        <p className="text-slate-400 text-xs">{node.sublabel}</p>
      </div>
    </div>
  );
}

function ArchitecturePage() {
  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* ── Page Header ────────────────────────────────────────────────────── */}
      <div className="mb-10 text-center">
        <h2 className="text-3xl font-bold gradient-text mb-2">System Architecture</h2>
        <p className="text-slate-400 text-sm max-w-xl mx-auto">
          QUANTUM AGENT uses a multi-agent pipeline where specialized AI agents analyze
          different aspects of a stock and a Master Agent combines their signals.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

        {/* ── Left: Flow Diagram ──────────────────────────────────────────── */}
        <div className="quantum-card">
          <h3 className="text-white font-semibold mb-6 flex items-center gap-2">
            <span>🔄</span> Agent Pipeline Flow
          </h3>

          {/* Vertical flow diagram */}
          <div className="max-w-xs mx-auto">
            {/* Step 1: User Input */}
            <Node node={NODES[0]} delay={0} />
            <Arrow />

            {/* Step 2: Market Data */}
            <Node node={NODES[1]} delay={0.1} />
            <Arrow />

            {/* Step 3: Three agents in a row — shown as a split */}
            <div className="text-center mb-1">
              <p className="text-slate-500 text-xs">Parallel analysis</p>
            </div>
            <div className="grid grid-cols-3 gap-2 mb-1">
              {NODES.slice(2, 5).map((node, i) => (
                <div
                  key={node.id}
                  className={`rounded-xl border ${node.border} bg-gradient-to-br ${node.color}
                               px-2 py-2 text-center node-float`}
                  style={{ animationDelay: `${0.2 + i * 0.1}s` }}
                >
                  <span className="text-xl block">{node.icon}</span>
                  <p className="text-white text-xs font-semibold leading-tight mt-1">{node.label.split(" ")[0]}</p>
                  <p className="text-slate-500 text-xs">{node.sublabel.split(" ")[0]}</p>
                </div>
              ))}
            </div>
            <Arrow />

            {/* Step 4: Master Agent */}
            <Node node={NODES[5]} delay={0.5} />
            <Arrow />

            {/* Step 5: Final Decision */}
            <Node node={NODES[6]} delay={0.6} />
          </div>
        </div>

        {/* ── Right: Agent Descriptions ───────────────────────────────────── */}
        <div className="space-y-4">
          <div className="quantum-card">
            <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
              <span>🤖</span> Agent Descriptions
            </h3>

            {/* Agent description list */}
            {[
              {
                icon: "📈",
                name: "Technical Agent",
                desc: "Analyzes price indicators: RSI (momentum), MACD (trend direction), and Moving Averages to determine if the stock is trending bullish or bearish.",
                tech: ["RSI", "MACD", "MA-50", "MA-200"],
              },
              {
                icon: "🏦",
                name: "Fundamental Agent",
                desc: "Evaluates company financial health through PE ratio, revenue growth, and earnings growth to determine if the stock is fundamentally strong.",
                tech: ["PE Ratio", "Revenue Growth", "EPS Growth"],
              },
              {
                icon: "📰",
                name: "Sentiment Agent",
                desc: "Reads and classifies recent news headlines to gauge market sentiment — whether news coverage is positive, negative, or neutral.",
                tech: ["News Count", "Sentiment Score", "Source Analysis"],
              },
              {
                icon: "🧠",
                name: "Master Agent",
                desc: "Aggregates results from all three agents using a weighted scoring system to produce the final BUY / HOLD / SELL recommendation.",
                tech: ["Signal Aggregation", "Risk Assessment", "Confidence Scoring"],
              },
            ].map((agent) => (
              <div key={agent.name} className="border-b border-[#1e1e4a] last:border-0 pb-4 last:pb-0 mb-4 last:mb-0">
                <div className="flex items-start gap-3">
                  <span className="text-2xl mt-0.5">{agent.icon}</span>
                  <div className="flex-1">
                    <p className="text-white font-semibold text-sm mb-1">{agent.name}</p>
                    <p className="text-slate-400 text-xs leading-relaxed mb-2">{agent.desc}</p>
                    <div className="flex flex-wrap gap-1">
                      {agent.tech.map((t) => (
                        <span key={t} className="px-2 py-0.5 bg-purple-600/10 border border-purple-500/20
                                                   text-purple-400 text-xs rounded-md">
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* ── Tech Stack Card ─────────────────────────────────────────────── */}
          <div className="quantum-card">
            <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
              <span>⚙️</span> Tech Stack
            </h3>
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: "Frontend", value: "React + Vite", color: "text-cyan-400" },
                { label: "Styling", value: "Tailwind CSS", color: "text-purple-400" },
                { label: "Backend", value: "FastAPI (Python)", color: "text-emerald-400" },
                { label: "Server", value: "Uvicorn", color: "text-amber-400" },
                { label: "HTTP Client", value: "Axios", color: "text-blue-400" },
                { label: "AI Ready", value: "OpenRouter API", color: "text-violet-400" },
              ].map((item) => (
                <div key={item.label} className="bg-[#0a0a1a] rounded-lg p-3 border border-[#1e1e4a]">
                  <p className="text-slate-500 text-xs">{item.label}</p>
                  <p className={`font-semibold text-sm ${item.color}`}>{item.value}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ArchitecturePage;
