// KpiCards.jsx — Top summary metric cards
// Shows 3 key numbers at a glance: Market Bias, Confidence Score, Risk Level.
// These are the first things a user sees after analysis.

import React from "react";

function KpiCards({ data }) {
  // Extract values from the master agent's final decision
  const { recommendation, confidence, risk } = data.final_decision;

  // Determine color based on recommendation type
  function getRecommendationColor(rec) {
    if (rec === "BUY")  return "text-emerald-400";
    if (rec === "SELL") return "text-red-400";
    return "text-amber-400"; // HOLD
  }

  function getRiskColor(r) {
    if (r === "Low")  return "text-emerald-400";
    if (r === "High") return "text-red-400";
    return "text-amber-400"; // Medium
  }

  // The three KPI card definitions
  const cards = [
    {
      label: "Market Bias",
      value: recommendation,
      icon: recommendation === "BUY" ? "📈" : recommendation === "SELL" ? "📉" : "↔️",
      valueClass: getRecommendationColor(recommendation),
      subtext: `Based on ${data.stock} analysis`,
    },
    {
      label: "Overall Confidence",
      value: `${confidence}%`,
      icon: "🎯",
      valueClass: confidence >= 75 ? "text-emerald-400" : confidence >= 55 ? "text-amber-400" : "text-red-400",
      subtext: "Average across all agents",
    },
    {
      label: "Risk Level",
      value: risk,
      icon: risk === "Low" ? "🛡️" : risk === "High" ? "⚠️" : "⚡",
      valueClass: getRiskColor(risk),
      subtext: "Signal disagreement level",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      {cards.map((card, index) => (
        <div
          key={card.label}
          className="quantum-card fade-in-up"
          style={{ animationDelay: `${index * 0.1}s` }}
        >
          {/* Card header */}
          <div className="flex items-center justify-between mb-3">
            <p className="text-slate-400 text-sm font-medium">{card.label}</p>
            <span className="text-2xl">{card.icon}</span>
          </div>

          {/* Main value — large and prominent */}
          <p className={`text-3xl font-bold ${card.valueClass}`}>
            {card.value}
          </p>

          {/* Subtext */}
          <p className="text-slate-500 text-xs mt-1">{card.subtext}</p>
        </div>
      ))}
    </div>
  );
}

export default KpiCards;
