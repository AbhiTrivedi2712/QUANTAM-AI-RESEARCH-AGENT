# fundamental_agent.py
# The Fundamental Analysis Agent evaluates a company's financial health
# by looking at metrics like PE ratio, revenue growth, and earnings growth.
#
# PE Ratio (Price-to-Earnings): How much investors pay per $1 of earnings.
#   Low PE (<20) might mean undervalued. Very high PE (>60) might mean overvalued.
#
# Revenue Growth: Is the company growing its sales? Higher is better.
#
# Earnings Growth: Is profit increasing? Key for long-term value.


def analyze(stock_data: dict) -> dict:
    """
    Evaluates company fundamentals and returns a verdict.

    Args:
        stock_data: dict from stock_service.get_stock_data()

    Returns:
        dict with keys: fundamental, confidence, reason
    """

    # Extract fundamental metrics
    pe_ratio = stock_data.get("pe_ratio", 25)
    revenue_growth = stock_data.get("revenue_growth", 5)
    earnings_growth = stock_data.get("earnings_growth", 5)

    # ── Score System ──────────────────────────────────────────────────────────
    score = 0
    reasons = []

    # Signal 1: PE Ratio — reasonable valuation
    if pe_ratio < 15:
        score += 40
        reasons.append("very attractive valuation")
    elif pe_ratio <= 30:
        score += 30
        reasons.append("reasonable PE ratio")
    elif pe_ratio <= 50:
        score += 10
        reasons.append("moderately high valuation")
    else:
        score -= 10
        reasons.append("expensive valuation")

    # Signal 2: Revenue Growth — is the business growing?
    if revenue_growth > 15:
        score += 35
        reasons.append("strong revenue growth")
    elif revenue_growth > 5:
        score += 20
        reasons.append("steady revenue growth")
    else:
        score += 5
        reasons.append("slow revenue growth")

    # Signal 3: Earnings Growth — is profit improving?
    if earnings_growth > 15:
        score += 35
        reasons.append("excellent earnings growth")
    elif earnings_growth > 5:
        score += 20
        reasons.append("healthy earnings growth")
    else:
        score += 5
        reasons.append("weak earnings growth")

    # ── Determine Fundamental Rating ──────────────────────────────────────────
    if score >= 75:
        fundamental = "Strong"
        confidence = min(95, score)
        reason = "Revenue growth and " + reasons[-1] if reasons else "Strong fundamentals"
    elif score >= 45:
        fundamental = "Average"
        confidence = 60
        reason = "Mixed fundamentals — " + (reasons[0] if reasons else "no clear edge")
    else:
        fundamental = "Weak"
        confidence = min(85, 100 - score)
        reason = "Poor valuation and " + (reasons[-1] if reasons else "weak metrics")

    return {
        "fundamental": fundamental,
        "confidence": confidence,
        "reason": reason,
    }
