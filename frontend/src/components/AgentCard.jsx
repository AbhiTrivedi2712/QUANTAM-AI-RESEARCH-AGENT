// AgentCard.jsx — Displays detailed agent analysis metrics,
// including multi-timeframe trends, strengths/weaknesses, and drivers.
// Upgraded to support Section 6: Agent Explainability widgets.

import React, { useState } from "react";

function AgentCard({ title, icon, verdict, confidence, reason, details, delay = 0 }) {
  const [showExplain, setShowExplain] = useState(false);

  // Verdict styling
  function getVerdictBadge(v) {
    const l = v ? v.toLowerCase() : "";
    if (["bullish", "strong", "positive"].includes(l)) return "badge-bullish";
    if (["bearish", "weak", "negative"].includes(l)) return "badge-bearish";
    return "badge-neutral";
  }

  function getConfColor(c) {
    if (c >= 75) return "text-emerald-400";
    if (c >= 55) return "text-amber-400";
    return "text-red-400";
  }

  const isTech = title.toLowerCase().includes("technical");
  const isFund = title.toLowerCase().includes("fundamental");
  const isSent = title.toLowerCase().includes("sentiment");

  return (
    <div
      className="quantum-card flex flex-col gap-4 fade-in-up"
      style={{ animationDelay: `${delay}s` }}
    >
      {/* ── Card Header ── */}
      <div className="flex items-center gap-3 border-b border-[#1e1e4a]/60 pb-3">
        <div className="w-9 h-9 rounded-xl bg-purple-600/10 border border-purple-500/20 flex items-center justify-center text-lg shadow-inner">
          {icon}
        </div>
        <div>
          <h4 className="font-bold text-white text-sm tracking-wide">{title}</h4>
          <p className="text-slate-500 text-xs">AI Agent Specialist</p>
        </div>
        <span className={`ml-auto badge ${getVerdictBadge(verdict)}`}>
          {verdict}
        </span>
      </div>

      {/* ── Confidence Score ── */}
      <div>
        <div className="flex justify-between items-center mb-1.5">
          <span className="text-slate-500 text-xs font-semibold">Agent Conviction</span>
          <span className={`text-xs font-mono font-bold ${getConfColor(confidence)}`}>
            {confidence}%
          </span>
        </div>
        <div className="confidence-bar">
          <div className="confidence-fill" style={{ width: `${confidence}%` }} />
        </div>
      </div>

      {/* ── Custom Metric Grids (Technical / Fundamental / Sentiment) ── */}
      {isTech && details && (
        <div className="grid grid-cols-2 gap-3 text-xs bg-[#0a0a1a]/40 p-3 rounded-xl border border-[#1e1e4a]/40">
          <div>
            <p className="text-slate-500 font-medium">Trend Strength</p>
            <p className="text-white font-semibold mt-0.5">{details.trend_strength || "N/A"}</p>
          </div>
          <div>
            <p className="text-slate-500 font-medium">Volatility</p>
            <p className="text-white font-semibold mt-0.5">{details.volatility ? `${details.volatility.toFixed(1)}%` : "N/A"}</p>
          </div>
          <div>
            <p className="text-slate-500 font-medium">Support (20d min)</p>
            <p className="text-emerald-400 font-mono font-semibold mt-0.5">${details.support_level?.toFixed(2) || "N/A"}</p>
          </div>
          <div>
            <p className="text-slate-500 font-medium">Resistance (20d max)</p>
            <p className="text-red-400 font-mono font-semibold mt-0.5">${details.resistance_level?.toFixed(2) || "N/A"}</p>
          </div>
          <div>
            <p className="text-slate-500 font-medium">Dist. to Support</p>
            <p className="text-emerald-500/80 font-mono font-semibold mt-0.5">{details.distance_to_support !== undefined ? `${details.distance_to_support}%` : "N/A"}</p>
          </div>
          <div>
            <p className="text-slate-500 font-medium">Dist. to Resistance</p>
            <p className="text-red-500/80 font-mono font-semibold mt-0.5">{details.distance_to_resistance !== undefined ? `${details.distance_to_resistance}%` : "N/A"}</p>
          </div>
          
          {/* Multi-Timeframe Trend Grid */}
          {details.timeframe_analysis && (
            <div className="col-span-2 mt-2 pt-2 border-t border-[#1e1e4a]/45">
              <p className="text-slate-500 font-medium mb-2">Timeframe Trend Structure</p>
              <div className="grid grid-cols-5 gap-1.5 text-center font-mono text-[9px]">
                {Object.entries(details.timeframe_analysis).map(([tf, trend]) => {
                  const isUp = trend.toLowerCase().includes("bullish");
                  const isDown = trend.toLowerCase().includes("bearish");
                  return (
                    <div key={tf} className="bg-[#070715] py-1 rounded border border-[#1d1d40]">
                      <span className="text-slate-400 block font-semibold">{tf}</span>
                      <span className={`font-black mt-0.5 block ${isUp ? "text-emerald-400" : isDown ? "text-red-400" : "text-amber-400"}`}>
                        {trend.replace("Strong ", "S. ")}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {isFund && details && (
        <div className="flex flex-col gap-3">
          <div className="grid grid-cols-3 gap-2 bg-[#0a0a1a]/40 p-2.5 rounded-xl border border-[#1e1e4a]/40 text-[10px] text-center">
            <div>
              <span className="text-slate-500 block">Health</span>
              <span className="text-white font-bold block mt-0.5">{details.health_score}/100</span>
            </div>
            <div>
              <span className="text-slate-500 block">Valuation</span>
              <span className="text-white font-bold block mt-0.5">{details.valuation_score}/100</span>
            </div>
            <div>
              <span className="text-slate-500 block">Growth</span>
              <span className="text-white font-bold block mt-0.5">{details.growth_score}/100</span>
            </div>
          </div>
          
          {/* Strengths & Weaknesses Columns */}
          {details.strengths && details.weaknesses && (
            <div className="grid grid-cols-2 gap-3 text-xs bg-[#0a0a1a]/40 p-3 rounded-xl border border-[#1e1e4a]/40">
              <div className="border-r border-[#1e1e4a]/40 pr-2">
                <p className="text-emerald-400 font-semibold mb-1.5 flex items-center gap-1">
                  <span>✔</span> Strengths
                </p>
                <ul className="list-disc list-inside text-slate-400 leading-normal pl-0.5 space-y-1 text-[9px]">
                  {details.strengths.slice(0, 3).map((str, idx) => (
                    <li key={idx} className="truncate text-slate-300" title={str}>{str}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="text-red-400 font-semibold mb-1.5 flex items-center gap-1">
                  <span>✗</span> Weaknesses
                </p>
                <ul className="list-disc list-inside text-slate-400 leading-normal pl-0.5 space-y-1 text-[9px]">
                  {details.weaknesses.slice(0, 3).map((weak, idx) => (
                    <li key={idx} className="truncate text-slate-300" title={weak}>{weak}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}

      {isSent && details && (
        <div className="flex flex-col gap-3">
          <div className="bg-[#0a0a1a]/40 p-3 rounded-xl border border-[#1e1e4a]/40 text-xs">
            <div className="flex justify-between items-center mb-1.5">
              <span className="text-slate-500">Sentiment Flow</span>
              <span className="font-mono text-[10px] text-white">Consensus Matrix</span>
            </div>
            <div className="flex h-3 rounded-full overflow-hidden w-full font-mono text-[9px] font-bold text-center leading-3">
              <div className="bg-emerald-500/80 text-white" style={{ width: `${(details.positive_ratio * 100) || 0}%` }}>
                {details.positive_ratio > 0.15 ? `${Math.round(details.positive_ratio * 100)}%` : ""}
              </div>
              <div className="bg-[#1e1e4a] text-slate-400" style={{ width: `${((1 - details.positive_ratio - details.negative_ratio) * 100) || 0}%` }}>
              </div>
              <div className="bg-red-500/80 text-white" style={{ width: `${(details.negative_ratio * 100) || 0}%` }}>
                {details.negative_ratio > 0.15 ? `${Math.round(details.negative_ratio * 100)}%` : ""}
              </div>
            </div>
          </div>

          {/* Positive vs Negative Drivers Columns */}
          {details.positive_drivers && details.negative_drivers && (
            <div className="grid grid-cols-2 gap-3 text-xs bg-[#0a0a1a]/40 p-3 rounded-xl border border-[#1e1e4a]/40">
              <div className="border-r border-[#1e1e4a]/40 pr-2">
                <p className="text-emerald-400 font-semibold mb-1.5 flex items-center gap-1">
                  <span>▲</span> Bullish Drivers
                </p>
                <ul className="list-disc list-inside text-slate-400 leading-normal pl-0.5 space-y-1 text-[9px]">
                  {details.positive_drivers.slice(0, 3).map((drv, idx) => (
                    <li key={idx} className="truncate text-slate-300" title={drv}>{drv}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="text-red-400 font-semibold mb-1.5 flex items-center gap-1">
                  <span>▼</span> Bearish Drivers
                </p>
                <ul className="list-disc list-inside text-slate-400 leading-normal pl-0.5 space-y-1 text-[9px]">
                  {details.negative_drivers.slice(0, 3).map((drv, idx) => (
                    <li key={idx} className="truncate text-slate-300" title={drv}>{drv}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── Agent Explanation Summary ── */}
      <div className="bg-[#0a0a1a] rounded-xl p-3 border border-[#1e1e4a] text-xs flex-1">
        <p className="text-slate-500 font-semibold mb-1">Agent Commentary</p>
        <p className="text-slate-300 leading-relaxed font-light text-[11px]">
          {reason || details?.summary}
        </p>
      </div>

      {/* ── SECTION 6: Toggleable Explainability Accoridion ── */}
      <div className="border-t border-[#1e1e4a]/40 pt-2.5">
        <button
          onClick={() => setShowExplain(!showExplain)}
          className="text-xs font-bold text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-1"
        >
          <span>🎓</span> {showExplain ? "Hide Methodology" : "Explain Methodology"}
        </button>

        {showExplain && (
          <div className="mt-2.5 p-3 rounded-lg border border-[#1e1e4a]/60 bg-[#060614] text-[10px] leading-relaxed text-slate-400 space-y-2 fade-in-up">
            {isTech && (
              <>
                <p><strong>SMA channels (50/200 MA)</strong>: Compares short-term and long-term moving averages to determine structural trend direction. A crossover establishes bullish/bearish conviction.</p>
                <p><strong>RSI Momentum (14)</strong>: Assesses speed and price changes to isolate overbought (≥70) or oversold (≤30) conditions.</p>
                <p><strong>MACD Oscillator</strong>: Signals changes in trend strength, direction, momentum, and duration of asset trends.</p>
                <p><strong>Support & Resistance (20-Period)</strong>: Rolled daily local extrema showing buyers/sellers thresholds and distance safety margins.</p>
              </>
            )}
            {isFund && (
              <>
                <p><strong>Financial Health Score</strong>: Weighted analysis of balance sheet solvency metrics, profitability indexes, and size buffer scales.</p>
                <p><strong>Valuation Safety Score</strong>: Compares the Trailing P/E multiplier against index parameters to identify premium ratios or value zones.</p>
                <p><strong>Compound Growth Score</strong>: Evaluates YoY top-line revenue expansions and bottom-line EPS trajectories for fundamental momentum.</p>
              </>
            )}
            {isSent && (
              <>
                <p><strong>Consensus Matrix</strong>: Evaluates volume flow of positive vs negative headlines to quantify market fear/greed bias.</p>
                <p><strong>Driver Keyword Parsing</strong>: Parses news keywords mapping corporate triggers like regulatory reviews, earnings beats, or product rollouts.</p>
              </>
            )}
          </div>
        )}
      </div>

      {/* ── Highlight Tags bottom tags ── */}
      {isTech && details?.signals && details.signals.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-1">
          {details.signals.slice(0, 3).map((sig, i) => (
            <span key={i} className="px-2 py-0.5 bg-purple-900/20 border border-purple-500/10 text-purple-400 text-[9px] rounded">
              ⚡ {sig}
            </span>
          ))}
        </div>
      )}

      {isFund && details?.metrics && (
        <div className="flex flex-wrap gap-1.5 mt-1 text-[9px]">
          {details.metrics.pe_ratio !== null && (
            <span className="px-2 py-0.5 bg-indigo-900/20 border border-indigo-500/10 text-indigo-400 rounded">
              PE: {details.metrics.pe_ratio}x
            </span>
          )}
          <span className="px-2 py-0.5 bg-indigo-900/20 border border-indigo-500/10 text-indigo-400 rounded">
            Rev Growth: {details.metrics.revenue_growth_pct}%
          </span>
          <span className="px-2 py-0.5 bg-indigo-900/20 border border-indigo-500/10 text-indigo-400 rounded">
            Cap: {details.metrics.market_cap}
          </span>
        </div>
      )}

      {isSent && details?.events && details.events.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-1">
          {details.events.slice(0, 3).map((evt, i) => (
            <span key={i} className="px-2 py-0.5 bg-cyan-900/20 border border-cyan-500/10 text-cyan-400 text-[9px] rounded">
              📌 {evt}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export default AgentCard;
