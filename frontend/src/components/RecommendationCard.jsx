// RecommendationCard.jsx (Repurposed as Master Synthesis Report)
// Displays the consolidated Master Agent intelligence, executive brief, 
// agent consensus debate panel, confidence/risk breakdowns, watchlist triggers, 
// potential downside risks, and future catalysts.

import React from "react";

function RecommendationCard({ finalDecision, symbol, technical, fundamental, sentiment }) {
  if (!finalDecision) return null;

  const {
    market_bias,
    confidence,
    risk,
    key_drivers,
    watchlist_factors,
    potential_risks = [],
    future_catalysts = [],
    summary,
  } = finalDecision;

  // Bias styling configuration
  function getTheme(bias) {
    const b = bias ? bias.toLowerCase() : "";
    if (b === "bullish" || b === "strong" || b === "positive") return {
      bg: "from-emerald-950/20 to-slate-900/5",
      border: "border-emerald-500/30",
      badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
      glow: "0 0 40px rgba(16, 185, 129, 0.08)",
      icon: "📈",
      text: "text-emerald-400",
    };
    if (b === "bearish" || b === "weak" || b === "negative") return {
      bg: "from-red-950/20 to-slate-900/5",
      border: "border-red-500/30",
      badge: "bg-red-500/10 text-red-400 border-red-500/20",
      glow: "0 0 40px rgba(239, 68, 68, 0.08)",
      icon: "📉",
      text: "text-red-400",
    };
    // Neutral / Average
    return {
      bg: "from-amber-950/20 to-slate-900/5",
      border: "border-amber-500/30",
      badge: "bg-amber-500/10 text-amber-400 border-amber-500/20",
      glow: "0 0 40px rgba(245, 158, 11, 0.08)",
      icon: "↔️",
      text: "text-amber-400",
    };
  }

  const theme = getTheme(market_bias);

  // Math-based parameters for Risk Breakdown
  const techVol = technical?.volatility || 20.0;
  const volRiskLabel = techVol >= 35.0 ? "High" : techVol >= 20.0 ? "Medium" : "Low";

  // Calculate Agreement Rating
  const t_verdict = technical?.trend || "Neutral";
  const f_verdict = fundamental?.fundamental || "Average";
  const s_verdict = sentiment?.sentiment || "Neutral";
  
  function getVerdictScore(v) {
    const l = v.toLowerCase();
    if (["bullish", "strong", "positive"].includes(l)) return 1;
    if (["bearish", "weak", "negative"].includes(l)) return -1;
    return 0;
  }
  
  const scores = [getVerdictScore(t_verdict), getVerdictScore(f_verdict), getVerdictScore(s_verdict)];
  const scoreSpread = Math.max(...scores) - Math.min(...scores);
  const agreementLabel = scoreSpread === 0 ? "High Consensus" : scoreSpread === 1 ? "Moderate Agreement" : "Divergent / Low Consensus";

  const posRatio = sentiment?.positive_ratio || 0.5;
  const newsUncertainty = (posRatio >= 0.45 && posRatio <= 0.55) ? "High Uncertainty" : "Low Uncertainty";

  return (
    <div
      className={`rounded-2xl border ${theme.border} bg-gradient-to-br ${theme.bg} p-6 mb-6 fade-in-up shadow-2xl`}
      style={{ boxShadow: theme.glow, animationDelay: "0.2s" }}
    >
      {/* ── SECTION 3: Executive Brief Card (Top Highlight) ── */}
      <div className="bg-[#0f0f24]/75 rounded-2xl border border-purple-500/20 p-5 mb-6 shadow-inner relative overflow-hidden">
        {/* Subtle decorative glow */}
        <div className="absolute -right-24 -top-24 w-48 h-48 rounded-full bg-purple-500/5 blur-3xl pointer-events-none" />
        
        <div className="flex items-center gap-2 mb-2.5">
          <span className="w-2 h-2 rounded-full bg-purple-500 animate-ping" />
          <span className="text-[10px] font-bold uppercase tracking-wider text-purple-400 font-mono">Consolidated Executive Brief</span>
        </div>
        <p className="text-white text-sm leading-relaxed font-normal">{summary}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 border-b border-[#1e1e4a]/60 pb-6 mb-6">
        {/* Left Column: Bias & Ring Indicator */}
        <div className="lg:col-span-4 flex flex-col items-center justify-center text-center p-5 bg-black/30 rounded-2xl border border-[#1e1e4a]/40">
          <span className="text-slate-500 font-mono text-[10px] uppercase tracking-wider">{symbol} Consensus Bias</span>
          <div className={`text-4xl font-black ${theme.text} mt-2.5 mb-4`} style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            {market_bias}
          </div>
          
          {/* Visual SVG Progress Ring */}
          <div className="relative w-28 h-28 flex items-center justify-center mb-4">
            <svg className="w-full h-full transform -rotate-90">
              <circle cx="56" cy="56" r="46" stroke="#101030" strokeWidth="6" fill="transparent" />
              <circle 
                cx="56" cy="56" r="46" 
                stroke={market_bias === "Bullish" ? "#10b981" : market_bias === "Bearish" ? "#ef4444" : "#f59e0b"} 
                strokeWidth="7" 
                fill="transparent" 
                strokeDasharray="289"
                strokeDashoffset={289 - (289 * (confidence || 50)) / 100}
                strokeLinecap="round"
                className="transition-all duration-1000 ease-out"
              />
            </svg>
            <div className="absolute flex flex-col items-center justify-center">
              <span className="text-2xl font-black text-white font-mono">{confidence}%</span>
              <span className="text-[9px] text-slate-500 font-semibold uppercase">Conviction</span>
            </div>
          </div>

          <div className="text-slate-400 text-xs font-semibold">
            Consensus Risk: <span className={`font-bold ${risk === "Low" ? "text-emerald-400" : risk === "High" ? "text-red-400" : "text-amber-400"}`}>{risk}</span>
          </div>
        </div>

        {/* Right Column: Drivers, Watchlist, Risks, Catalysts */}
        <div className="lg:col-span-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Key Drivers */}
          <div>
            <h4 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-2 flex items-center gap-1.5 font-mono">
              <span className="text-purple-400">⚡</span> Consensus Drivers
            </h4>
            <ul className="text-xs space-y-1.5 text-slate-300">
              {key_drivers && key_drivers.slice(0, 3).map((drv, i) => (
                <li key={i} className="flex gap-2 items-start bg-[#050512]/45 p-2 rounded-lg border border-white/5 font-light">
                  <span className="text-purple-400">✦</span>
                  <span className="leading-relaxed text-[11px]">{drv}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Watchlist Factors */}
          <div>
            <h4 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-2 flex items-center gap-1.5 font-mono">
              <span className="text-cyan-400">📌</span> Watchlist triggers
            </h4>
            <ul className="text-xs space-y-1.5 text-slate-300">
              {watchlist_factors && watchlist_factors.slice(0, 3).map((fct, i) => (
                <li key={i} className="flex gap-2 items-start bg-[#050512]/45 p-2 rounded-lg border border-white/5 font-light">
                  <span className="text-cyan-400">▪</span>
                  <span className="leading-relaxed text-[11px]">{fct}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Potential Risks (Section 13 addition) */}
          <div>
            <h4 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-2 flex items-center gap-1.5 font-mono">
              <span className="text-red-400">⚠️</span> Potential Downside Risks
            </h4>
            <ul className="text-xs space-y-1.5 text-slate-300">
              {potential_risks && potential_risks.slice(0, 3).map((rsk, i) => (
                <li key={i} className="flex gap-2 items-start bg-[#050512]/45 p-2 rounded-lg border border-white/5 font-light">
                  <span className="text-red-400">▪</span>
                  <span className="leading-relaxed text-[11px]">{rsk}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Future Catalysts (Section 13 addition) */}
          <div>
            <h4 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-2 flex items-center gap-1.5 font-mono">
              <span className="text-emerald-400">🚀</span> Future Catalyst Events
            </h4>
            <ul className="text-xs space-y-1.5 text-slate-300">
              {future_catalysts && future_catalysts.slice(0, 3).map((cat, i) => (
                <li key={i} className="flex gap-2 items-start bg-[#050512]/45 p-2 rounded-lg border border-white/5 font-light">
                  <span className="text-emerald-400">✦</span>
                  <span className="leading-relaxed text-[11px]">{cat}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* ── SECTION 4: Agent Debate Panel (Agree/Disagree Matrix) ── */}
      {technical && fundamental && sentiment && (
        <div className="bg-[#050512]/30 p-4 rounded-xl border border-[#1e1e4a]/40 mb-6">
          <h4 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-3 flex items-center gap-1.5 font-mono">
            <span>💬</span> Sub-Agent Debate & Consensus Matrix
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs text-center font-mono">
            {/* Technical node */}
            <div className="bg-black/20 p-2.5 rounded-lg border border-white/5 flex flex-col justify-between">
              <span className="text-slate-500 text-[10px]">Technical Agent</span>
              <span className="text-white font-bold block mt-1">{technical.trend}</span>
              <span className="text-slate-400 text-[9px] mt-0.5">Conviction: {technical.confidence}%</span>
            </div>
            {/* Fundamental node */}
            <div className="bg-black/20 p-2.5 rounded-lg border border-white/5 flex flex-col justify-between">
              <span className="text-slate-500 text-[10px]">Fundamental Agent</span>
              <span className="text-white font-bold block mt-1">{fundamental.fundamental}</span>
              <span className="text-slate-400 text-[9px] mt-0.5">Conviction: {fundamental.confidence}%</span>
            </div>
            {/* Sentiment node */}
            <div className="bg-black/20 p-2.5 rounded-lg border border-white/5 flex flex-col justify-between">
              <span className="text-slate-500 text-[10px]">Sentiment Agent</span>
              <span className="text-white font-bold block mt-1">{sentiment.sentiment}</span>
              <span className="text-slate-400 text-[9px] mt-0.5">Conviction: {sentiment.confidence}%</span>
            </div>
            {/* Master consensus node */}
            <div className="bg-[#120b24] p-2.5 rounded-lg border border-purple-500/25 flex flex-col justify-between">
              <span className="text-purple-400 text-[10px] font-bold">Master Orchestrator</span>
              <span className="text-purple-300 font-bold block mt-1">{market_bias}</span>
              <span className="text-purple-400 text-[9px] mt-0.5">Conviction: {confidence}%</span>
            </div>
          </div>

          <div className="mt-3 text-[10px] text-slate-400 flex items-center gap-1.5 leading-normal">
            <span className="text-purple-400">✦</span>
            <span><strong>Debate Summary:</strong> Agents indicate a status of <strong>{agreementLabel}</strong>. {
              scoreSpread === 0 
                ? "All sub-agents align cleanly on the consensus trajectory." 
                : "Indicators have moderate differences. The Master Agent has synthesized the discrepancy using weighted consensus values."
            }</span>
          </div>
        </div>
      )}

      {/* ── SECTION 7 & 8: Confidence Math & Risk Breakdowns ── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6 border-t border-[#1e1e4a]/60 pt-5 text-xs">
        {/* Confidence Math */}
        <div className="bg-black/25 p-4 rounded-xl border border-white/5">
          <h4 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-3.5 flex items-center gap-1.5 font-mono">
            <span>📊</span> Consensus Confidence Math
          </h4>
          
          <div className="space-y-3 font-mono text-[10px] text-slate-400">
            <div className="flex justify-between border-b border-[#1e1e4a]/40 pb-1.5">
              <span>Technical Weight (40%)</span>
              <span className="text-white">{technical?.confidence || 50} × 0.40 = {Math.round((technical?.confidence || 50) * 0.40)}%</span>
            </div>
            <div className="flex justify-between border-b border-[#1e1e4a]/40 pb-1.5">
              <span>Fundamental Weight (35%)</span>
              <span className="text-white">{fundamental?.confidence || 50} × 0.35 = {Math.round((fundamental?.confidence || 50) * 0.35)}%</span>
            </div>
            <div className="flex justify-between border-b border-[#1e1e4a]/40 pb-1.5">
              <span>Sentiment Weight (25%)</span>
              <span className="text-white">{sentiment?.confidence || 50} × 0.25 = {Math.round((sentiment?.confidence || 50) * 0.25)}%</span>
            </div>
            <div className="flex justify-between pt-1 font-bold text-xs">
              <span className="text-purple-400">Calculated Final Consensus</span>
              <span className="text-purple-300">{confidence}%</span>
            </div>
          </div>
        </div>

        {/* Risk Breakdown parameters */}
        <div className="bg-black/25 p-4 rounded-xl border border-white/5">
          <h4 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-3.5 flex items-center gap-1.5 font-mono">
            <span>📉</span> Consensus Risk Parameter Breakdown
          </h4>
          
          <div className="space-y-3 font-mono text-[10px] text-slate-400">
            <div className="flex justify-between border-b border-[#1e1e4a]/40 pb-1.5">
              <span>Volatility Factor</span>
              <span className={`font-bold ${volRiskLabel === "High" ? "text-red-400" : volRiskLabel === "Medium" ? "text-amber-400" : "text-emerald-400"}`}>
                {volRiskLabel} ({techVol.toFixed(1)}%)
              </span>
            </div>
            <div className="flex justify-between border-b border-[#1e1e4a]/40 pb-1.5">
              <span>Agent Agreement</span>
              <span className="text-white font-bold">{agreementLabel}</span>
            </div>
            <div className="flex justify-between border-b border-[#1e1e4a]/40 pb-1.5">
              <span>Sentiment Uncertainty</span>
              <span className="text-white font-bold">{newsUncertainty}</span>
            </div>
            <div className="flex justify-between pt-1 font-bold text-xs">
              <span className="text-amber-400">Aggregated Consensus Risk</span>
              <span className={`font-bold ${risk === "Low" ? "text-emerald-400" : risk === "High" ? "text-red-400" : "text-amber-400"}`}>
                {risk}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <p className="text-center text-[10px] text-slate-600 mt-6 leading-normal">
        ⚠️ <strong>Regulatory Disclaimer:</strong> This report represents automated quantitative synthesis of market indicators. 
        It does not represent investment advice, recommendation, or offer to buy/sell securities. All decisions require independent validation.
      </p>
    </div>
  );
}

export default RecommendationCard;
