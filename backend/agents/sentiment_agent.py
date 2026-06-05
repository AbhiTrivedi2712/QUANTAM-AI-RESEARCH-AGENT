# sentiment_agent.py
# The Sentiment Analysis Agent reads news headlines and decides whether
# market sentiment around the stock is Positive, Negative, or Neutral.
#
# In this MVP, we count how many positive vs negative news articles there are.
# In a real app, you'd use NLP (Natural Language Processing) or an AI model
# to actually read and classify the headlines.


def analyze(news_data: dict) -> dict:
    """
    Analyzes news article sentiments and returns an overall sentiment verdict.

    Args:
        news_data: dict from news_service.get_news()
                   Contains a list of articles, each with a 'sentiment' field.

    Returns:
        dict with keys: sentiment, confidence, reason
    """

    articles = news_data.get("articles", [])

    # If there are no articles, return a neutral default
    if not articles:
        return {
            "sentiment": "Neutral",
            "confidence": 50,
            "reason": "No recent news found",
        }

    # Count how many articles are positive, negative, and neutral
    positive_count = sum(1 for a in articles if a.get("sentiment") == "positive")
    negative_count = sum(1 for a in articles if a.get("sentiment") == "negative")
    neutral_count = sum(1 for a in articles if a.get("sentiment") == "neutral")
    total = len(articles)

    # Calculate what percentage of articles are positive
    positive_ratio = positive_count / total  # e.g. 0.6 = 60% positive

    # ── Determine Sentiment ───────────────────────────────────────────────────
    if positive_ratio >= 0.6:
        # More than 60% positive articles
        sentiment = "Positive"
        confidence = int(50 + positive_ratio * 45)  # Scale to 50–95 range
        reason = f"Majority positive news coverage ({positive_count}/{total} articles bullish)"

    elif negative_count > positive_count:
        # More negative than positive articles
        sentiment = "Negative"
        negative_ratio = negative_count / total
        confidence = int(50 + negative_ratio * 40)
        reason = f"Negative news dominates ({negative_count}/{total} articles bearish)"

    else:
        # Mixed or balanced news
        sentiment = "Neutral"
        confidence = 55
        reason = f"Mixed news — {positive_count} positive, {negative_count} negative articles"

    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "reason": reason,
    }
