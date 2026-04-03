from pydantic import BaseModel


class ScoreResponse(BaseModel):
    total_score: int
    rank: str
    address: str
    breakdown: dict
    recommendations: list[str]


def classify_rank(score: int) -> str:
    if score >= 750:
        return "Excellent"
    elif score >= 600:
        return "Good"
    elif score >= 400:
        return "Fair"
    elif score >= 200:
        return "Developing"
    else:
        return "New"


def generate_recommendations(breakdown: dict) -> list[str]:
    recs = []

    if breakdown.get("consistency", 0) < 100:
        recs.append("Increase transaction frequency to improve consistency")
    if breakdown.get("diversification", 0) < 50:
        recs.append("Explore Lightning Network to improve layer diversification")
    if breakdown.get("savings_pattern", 0) < 100:
        recs.append("Maintain a consistent savings pattern to increase your score")
    if breakdown.get("lightning_activity", 0) < 50:
        recs.append("Activate your Lightning wallet to improve activity score")

    if not recs:
        recs.append("Excellent work! Keep maintaining your Bitcoin activity.")

    return recs
