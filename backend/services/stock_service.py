# stock_service.py
# This service fetches stock market data.
# Right now it returns realistic MOCK data so the app works without any API key.
# Later you can replace the mock functions with real API calls (Yahoo Finance, Alpha Vantage, etc.)

import random

# ─── Mock Data Library ────────────────────────────────────────────────────────
# We predefine realistic data for a few popular stocks.
# If the user searches for any other symbol, we generate random data.

MOCK_STOCK_DATA = {
    "AAPL": {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "price": 189.45,
        "change": 2.34,
        "change_pct": 1.25,
        "volume": 55_234_000,
        "market_cap": "2.95T",
        "pe_ratio": 29.5,
        "revenue_growth": 8.1,
        "earnings_growth": 10.2,
        "rsi": 58,           # RSI: 0–100, >70 overbought, <30 oversold
        "macd": 1.2,         # MACD: positive = bullish signal
        "moving_avg_50": 182.3,
        "moving_avg_200": 175.0,
    },
    "TSLA": {
        "symbol": "TSLA",
        "name": "Tesla Inc.",
        "price": 245.67,
        "change": -5.23,
        "change_pct": -2.08,
        "volume": 98_450_000,
        "market_cap": "780B",
        "pe_ratio": 65.2,
        "revenue_growth": 19.5,
        "earnings_growth": 25.3,
        "rsi": 42,
        "macd": -0.8,
        "moving_avg_50": 252.1,
        "moving_avg_200": 231.5,
    },
    "INFY": {
        "symbol": "INFY",
        "name": "Infosys Ltd.",
        "price": 18.92,
        "change": 0.45,
        "change_pct": 2.44,
        "volume": 12_340_000,
        "market_cap": "78B",
        "pe_ratio": 22.1,
        "revenue_growth": 12.3,
        "earnings_growth": 8.7,
        "rsi": 62,
        "macd": 0.5,
        "moving_avg_50": 18.1,
        "moving_avg_200": 16.8,
    },
    "TCS": {
        "symbol": "TCS",
        "name": "Tata Consultancy Services",
        "price": 42.30,
        "change": 0.78,
        "change_pct": 1.88,
        "volume": 8_900_000,
        "market_cap": "153B",
        "pe_ratio": 28.4,
        "revenue_growth": 10.1,
        "earnings_growth": 11.5,
        "rsi": 55,
        "macd": 0.9,
        "moving_avg_50": 41.5,
        "moving_avg_200": 38.2,
    },
}


def get_stock_data(symbol: str) -> dict:
    """
    Returns stock data for a given ticker symbol.
    If we have mock data for that symbol, we return it.
    Otherwise, we generate random but realistic-looking data.
    """
    symbol = symbol.upper().strip()

    # Check if we have pre-defined mock data
    if symbol in MOCK_STOCK_DATA:
        return MOCK_STOCK_DATA[symbol]

    # Generate random data for unknown symbols
    price = round(random.uniform(10, 500), 2)
    change = round(random.uniform(-10, 10), 2)

    return {
        "symbol": symbol,
        "name": f"{symbol} Corp.",
        "price": price,
        "change": change,
        "change_pct": round(change / price * 100, 2),
        "volume": random.randint(1_000_000, 100_000_000),
        "market_cap": f"{round(random.uniform(1, 500), 1)}B",
        "pe_ratio": round(random.uniform(10, 80), 1),
        "revenue_growth": round(random.uniform(-5, 30), 1),
        "earnings_growth": round(random.uniform(-5, 35), 1),
        "rsi": random.randint(25, 75),
        "macd": round(random.uniform(-2, 2), 2),
        "moving_avg_50": round(price * random.uniform(0.9, 1.1), 2),
        "moving_avg_200": round(price * random.uniform(0.8, 1.1), 2),
    }


def get_multiple_timeframes(symbol: str) -> dict:
    """
    Returns price data across multiple timeframes.
    Used to show historical price trend charts on the frontend.
    """
    base = get_stock_data(symbol)["price"]

    # Simulate past 7 days of closing prices by adding small random changes
    daily_prices = []
    price = base * 0.92  # start a bit lower than current
    for _ in range(7):
        price = round(price * random.uniform(0.98, 1.03), 2)
        daily_prices.append(price)
    daily_prices.append(base)  # today's price at the end

    return {
        "symbol": symbol,
        "weekly": daily_prices,       # Last 7 days
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Today"],
    }
