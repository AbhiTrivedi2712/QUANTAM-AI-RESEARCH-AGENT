// TradingViewChart.jsx — Renders an interactive TradingView widget or a custom native chart
// Automatically resolves ticker formats (e.g., RELIANCE.NS -> NSE:RELIANCE)
// Supports interactive timeframe switching: 15m, 1h, 4h, 1d, 1w

import React, { useState, useEffect, useRef } from "react";
import { BarChart3, TrendingUp, Cpu } from "lucide-react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine
} from "recharts";

const TIMEFRAMES = [
  { label: "15m", val: "15" },
  { label: "1h", val: "60" },
  { label: "4h", val: "240" },
  { label: "1d", val: "D" },
  { label: "1w", val: "W" },
];

function TradingViewChart({ 
  symbol, 
  timeframeData, 
  supportPrice, 
  resistancePrice,
  activeTimeframe: propsTimeframe,
  setActiveTimeframe: propsSetTimeframe
}) {
  const [localTimeframe, setLocalTimeframe] = useState("1d");
  const activeTimeframe = propsTimeframe !== undefined ? propsTimeframe : localTimeframe;
  const setActiveTimeframe = propsSetTimeframe !== undefined ? propsSetTimeframe : setLocalTimeframe;
  const containerRef = useRef(null);

  // Check if ticker is Indian to default to the custom native chart
  const isIndian = symbol && (
    symbol.endsWith(".NS") || 
    symbol.endsWith(".BO") || 
    symbol.endsWith(".ns") || 
    symbol.endsWith(".bo")
  );
  
  const [chartMode, setChartMode] = useState(isIndian ? "native" : "tradingview");
  const currencySymbol = isIndian ? "₹" : "$";

  // Map timeframe label to TradingView intervals
  const timeframeMap = {
    "15m": "15",
    "1h": "60",
    "4h": "240",
    "1d": "D",
    "1w": "W",
  };

  // Convert Yahoo Finance symbol (.NS) to TradingView symbol (NSE:)
  function resolveTradingViewSymbol(sym) {
    if (!sym) return "NASDAQ:AAPL";
    const cleanSym = sym.toUpperCase().strip ? sym.toUpperCase().trim() : sym.toUpperCase();
    if (cleanSym.endsWith(".NS")) {
      return `NSE:${cleanSym.replace(".NS", "")}`;
    }
    // Popular US names
    if (["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "META", "NVDA", "NFLX"].includes(cleanSym)) {
      return `NASDAQ:${cleanSym}`;
    }
    return cleanSym;
  }

  const tvSymbol = resolveTradingViewSymbol(symbol);
  const activeInterval = timeframeMap[activeTimeframe] || "D";

  useEffect(() => {
    // Only load the TradingView widget if chartMode is "tradingview"
    if (chartMode !== "tradingview") return;

    const container = containerRef.current;
    if (!container) return;

    // Reset container HTML to clean old widgets
    container.innerHTML = "";

    const widgetId = `tradingview_widget_${Math.random().toString(36).substring(7)}`;
    const widgetDiv = document.createElement("div");
    widgetDiv.id = widgetId;
    widgetDiv.style.width = "100%";
    widgetDiv.style.height = "100%";
    container.appendChild(widgetDiv);

    const loadWidget = () => {
      if (typeof window.TradingView !== "undefined") {
        new window.TradingView.widget({
          autosize: true,
          symbol: tvSymbol,
          interval: activeInterval,
          timezone: "Etc/UTC",
          theme: "dark",
          style: "1",
          locale: "en",
          enable_publishing: false,
          hide_side_toolbar: false,
          allow_symbol_change: true,
          container_id: widgetId,
          studies: ["RSI@tv-basicstudies", "MASimple@tv-basicstudies"],
          loading_screen: { backgroundColor: "#0f0f2a" },
        });
      }
    };

    // Check if script is already present on page
    const scriptId = "tradingview-widget-script";
    let script = document.getElementById(scriptId);

    if (!script) {
      script = document.createElement("script");
      script.id = scriptId;
      script.src = "https://s3.tradingview.com/tv.js";
      script.type = "text/javascript";
      script.async = true;
      script.onload = loadWidget;
      document.head.appendChild(script);
    } else {
      loadWidget();
    }

    return () => {
      if (container) {
        container.innerHTML = "";
      }
    };
  }, [tvSymbol, activeInterval, chartMode]);

  // Format Recharts historical data array
  const activeDataArray = timeframeData ? timeframeData[activeTimeframe] : null;
  const chartData = activeDataArray
    ? activeDataArray.map((price, idx) => ({
        idx,
        Price: price,
      }))
    : [];

  const sPrice = typeof supportPrice === "number" ? supportPrice : parseFloat(supportPrice);
  const rPrice = typeof resistancePrice === "number" ? resistancePrice : parseFloat(resistancePrice);

  return (
    <div className="quantum-card w-full flex flex-col gap-4">
      {/* Chart Header & Toggles */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-[#1e1e4a] pb-3 gap-3">
        <div>
          <h3 className="text-white font-semibold text-sm flex items-center gap-2">
            <BarChart3 size={16} className="text-slate-300" /> {chartMode === "native" ? "Quantum Native Chart" : "TradingView Chart"}
          </h3>
          <p className="text-slate-500 text-xs mt-0.5">
            {chartMode === "native" 
              ? `Interactive custom tracking feed for ${symbol}`
              : `Interactive TradingView widget for ${tvSymbol}`
            }
          </p>
        </div>
        
        {/* Controls block */}
        <div className="flex flex-wrap gap-2 items-center">
          {/* Chart Mode Toggle */}
          <div className="flex gap-1 bg-[#0a0a1a] p-1 rounded-lg border border-[#1e1e4a]">
            <button
              onClick={() => setChartMode("native")}
              className={`px-3 py-1 text-[11px] font-semibold rounded-md transition-all duration-200 flex items-center gap-1 cursor-pointer ${
                chartMode === "native"
                  ? "bg-[#FFBA9D] text-black shadow-md font-bold"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <Cpu size={12} /> Native
            </button>
            <button
              onClick={() => setChartMode("tradingview")}
              className={`px-3 py-1 text-[11px] font-semibold rounded-md transition-all duration-200 flex items-center gap-1 cursor-pointer ${
                chartMode === "tradingview"
                  ? "bg-[#FFBA9D] text-black shadow-md font-bold"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <TrendingUp size={12} /> TradingView
            </button>
          </div>

          {/* Timeframe Buttons */}
          <div className="flex gap-1 bg-[#0a0a1a] p-1 rounded-lg border border-[#1e1e4a]">
            {TIMEFRAMES.map((tf) => (
              <button
                key={tf.label}
                onClick={() => setActiveTimeframe(tf.label)}
                className={`px-3 py-1 text-xs font-semibold rounded-md transition-all duration-200 cursor-pointer ${
                  activeTimeframe === tf.label
                    ? "bg-white text-black shadow-md font-bold"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                {tf.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Widget/Chart Container */}
      <div 
        className="w-full rounded-xl overflow-hidden border border-[#1e1e4a]/60 bg-[#0a0a1a] p-4 flex items-center justify-center" 
        style={{ height: "400px" }}
      >
        {chartMode === "tradingview" ? (
          <div ref={containerRef} className="w-full h-full" />
        ) : (
          timeframeData ? (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorPriceTv" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#FFBA9D" stopOpacity={0.25}/>
                    <stop offset="95%" stopColor="#FFBA9D" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="rgba(255,255,255,0.05)" strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="idx" hide />
                <YAxis 
                  domain={["dataMin - (dataMax - dataMin) * 0.05", "dataMax + (dataMax - dataMin) * 0.05"]} 
                  stroke="#64748b" 
                  tickFormatter={(v) => `${currencySymbol}${v.toLocaleString()}`}
                  fontFamily="monospace"
                  fontSize={10}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#0a0a1a", borderColor: "rgba(255,255,255,0.1)", borderRadius: "8px" }}
                  labelStyle={{ color: "#FFBA9D" }}
                  itemStyle={{ color: "#fff" }}
                  formatter={(value) => [`${currencySymbol}${value.toLocaleString()}`, "Price"]}
                />
                {!isNaN(sPrice) && (
                  <ReferenceLine 
                    y={sPrice} 
                    label={{ value: `Support Floor: ${currencySymbol}${sPrice.toFixed(2)}`, fill: "#10b981", position: "bottom", fontSize: 9, fontFamily: "monospace" }} 
                    stroke="#10b981" 
                    strokeDasharray="3 3" 
                  />
                )}
                {!isNaN(rPrice) && (
                  <ReferenceLine 
                    y={rPrice} 
                    label={{ value: `Resistance Ceiling: ${currencySymbol}${rPrice.toFixed(2)}`, fill: "#ef4444", position: "top", fontSize: 9, fontFamily: "monospace" }} 
                    stroke="#ef4444" 
                    strokeDasharray="3 3" 
                  />
                )}
                <Area type="monotone" dataKey="Price" stroke="#FFBA9D" strokeWidth={2} fillOpacity={1} fill="url(#colorPriceTv)" />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex flex-col items-center justify-center text-center p-8 space-y-2">
              <span className="text-2xl">📊</span>
              <p className="text-slate-400 text-xs font-mono">No historical price arrays found for this symbol.</p>
              <p className="text-slate-650 text-[10px] max-w-md">The system failed to retrieve timeframe data from the API feed. Toggle to TradingView to try loading the external widget.</p>
            </div>
          )
        )}
      </div>
    </div>
  );
}

export default TradingViewChart;
