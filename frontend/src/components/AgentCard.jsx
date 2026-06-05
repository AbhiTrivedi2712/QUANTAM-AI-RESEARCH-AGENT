// AgentCard.jsx — Reusable card for displaying a single agent's result
// Used for Technical, Fundamental, and Sentiment agents.
// Each agent card shows: verdict badge, confidence bar, and reasoning text.

import React from "react";

/**
 * Props:
 *   title      — Agent name, e.g. "Technical Analysis"
 *   icon       — Emoji icon for the agent
 *   verdict    — The main result: "Bullish", "Strong", "Positive", etc.
 *   confidence — 0–100 score from the agent
 *   reason     — Explanation string
 *   delay      — Animation delay (in seconds) for staggered entrance
 */
function AgentCard({ title, icon, verdict, confidence, reason, delay = 0 }) {

  // Determine badge style based on verdict text
  function getBadgeClass(v) {
    const lower = v.toLowerCase();
    if (["bullish", "strong", "positive"].includes(lower)) return "badge-bullish";
    if (["bearish", "weak", "negative"].includes(lower))   return "badge-bearish";
    return "badge-neutral"; // neutral, average, mixed
  }

  // Color for the confidence percentage text
  function getConfidenceColor(c) {
    if (c >= 75) return "text-emerald-400";
    if (c >= 55) return "text-amber-400";
    return "text-red-400";
  }

  return (
    <div
      className="quantum-card fade-in-up"
      style={{ animationDelay: `${delay}s` }}
    >
      {/* ── Card Header ─────────────────────────────────────────────────── */}
      <div className="flex items-center gap-3 mb-5">
        <div className="w-10 h-10 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-xl">
          {icon}
        </div>
        <div>
          <h3 className="font-semibold text-white text-sm">{title}</h3>
          <p className="text-slate-500 text-xs">AI Agent Analysis</p>
        </div>
        {/* Verdict Badge — top right */}
        <div className="ml-auto">
          <span className={`badge ${getBadgeClass(verdict)}`}>
            {verdict}
          </span>
        </div>
      </div>

      {/* ── Confidence Score ─────────────────────────────────────────────── */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-slate-400 text-xs font-medium">Confidence</span>
          <span className={`text-sm font-bold ${getConfidenceColor(confidence)}`}>
            {confidence}%
          </span>
        </div>
        {/* Animated progress bar */}
        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{ width: `${confidence}%` }}
          />
        </div>
      </div>

      {/* ── Reason / Explanation ─────────────────────────────────────────── */}
      <div className="bg-[#0a0a1a] rounded-xl p-3 border border-[#1e1e4a]">
        <p className="text-xs text-slate-400 mb-1 font-medium">Agent Reasoning</p>
        <p className="text-sm text-slate-300 leading-relaxed">{reason}</p>
      </div>
    </div>
  );
}

export default AgentCard;
