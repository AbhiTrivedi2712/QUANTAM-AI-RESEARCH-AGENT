// StockInfoCard.jsx — Shows basic stock info (price, change, market cap)
// Displayed at the top of results to give context before the agent analysis.

import React from "react";
import MiniChart from "./MiniChart";

function StockInfoCard({ symbol, stockInfo }) {
  // stockInfo comes from GET /api/stock/{symbol}
  const { stock, timeframes } = stockInfo || {};

  if (!stock) return null;

  const isPositive = stock.change >= 0;
  const isIndian = stock.symbol && (stock.symbol.endsWith(".NS") || stock.symbol.endsWith(".BO") || stock.symbol.endsWith(".ns") || stock.symbol.endsWith(".bo"));
  const currencySymbol = isIndian ? "₹" : "$";

  return (
    <div className="quantum-card mb-6 fade-in-up">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* ── Left: Company Info ──────────────────────────────────────────── */}
        <div>
          <div className="flex items-center gap-3 mb-1">
            {/* Stock symbol chip */}
            <span className="font-mono font-bold text-2xl gradient-text">
              {stock.symbol}
            </span>
            <span className={`text-sm font-semibold px-2 py-0.5 rounded-md ${
              isPositive ? "bg-emerald-500/20 text-emerald-400" : "bg-red-500/20 text-red-400"
            }`}>
              {isPositive ? "+" : ""}{stock.change_pct}%
            </span>
          </div>
          <p className="text-slate-400 text-sm">{stock.name}</p>

          {/* Price */}
          <div className="flex items-end gap-2 mt-2">
            <span className="text-3xl font-bold text-white">{currencySymbol}{stock.price}</span>
            <span className={`text-sm mb-1 ${isPositive ? "text-emerald-400" : "text-red-400"}`}>
              {isPositive ? "▲" : "▼"} {currencySymbol}{Math.abs(stock.change)}
            </span>
          </div>
        </div>

        {/* ── Middle: Quick Stats ──────────────────────────────────────────── */}
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-slate-500 text-xs">Market Cap</p>
            <p className="text-white font-semibold">{stock.market_cap}</p>
          </div>
          <div>
            <p className="text-slate-500 text-xs">P/E Ratio</p>
            <p className="text-white font-semibold">{stock.pe_ratio}x</p>
          </div>
          <div>
            <p className="text-slate-500 text-xs">Volume</p>
            <p className="text-white font-semibold">
              {(stock.volume / 1_000_000).toFixed(1)}M
            </p>
          </div>
          <div>
            <p className="text-slate-500 text-xs">RSI</p>
            <p className={`font-semibold ${
              stock.rsi > 70 ? "text-red-400" : stock.rsi < 30 ? "text-emerald-400" : "text-white"
            }`}>{stock.rsi}</p>
          </div>
          <div>
            <p className="text-slate-500 text-xs">MACD</p>
            <p className={`font-semibold ${stock.macd > 0 ? "text-emerald-400" : "text-red-400"}`}>
              {stock.macd > 0 ? "+" : ""}{stock.macd}
            </p>
          </div>
          <div>
            <p className="text-slate-500 text-xs">MA 50d</p>
            <p className="text-white font-semibold">{currencySymbol}{stock.moving_avg_50}</p>
          </div>
        </div>

        {/* ── Right: Mini Price Chart ──────────────────────────────────────── */}
        <div className="w-full md:w-48">
          <p className="text-slate-500 text-xs mb-1">7-Day Trend</p>
          {timeframes && (
            <MiniChart
              prices={timeframes["1d"] ? timeframes["1d"].slice(-15) : []}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default StockInfoCard;
