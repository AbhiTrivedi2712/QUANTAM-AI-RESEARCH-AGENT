# stock_service.py
# This service fetches real stock market data using the yfinance library.
# It supports US stocks and Indian stocks (.NS suffix).
# It falls back to realistic mock data if the API fails or the symbol is invalid.

import yfinance as yf
import pandas as pd
import numpy as np
import random
import logging

logger = logging.getLogger("quantum_agent.stock_service")

# Common Indian stocks that we auto-resolve to .NS
INDIAN_TICKERS = {
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "BHARTIARTL", 
    "ITC", "LICI", "HINDUNILVR", "LT", "ITC", "BAJFINANCE", "WIPRO"
}

def resolve_symbol(symbol: str) -> str:
    """
    Cleans up ticker symbols and appends .NS for popular Indian stocks 
    if no suffix is provided.
    """
    symbol = symbol.upper().strip()
    if "." not in symbol and symbol in INDIAN_TICKERS:
        resolved = f"{symbol}.NS"
        logger.info(f"Auto-resolving Indian ticker: {symbol} -> {resolved}")
        return resolved
    return symbol

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculates the Relative Strength Index (RSI)."""
    if len(series) < period:
        return pd.Series(50, index=series.index)
    
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    
    # Calculate EMA of gains and losses
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    
    rs = avg_gain / (avg_loss + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    """Calculates MACD Line, Signal Line, and Histogram."""
    if len(series) < slow:
        zero_series = pd.Series(0.0, index=series.index)
        return zero_series, zero_series, zero_series
        
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    macd_hist = macd_line - signal_line
    return macd_line, signal_line, macd_hist

def get_stock_data(symbol: str) -> dict:
    """
    Fetches real stock statistics and historical daily prices from yfinance.
    Calculates technical indicators dynamically (RSI, MACD, MA, Volatility, S/R).
    Falls back to mock data if API fails.
    """
    resolved_symbol = resolve_symbol(symbol)
    
    try:
        ticker = yf.Ticker(resolved_symbol)
        
        # 1. Fetch historical data for technical indicators (1 year of daily history)
        hist = ticker.history(period="1y", interval="1d")
        if hist.empty:
            raise ValueError(f"No historical data returned for {resolved_symbol}")

        # Drop rows with NaN close prices (yfinance may return NaN for most recent incomplete candle)
        hist = hist.dropna(subset=['Close'])
        if hist.empty:
            raise ValueError(f"No valid historical close prices for {resolved_symbol}")
            
        close_prices = hist['Close']
        hist_last_price = float(close_prices.iloc[-1])

        # 2a. Fetch Fundamental Data first so we can pull live price from info
        info = ticker.info

        # Determine the market state (REGULAR, PRE, POST, CLOSED, etc.)
        market_state = (info.get("marketState") or "").upper()

        # Resolve the best available current price and matching change data
        # based on the current market session.
        reg_price   = info.get("regularMarketPrice") or info.get("currentPrice")
        pre_price   = info.get("preMarketPrice")
        post_price  = info.get("postMarketPrice")

        if market_state == "PRE" and pre_price:
            # Pre-market session: show the pre-market price
            last_price = float(pre_price)
            change     = float(info.get("preMarketChange") or 0.0)
            # Derive pct from the actual price delta — avoids ambiguity in
            # yfinance returning the field as a fraction vs. a percentage.
            prev_price = last_price - change
            change_pct = (change / prev_price * 100) if prev_price else 0.0
        elif market_state in ("POST", "POSTPOST") and post_price:
            # After-hours session: show the post-market price
            last_price = float(post_price)
            change     = float(info.get("postMarketChange") or 0.0)
            prev_price = last_price - change
            change_pct = (change / prev_price * 100) if prev_price else 0.0
        else:
            # Regular market hours (or fallback for CLOSED/unknown states)
            last_price = float(reg_price) if reg_price else hist_last_price
            # Prefer pre-computed change values from info when available
            if info.get("regularMarketChange") is not None and info.get("regularMarketChangePercent") is not None:
                change     = float(info["regularMarketChange"])
                change_pct = float(info["regularMarketChangePercent"])
            else:
                prev_close_info = info.get("previousClose") or info.get("regularMarketPreviousClose")
                prev_close = float(prev_close_info) if prev_close_info else (
                    float(close_prices.iloc[-2]) if len(close_prices) > 1 else last_price
                )
                change     = last_price - prev_close
                change_pct = (change / prev_close) * 100 if prev_close else 0.0
        
        # Calculate Technical Indicators
        # Moving Averages
        ma_50 = float(close_prices.rolling(window=50).mean().iloc[-1]) if len(close_prices) >= 50 else last_price
        ma_200 = float(close_prices.rolling(window=200).mean().iloc[-1]) if len(close_prices) >= 200 else last_price
        
        # RSI
        rsi_series = calculate_rsi(close_prices)
        rsi_val = float(rsi_series.iloc[-1])
        
        # MACD
        macd_line, signal_line, macd_hist = calculate_macd(close_prices)
        macd_val = float(macd_line.iloc[-1])
        macd_signal = float(signal_line.iloc[-1])
        macd_hist_val = float(macd_hist.iloc[-1])
        
        # Volatility: standard deviation of daily percent changes over past 20 days (annualized)
        daily_returns = close_prices.pct_change().dropna()
        if len(daily_returns) >= 20:
            vol_score = float(daily_returns.tail(20).std() * np.sqrt(252) * 100)
        else:
            vol_score = 15.0 # default volatility
            
        # Support and Resistance: local extrema of the past 20 trading days
        recent_data = close_prices.tail(20)
        support = float(recent_data.min())
        resistance = float(recent_data.max())

        
        # 2. Use already-fetched ticker info for fundamental data
        name = info.get("longName") or info.get("shortName") or f"{symbol} Corp."
        market_cap_raw = info.get("marketCap")
        if market_cap_raw:
            if market_cap_raw >= 1e12:
                market_cap = f"${market_cap_raw / 1e12:.2f}T"
            elif market_cap_raw >= 1e9:
                market_cap = f"${market_cap_raw / 1e9:.2f}B"
            else:
                market_cap = f"${market_cap_raw / 1e6:.2f}M"
        else:
            market_cap = "N/A"
            
        pe_ratio_raw = info.get("trailingPE") or info.get("forwardPE") or 0.0
        pe_ratio = 0.0 if (pe_ratio_raw != pe_ratio_raw) else float(pe_ratio_raw)  # NaN check
        
        # Growth rates (convert standard decimals from yfinance info to percentages)
        rev_growth_raw = info.get("revenueGrowth")
        rev_growth = float(rev_growth_raw * 100) if (rev_growth_raw is not None and rev_growth_raw == rev_growth_raw) else 0.0
        
        earn_growth_raw = info.get("earningsGrowth")
        earn_growth = float(earn_growth_raw * 100) if (earn_growth_raw is not None and earn_growth_raw == earn_growth_raw) else 0.0
        
        total_revenue = info.get("totalRevenue") or 0.0
        net_income = info.get("netIncomeToCommon") or info.get("netIncome") or 0.0
        volume = info.get("regularMarketVolume") or info.get("volume") or int(hist['Volume'].iloc[-1])

        def safe_float(val, default=0.0):
            """Returns default if val is NaN or None."""
            try:
                f = float(val)
                return default if f != f else f  # NaN != NaN
            except (TypeError, ValueError):
                return default
        
        return {
            "symbol": resolved_symbol,
            "name": name,
            "price": round(safe_float(last_price), 2),
            "change": round(safe_float(change), 2),
            "change_pct": round(safe_float(change_pct), 2),
            "market_state": market_state,  # "PRE", "POST", "REGULAR", "CLOSED", etc.
            "volume": volume,
            "market_cap": market_cap,
            "pe_ratio": round(pe_ratio, 1) if pe_ratio else None,
            "revenue_growth": round(rev_growth, 1),
            "earnings_growth": round(earn_growth, 1),
            "total_revenue": safe_float(total_revenue),
            "net_income": safe_float(net_income),
            "rsi": round(safe_float(rsi_val, 50.0), 1),
            "macd": round(safe_float(macd_val), 2),
            "macd_signal": round(safe_float(macd_signal), 2),
            "macd_hist": round(safe_float(macd_hist_val), 2),
            "moving_avg_50": round(safe_float(ma_50, last_price), 2),
            "moving_avg_200": round(safe_float(ma_200, last_price), 2),
            "support": round(safe_float(support, last_price), 2),
            "resistance": round(safe_float(resistance, last_price), 2),
            "volatility": round(safe_float(vol_score, 15.0), 1),
            "source": "Yahoo Finance (Real-Time)"
        }
        
    except Exception as e:
        logger.error(f"Error fetching real data for {resolved_symbol}: {str(e)}. Falling back to mock data.")
        return get_mock_stock_data(resolved_symbol)

def get_mock_stock_data(symbol: str) -> dict:
    """Generates realistic mock data as a robust fallback."""
    price = round(random.uniform(10, 500), 2)
    change = round(random.uniform(-10, 10), 2)
    change_pct = round((change / price) * 100, 2)
    rsi = random.randint(25, 75)
    
    return {
        "symbol": symbol,
        "name": f"{symbol} Corp. (Mock)",
        "price": price,
        "change": change,
        "change_pct": change_pct,
        "volume": random.randint(1_000_000, 50_000_000),
        "market_cap": f"${random.uniform(1, 200):.1f}B",
        "pe_ratio": round(random.uniform(12, 45), 1),
        "revenue_growth": round(random.uniform(-5, 25), 1),
        "earnings_growth": round(random.uniform(-10, 30), 1),
        "total_revenue": random.randint(100_000_000, 5_000_000_000),
        "net_income": random.randint(-50_000_000, 500_000_000),
        "rsi": rsi,
        "macd": round(random.uniform(-2, 2), 2),
        "macd_signal": round(random.uniform(-1.5, 1.5), 2),
        "macd_hist": round(random.uniform(-0.5, 0.5), 2),
        "moving_avg_50": round(price * 0.98, 2),
        "moving_avg_200": round(price * 0.94, 2),
        "support": round(price * 0.92, 2),
        "resistance": round(price * 1.05, 2),
        "volatility": round(random.uniform(10, 40), 1),
        "source": "Mock Data Engine (Fallback)"
    }

def get_multiple_timeframes(symbol: str) -> dict:
    """
    Fetches real price data for multiple timeframes.
    Supports 15m (5 days), 1h (1 month), 4h (resampled from 1h), 1d (6 months), 1w (1 year).
    Falls back to generated arrays if real calls fail.
    """
    resolved_symbol = resolve_symbol(symbol)
    timeframes = {}
    
    try:
        ticker = yf.Ticker(resolved_symbol)
        
        # 15m (5 days)
        hist_15m = ticker.history(period="5d", interval="15m")
        if not hist_15m.empty:
            hist_15m = hist_15m.dropna(subset=['Close'])
            timeframes["15m"] = hist_15m['Close'].round(2).tolist()
            
        # 1h (1 month)
        hist_1h = ticker.history(period="1mo", interval="1h")
        if not hist_1h.empty:
            hist_1h = hist_1h.dropna(subset=['Close'])
            timeframes["1h"] = hist_1h['Close'].round(2).tolist()
            
            # Resample 1h to 4h (generate Open, High, Low, Close, Volume)
            resampled_4h_df = hist_1h.resample('4h').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()

            timeframes["4h"] = resampled_4h_df['Close'].round(2).tolist()
            timeframes["4h_ohlcv"] = {
                "open": resampled_4h_df['Open'].round(2).tolist(),
                "high": resampled_4h_df['High'].round(2).tolist(),
                "low": resampled_4h_df['Low'].round(2).tolist(),
                "close": resampled_4h_df['Close'].round(2).tolist(),
                "volume": resampled_4h_df['Volume'].round(2).tolist()
            }

            
        # 1d (6 months)
        hist_1d = ticker.history(period="6mo", interval="1d")
        if not hist_1d.empty:
            hist_1d = hist_1d.dropna(subset=['Close'])
            timeframes["1d"] = hist_1d['Close'].round(2).tolist()
            
        # 1w (1 year)
        hist_1w = ticker.history(period="1y", interval="1wk")
        if not hist_1w.empty:
            hist_1w = hist_1w.dropna(subset=['Close'])
            timeframes["1w"] = hist_1w['Close'].round(2).tolist()
            
        # Standardize fallback keys if any timeframe is missing
        base_price = get_stock_data(resolved_symbol)["price"]
        for tf, period_days in [("15m", 5), ("1h", 20), ("4h", 40), ("1d", 60), ("1w", 52)]:
            if tf not in timeframes or len(timeframes[tf]) == 0:
                timeframes[tf] = simulate_history(base_price, period_days)
                
        return timeframes
        
    except Exception as e:
        logger.error(f"Error fetching historical timeframes for {resolved_symbol}: {str(e)}")
        # Complete fallback
        base_price = 100.0
        try:
            base_price = get_stock_data(resolved_symbol)["price"]
        except Exception:
            pass
        return {
            "15m": simulate_history(base_price, 30),
            "1h": simulate_history(base_price, 50),
            "4h": simulate_history(base_price, 80),
            "1d": simulate_history(base_price, 120),
            "1w": simulate_history(base_price, 52),
        }

def simulate_history(base_price: float, count: int) -> list:
    """Generates a random walk history starting around the base price."""
    prices = []
    current = base_price * 0.95
    for _ in range(count - 1):
        current = round(current * random.uniform(0.98, 1.02), 2)
        prices.append(current)
    prices.append(base_price)
    return prices


def is_ticker_valid(symbol: str) -> bool:
    """
    Checks if a ticker symbol actually exists on Yahoo Finance.
    If it's a completely fake ticker, history will be empty or yfinance raises ValueErrors.
    If it's a network error, we return True to allow mock fallbacks for valid tickers,
    but if it's a clear 'Quote not found' or delisted state, we return False.
    """
    try:
        resolved = resolve_symbol(symbol)
        
        # Test basic initialization (triggers ValueErrors on bad formatting e.g. ISIN check)
        ticker = yf.Ticker(resolved)
        
        # Fetch 1-day history to check existence
        hist = ticker.history(period="1d")
        if hist.empty:
            # Check if there is any basic symbol data or if it's completely missing
            info = ticker.info
            # If info is empty or missing key metrics, it's invalid
            if not info or not any(k in info for k in ["regularMarketPrice", "longName", "symbol"]):
                logger.warning(f"Ticker validation: Ticker {resolved} returned empty history and info.")
                return False
        return True
    except ValueError as ve:
        # e.g., ValueError: Invalid ISIN number: FAKESTOCK123
        logger.warning(f"Ticker validation: Ticker {symbol} triggered ValueError: {str(ve)}")
        return False
    except Exception as e:
        err_msg = str(e).lower()
        if "not found" in err_msg or "invalid" in err_msg or "404" in err_msg:
            logger.warning(f"Ticker validation: Ticker {symbol} failed with error: {str(e)}")
            return False
        # For connection timeouts/DNS failures, return True to allow mock engine fallbacks
        logger.info(f"Ticker validation: Connection error or standard warning during check: {str(e)}. Assuming True.")
        return True

