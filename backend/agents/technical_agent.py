# technical_agent.py
# The Technical Analysis Agent looks at price indicators (RSI, MACD, moving averages)
# to determine whether a stock is trending Bullish, Bearish, or Neutral.
#
# RSI (Relative Strength Index): Measures momentum.
#   > 70 = overbought (might fall), < 30 = oversold (might rise), 30-70 = neutral
#
# MACD (Moving Average Convergence Divergence): Measures trend direction.
#   Positive = bullish momentum, Negative = bearish momentum
#
# Moving Averages: Price above 50-day MA = short-term bullish signal.

def analyze(stock_data: dict) -> dict:
    """
    Analyzes technical indicators from stock data and returns a trend verdict.

    Args:
        stock_data: dict from stock_service.get_stock_data()

    Returns:
        dict with keys: trend, confidence, reason
    """

    # Extract the indicators we need
    rsi = stock_data.get("rsi", 50)
    macd = stock_data.get("macd", 0)
    price = stock_data.get("price", 100)
    ma_50 = stock_data.get("moving_avg_50", 100)

    # ── Score System ──────────────────────────────────────────────────────────
    # We award points based on each bullish signal.
    # At the end, the total score determines the trend.
    bullish_points = 0
    signals = []  # Collect human-readable reasons

    # Signal 1: RSI in healthy buy zone (40–65)
    if 40 <= rsi <= 65:
        bullish_points += 30
        signals.append("RSI in healthy zone")
    elif rsi < 30:
        bullish_points += 20
        signals.append("RSI oversold — possible bounce")
    elif rsi > 70:
        bullish_points -= 10
        signals.append("RSI overbought")

    # Signal 2: MACD is positive (bullish momentum)
    if macd > 0:
        bullish_points += 35
        signals.append("MACD positive momentum")
    else:
        bullish_points -= 15
        signals.append("MACD negative — bearish pressure")

    # Signal 3: Price is above the 50-day moving average
    if price > ma_50:
        bullish_points += 35
        signals.append("Price above 50-day MA")
    else:
        bullish_points -= 10
        signals.append("Price below 50-day MA")

    # ── Determine Trend ───────────────────────────────────────────────────────
    if bullish_points >= 60:
        trend = "Bullish"
        confidence = min(95, 60 + bullish_points // 3)
        reason = " and ".join(signals[:2]) if signals else "Multiple bullish indicators"
    elif bullish_points >= 20:
        trend = "Neutral"
        confidence = 55
        reason = "Mixed signals — no clear direction"
    else:
        trend = "Bearish"
        confidence = min(90, abs(bullish_points) + 40)
        reason = " and ".join(signals[:2]) if signals else "Multiple bearish indicators"

    return {
        "trend": trend,
        "confidence": confidence,
        "reason": reason,
    }
