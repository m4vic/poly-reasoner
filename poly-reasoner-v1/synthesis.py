# synthesis.py

KEYWORDS = {
    "positive": ["feasible", "viable", "good", "strong", "low risk", "worth"],
    "negative": ["risk", "hard", "difficult", "uncertain", "expensive", "problem"],
}


def classify_sentiment(text: str) -> str:
    t = text.lower()
    pos = any(k in t for k in KEYWORDS["positive"])
    neg = any(k in t for k in KEYWORDS["negative"])

    if pos and not neg:
        return "positive"
    if neg and not pos:
        return "negative"
    return "neutral"


def calculate_confidence(positives, negatives, total):
    if positives and not negatives:
        return round(len(positives) / total, 2)
    if negatives and not positives:
        return round(len(negatives) / total, 2)
    if positives and negatives:
        return 0.3
    return 0.5


def synthesize(agent_outputs: list[dict], weights: dict | None = None) -> dict:
    summary = []
    sentiments = {}

    for item in agent_outputs:
        agent = item["agent"]
        text = item["output"]

        sentiment = classify_sentiment(text)
        sentiments[agent] = sentiment

        summary.append({
            "agent": agent,
            "sentiment": sentiment,
            "output": text
        })

    positives = [a for a, s in sentiments.items() if s == "positive"]
    negatives = [a for a, s in sentiments.items() if s == "negative"]

    confidence = calculate_confidence(
        positives, negatives, len(sentiments)
    )

    weighted_score = None
    if weights:
        score = 0.0
        for agent, sentiment in sentiments.items():
            w = weights.get(agent, 0)
            if sentiment == "positive":
                score += w
            elif sentiment == "negative":
                score -= w
        weighted_score = round(score, 2)

    return {
        "summary": summary,
        "positives": positives,
        "negatives": negatives,
        "disagreement": bool(positives and negatives),
        "confidence": confidence,
        "weighted_score": weighted_score,
        "note": "Advisory output. Higher disagreement lowers confidence."
    }
