// RecommendationCard.jsx — The final decision card
// This is the most important card — it shows BUY / HOLD / SELL
// with a glowing animated border for visual impact.

import React from "react";

function RecommendationCard({ finalDecision, symbol }) {
  const { recommendation, confidence, risk, summary } = finalDecision;

  // Color scheme based on recommendation
  function getTheme(rec) {
    if (rec === "BUY") return {
      bg: "from-emerald-900/30 to-emerald-900/10",
      border: "border-emerald-500/40",
      badge: "bg-emerald-500 text-white",
      glow: "0 0 40px rgba(16, 185, 129, 0.3)",
      icon: "📈",
      text: "text-emerald-400",
    };
    if (rec === "SELL") return {
      bg: "from-red-900/30 to-red-900/10",
      border: "border-red-500/40",
      badge: "bg-red-500 text-white",
      glow: "0 0 40px rgba(239, 68, 68, 0.3)",
      icon: "📉",
      text: "text-red-400",
    };
    // HOLD
    return {
      bg: "from-amber-900/30 to-amber-900/10",
      border: "border-amber-500/40",
      badge: "bg-amber-500 text-white",
      glow: "0 0 40px rgba(245, 158, 11, 0.3)",
      icon: "↔️",
      text: "text-amber-400",
    };
  }

  const theme = getTheme(recommendation);

  return (
    <div
      className={`rounded-2xl border ${theme.border} bg-gradient-to-br ${theme.bg} p-6 fade-in-up`}
      style={{ boxShadow: theme.glow, animationDelay: "0.4s" }}
    >
      {/* ── Header ────────────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className="text-slate-400 text-sm font-medium">Master Agent Decision</p>
          <h2 className="text-white font-bold text-xl">Final Recommendation</h2>
        </div>
        <span className="text-4xl">{theme.icon}</span>
      </div>

      {/* ── Big Recommendation Text ────────────────────────────────────────── */}
      <div className="text-center py-6">
        {/* Stock symbol */}
        <p className="text-slate-400 text-lg font-mono mb-2">{symbol}</p>

        {/* BUY / HOLD / SELL in huge text */}
        <div className={`text-7xl font-extrabold ${theme.text} mb-2`}
             style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
          {recommendation}
        </div>

        {/* Confidence badge */}
        <span className={`inline-block px-4 py-1.5 rounded-full text-sm font-semibold ${theme.badge}`}>
          {confidence}% Confidence
        </span>
      </div>

      {/* ── Stats Row ──────────────────────────────────────────────────────── */}
      <div className="grid grid-cols-2 gap-4 mb-5">
        <div className="bg-black/20 rounded-xl p-3 text-center">
          <p className="text-slate-500 text-xs mb-1">Confidence Score</p>
          <p className={`text-2xl font-bold ${theme.text}`}>{confidence}%</p>
        </div>
        <div className="bg-black/20 rounded-xl p-3 text-center">
          <p className="text-slate-500 text-xs mb-1">Risk Level</p>
          <p className={`text-2xl font-bold ${
            risk === "Low" ? "text-emerald-400" : risk === "High" ? "text-red-400" : "text-amber-400"
          }`}>{risk}</p>
        </div>
      </div>

      {/* ── Summary Text ───────────────────────────────────────────────────── */}
      <div className="bg-black/20 rounded-xl p-4 border border-white/5">
        <p className="text-xs text-slate-500 mb-1 font-medium">Master Agent Summary</p>
        <p className="text-slate-300 text-sm leading-relaxed">{summary}</p>
      </div>

      {/* ── Disclaimer ─────────────────────────────────────────────────────── */}
      <p className="text-slate-600 text-xs mt-4 text-center">
        ⚠️ For educational purposes only. Not financial advice.
      </p>
    </div>
  );
}

export default RecommendationCard;
