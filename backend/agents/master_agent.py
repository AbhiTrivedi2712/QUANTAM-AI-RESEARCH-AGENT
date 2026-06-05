# master_agent.py
# The Master Agent is the "brain" that combines results from all three sub-agents
# (Technical, Fundamental, Sentiment) and produces a final investment recommendation.
#
# Decision Logic:
#   - Count how many agents are bullish vs bearish
#   - Average their confidence scores
#   - Use a simple majority vote to decide BUY / HOLD / SELL
#   - Assess risk based on how divided the agents are


def analyze(technical: dict, fundamental: dict, sentiment: dict) -> dict:
    """
    Combines outputs from all three agents into a final recommendation.

    Args:
        technical:   Output from technical_agent.analyze()
        fundamental: Output from fundamental_agent.analyze()
        sentiment:   Output from sentiment_agent.analyze()

    Returns:
        dict with keys: recommendation, confidence, risk, summary
    """

    # ── Step 1: Map each agent's verdict to a simple score ───────────────────
    # Bullish / Strong / Positive → 1 (positive signal)
    # Neutral / Average           → 0 (no signal)
    # Bearish / Weak / Negative   → -1 (negative signal)

    def score_signal(value: str) -> int:
        """Convert agent verdict string into a numeric score."""
        positive_words = {"bullish", "strong", "positive"}
        negative_words = {"bearish", "weak", "negative"}

        lower = value.lower()
        if lower in positive_words:
            return 1
        elif lower in negative_words:
            return -1
        return 0  # Neutral / Average

    tech_score = score_signal(technical.get("trend", "neutral"))
    fund_score = score_signal(fundamental.get("fundamental", "average"))
    sent_score = score_signal(sentiment.get("sentiment", "neutral"))

    # Total score ranges from -3 (all bearish) to +3 (all bullish)
    total_score = tech_score + fund_score + sent_score

    # ── Step 2: Calculate average confidence across all agents ────────────────
    tech_conf = technical.get("confidence", 50)
    fund_conf = fundamental.get("confidence", 50)
    sent_conf = sentiment.get("confidence", 50)
    avg_confidence = (tech_conf + fund_conf + sent_conf) // 3

    # ── Step 3: Make the final recommendation ─────────────────────────────────
    if total_score >= 2:
        # At least 2 out of 3 agents are bullish → BUY
        recommendation = "BUY"
        summary = "Technical, fundamental, and sentiment signals are aligned bullish."
    elif total_score <= -2:
        # At least 2 out of 3 agents are bearish → SELL
        recommendation = "SELL"
        summary = "Multiple signals indicate bearish pressure. Consider reducing exposure."
    else:
        # Mixed signals → HOLD
        recommendation = "HOLD"
        summary = "Mixed signals detected. Wait for clearer market direction."

    # ── Step 4: Assess Risk ───────────────────────────────────────────────────
    # Risk is higher when agents disagree with each other.
    agent_scores = [tech_score, fund_score, sent_score]
    disagreement = max(agent_scores) - min(agent_scores)  # 0, 1, or 2

    if disagreement == 0:
        risk = "Low"      # All agents agree
    elif disagreement == 1:
        risk = "Medium"   # Slight disagreement
    else:
        risk = "High"     # Agents completely disagree

    return {
        "recommendation": recommendation,
        "confidence": avg_confidence,
        "risk": risk,
        "summary": summary,
    }
