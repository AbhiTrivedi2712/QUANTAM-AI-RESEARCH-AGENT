import React from "react";
import { Cpu, ShieldAlert, Award, AlertTriangle, TrendingUp, Info } from "lucide-react";
import { ResponsiveContainer, PieChart, Pie, Cell } from "recharts";

export default function RecommendationCard({ finalDecision, symbol, technical, fundamental, sentiment }) {
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

  // Verdict style mapper
  function getTheme(bias) {
    const b = bias ? bias.toLowerCase() : "";
    if (b === "bullish" || b === "strong" || b === "positive") return {
      bg: "from-emerald-950/20 to-slate-950/5",
      border: "border-emerald-500/30",
      badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
      icon: "📈",
      glow: "rgba(16, 185, 129, 0.05)",
      text: "text-emerald-400"
    };
    if (b === "bearish" || b === "weak" || b === "negative") return {
      bg: "from-red-950/20 to-slate-950/5",
      border: "border-red-500/30",
      badge: "bg-red-500/10 text-red-400 border-red-500/20",
      icon: "📉",
      glow: "rgba(239, 68, 68, 0.05)",
      text: "text-red-400"
    };
    return {
      bg: "from-amber-950/20 to-slate-950/5",
      border: "border-amber-500/30",
      badge: "bg-amber-500/10 text-amber-400 border-amber-500/20",
      icon: "↔️",
      glow: "rgba(245, 158, 11, 0.05)",
      text: "text-amber-400"
    };
  }

  const theme = getTheme(market_bias);

  // Gauge data for Recharts
  const gaugeData = [
    { value: confidence || 50, fill: market_bias === "Bullish" ? "#10b981" : market_bias === "Bearish" ? "#ef4444" : "#f59e0b" },
    { value: 100 - (confidence || 50), fill: "#13132e" }
  ];

  // Risk meter position helper
  const riskPercent = risk === "Low" ? 20 : risk === "Medium" ? 50 : 80;
  const riskColor = risk === "Low" ? "bg-emerald-400 shadow-emerald-400/50" : risk === "High" ? "bg-red-400 shadow-red-400/50" : "bg-amber-400 shadow-amber-400/50";

  return (
    <div
      className={`rounded-2xl border ${theme.border} bg-gradient-to-br ${theme.bg} p-6 mb-6 fade-in-up relative overflow-hidden`}
      style={{ boxShadow: `0 0 35px ${theme.glow}`, animationDelay: "0.2s" }}
    >
      <div className="absolute -right-24 -top-24 w-64 h-64 rounded-full bg-purple-600/5 blur-3xl pointer-events-none" />

      {/* ── Executive Brief banner ── */}
      <div className="bg-[#040416]/85 border border-[#1e1e4a]/60 rounded-xl p-5 mb-6 shadow-inner relative overflow-hidden">
        <div className="absolute -left-20 -bottom-20 w-44 h-44 rounded-full bg-purple-500/5 blur-3xl pointer-events-none" />
        <div className="flex items-center gap-2 mb-2">
          <span className="w-1.5 h-1.5 rounded-full bg-purple-500 animate-ping" />
          <span className="text-[10px] font-bold uppercase tracking-wider text-purple-400 font-mono">Consolidated Executive Brief</span>
        </div>
        <p className="text-slate-300 text-xs leading-relaxed font-light">{summary}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Consensus Speedometer Gauge */}
        <div className="lg:col-span-4 flex flex-col items-center justify-center text-center p-5 bg-[#03030d]/80 rounded-xl border border-white/5 relative">
          <span className="text-slate-500 font-mono text-[9px] uppercase tracking-wider font-bold">Consensus Conviction Gauge</span>
          <div className={`text-3xl font-black ${theme.text} mt-2 mb-3 font-mono`} style={{ letterSpacing: "1px" }}>
            {market_bias?.toUpperCase()}
          </div>

          {/* Recharts Half-Gauge */}
          <div className="relative w-36 h-36 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={gaugeData}
                  cx="50%"
                  cy="75%"
                  startAngle={180}
                  endAngle={0}
                  innerRadius={55}
                  outerRadius={75}
                  dataKey="value"
                  stroke="none"
                >
                  <Cell />
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute top-[45%] flex flex-col items-center">
              <span className="text-2xl font-black text-white font-mono leading-none">{confidence}%</span>
              <span className="text-[8px] text-slate-500 font-mono uppercase font-bold tracking-wider mt-1">Conviction</span>
            </div>
          </div>

          {/* Risk Level Slider */}
          <div className="w-full mt-4 space-y-2">
            <div className="flex justify-between items-center text-[10px] font-mono">
              <span className="text-slate-500 font-bold uppercase">Consensus Risk</span>
              <span className={`font-bold uppercase ${
                risk === "Low" ? "text-emerald-400" : risk === "High" ? "text-red-400" : "text-amber-400"
              }`}>{risk} RISK</span>
            </div>
            {/* Custom linear slider track */}
            <div className="h-1 rounded-full bg-[#13132d] relative">
              <div 
                className={`absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full ${riskColor} shadow-[0_0_8px] transition-all duration-1000`} 
                style={{ left: `calc(${riskPercent}% - 6px)` }} 
              />
            </div>
          </div>
        </div>

        {/* Dynamic Multi-Agent Debate and consensus stats */}
        <div className="lg:col-span-8 flex flex-col justify-between">
          
          {/* Sub-Agent Debate Panels */}
          {technical && fundamental && sentiment && (
            <div className="bg-[#03030d]/80 rounded-xl border border-white/5 p-4 mb-4">
              <div className="flex items-center gap-1.5 mb-3">
                <Cpu size={12} className="text-purple-400 animate-pulse" />
                <h4 className="text-slate-500 text-[9px] font-bold uppercase tracking-wider font-mono">Agent Consensus debate</h4>
              </div>
              
              <div className="grid grid-cols-3 gap-3 text-center text-xs font-mono">
                <div className="bg-[#060614] p-3 rounded-lg border border-white/5 flex flex-col justify-between">
                  <span className="text-slate-500 text-[9px] block">Technical Agent</span>
                  <span className="text-white font-bold block mt-1">{technical.trend}</span>
                  <span className="text-slate-400 text-[8px] mt-0.5">{technical.confidence}% Conv.</span>
                </div>

                <div className="bg-[#060614] p-3 rounded-lg border border-white/5 flex flex-col justify-between">
                  <span className="text-slate-500 text-[9px] block">Fundamental Agent</span>
                  <span className="text-white font-bold block mt-1">{fundamental.fundamental}</span>
                  <span className="text-slate-400 text-[8px] mt-0.5">{fundamental.confidence}% Conv.</span>
                </div>

                <div className="bg-[#060614] p-3 rounded-lg border border-white/5 flex flex-col justify-between">
                  <span className="text-slate-500 text-[9px] block">Sentiment Agent</span>
                  <span className="text-white font-bold block mt-1">{sentiment.sentiment}</span>
                  <span className="text-slate-400 text-[8px] mt-0.5">{sentiment.confidence}% Conv.</span>
                </div>
              </div>
            </div>
          )}

          {/* Explainable Consensus Formula breakdown */}
          <div className="grid grid-cols-2 gap-4">
            
            {/* Drivers list */}
            <div>
              <h4 className="text-slate-400 text-[9px] font-bold uppercase tracking-wider mb-2 flex items-center gap-1.5 font-mono">
                <span>⚡</span> Consensus Drivers
              </h4>
              <ul className="space-y-1.5">
                {key_drivers && key_drivers.slice(0, 2).map((drv, idx) => (
                  <li key={idx} className="flex gap-2 items-start bg-[#03030d]/50 p-2.5 rounded-lg border border-white/5 font-mono">
                    <span className="text-purple-400">✦</span>
                    <span className="text-[10px] text-slate-300 leading-normal font-light">{drv}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Watchlist Factors */}
            <div>
              <h4 className="text-slate-400 text-[9px] font-bold uppercase tracking-wider mb-2 flex items-center gap-1.5 font-mono">
                <span>📌</span> Watchlist Triggers
              </h4>
              <ul className="space-y-1.5">
                {watchlist_factors && watchlist_factors.slice(0, 2).map((fac, idx) => (
                  <li key={idx} className="flex gap-2 items-start bg-[#03030d]/50 p-2.5 rounded-lg border border-white/5 font-mono">
                    <span className="text-cyan-400">▪</span>
                    <span className="text-[10px] text-slate-300 leading-normal font-light">{fac}</span>
                  </li>
                ))}
              </ul>
            </div>

          </div>

        </div>
      </div>

      {/* Downside Risks & Catalyst sections (Section 13 additions) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6 border-t border-[#1e1e4a]/60 pt-5 text-xs">
        <div>
          <h4 className="text-red-400 text-[9px] font-bold uppercase tracking-wider mb-2.5 flex items-center gap-1.5 font-mono">
            <ShieldAlert size={12} /> Potential Downside Risks
          </h4>
          <ul className="space-y-1.5">
            {potential_risks && potential_risks.slice(0, 2).map((rsk, i) => (
              <li key={i} className="flex gap-2 items-start bg-[#03030d]/40 p-2.5 rounded-lg border border-white/5 font-mono text-[10px]">
                <span className="text-red-400">▪</span>
                <span className="leading-relaxed text-slate-300">{rsk}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="text-emerald-400 text-[9px] font-bold uppercase tracking-wider mb-2.5 flex items-center gap-1.5 font-mono">
            <Award size={12} /> Catalyst Catalyst Events
          </h4>
          <ul className="space-y-1.5">
            {future_catalysts && future_catalysts.slice(0, 2).map((cat, i) => (
              <li key={i} className="flex gap-2 items-start bg-[#03030d]/40 p-2.5 rounded-lg border border-white/5 font-mono text-[10px]">
                <span className="text-emerald-400">✦</span>
                <span className="leading-relaxed text-slate-300">{cat}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Consensus calculation explanation */}
      <div className="mt-6 border-t border-[#1e1e4a]/40 pt-4 text-center">
        <p className="text-[9px] font-mono text-slate-500 flex items-center justify-center gap-1">
          <Info size={10} className="text-purple-400" />
          Consensus Calculation = Technical (40%) + Fundamental (35%) + Sentiment (25%)
        </p>
      </div>
    </div>
  );
}
