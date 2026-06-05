# news_service.py
# This service provides news headlines for a given stock symbol.
# It returns mock news data so the Sentiment Agent has something to analyze.
# In production, you'd call a real news API (NewsAPI.org, Finnhub, etc.)

import random

# ─── Mock News Headlines ──────────────────────────────────────────────────────
# Pre-written headlines categorized by sentiment.
# The Sentiment Agent will analyze these.

POSITIVE_HEADLINES = [
    "{sym} beats earnings expectations by wide margin",
    "{sym} announces major partnership deal with Google",
    "{sym} stock surges after record quarterly revenue",
    "Analysts upgrade {sym} to 'Strong Buy' rating",
    "{sym} expands into new international markets",
    "{sym} CEO announces aggressive growth strategy",
    "Institutional investors increase stake in {sym}",
]

NEGATIVE_HEADLINES = [
    "{sym} misses revenue targets for Q3",
    "Regulatory probe launched against {sym}",
    "{sym} faces supply chain disruptions",
    "Key executives leave {sym} amid restructuring",
    "{sym} lowers full-year guidance",
]

NEUTRAL_HEADLINES = [
    "{sym} holds annual investor day meeting",
    "{sym} announces upcoming product launch event",
    "Analysts maintain 'Hold' rating on {sym}",
    "{sym} files standard SEC quarterly report",
]


def get_news(symbol: str) -> dict:
    """
    Returns a list of recent news headlines for the given stock symbol.
    Each article has a title, sentiment label, and source.

    In a real app, you'd call: requests.get("https://newsapi.org/v2/...")
    """
    symbol = symbol.upper().strip()
    articles = []

    # Pick a mix of 3 positive, 1 negative, 1 neutral article
    chosen_positive = random.sample(POSITIVE_HEADLINES, 3)
    chosen_negative = random.sample(NEGATIVE_HEADLINES, 1)
    chosen_neutral = random.sample(NEUTRAL_HEADLINES, 1)

    # Format headlines by replacing {sym} with the actual stock symbol
    for headline in chosen_positive:
        articles.append({
            "title": headline.format(sym=symbol),
            "sentiment": "positive",
            "source": "MarketWatch",
        })

    for headline in chosen_negative:
        articles.append({
            "title": headline.format(sym=symbol),
            "sentiment": "negative",
            "source": "Reuters",
        })

    for headline in chosen_neutral:
        articles.append({
            "title": headline.format(sym=symbol),
            "sentiment": "neutral",
            "source": "Bloomberg",
        })

    # Shuffle so the order isn't always the same
    random.shuffle(articles)

    return {
        "symbol": symbol,
        "total_articles": len(articles),
        "articles": articles,
    }
