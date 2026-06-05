// Header.jsx — Top navigation bar
// Displays the QUANTUM AGENT logo and nav links.

import React from "react";

// Navigation page options
const NAV_ITEMS = ["Dashboard", "Architecture"];

function Header({ currentPage, setCurrentPage }) {
  return (
    <header className="border-b border-[#1e1e4a] bg-[#0a0a1a]/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* ── Logo ───────────────────────────────────────────────────────── */}
        <div className="flex items-center gap-3">
          {/* Animated logo icon */}
          <div className="relative">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-cyan-500 flex items-center justify-center">
              <span className="text-white font-bold text-lg">Q</span>
            </div>
            {/* Glow effect behind logo */}
            <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-purple-600 to-cyan-500 blur-md opacity-40 -z-10" />
          </div>

          <div>
            <h1 className="font-bold text-xl tracking-wider gradient-text" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              QUANTUM AGENT
            </h1>
            <p className="text-xs text-slate-500 -mt-0.5">Multi-Agent Financial Intelligence</p>
          </div>
        </div>

        {/* ── Navigation Links ────────────────────────────────────────────── */}
        <nav className="flex items-center gap-2">
          {NAV_ITEMS.map((page) => (
            <button
              key={page}
              onClick={() => setCurrentPage(page)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                currentPage === page
                  ? "bg-purple-600/20 text-purple-400 border border-purple-500/30"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
            >
              {page}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default Header;
