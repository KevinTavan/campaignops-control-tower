from typing import List, Dict, Any
import itertools
import re
import pandas as pd


STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "your", "our",
    "you", "are", "can", "will", "how", "why", "what", "to", "of", "in", "on",
    "a", "an", "by", "as", "is", "it", "be", "or", "at", "their", "teams",
}


def tokenize(text: str) -> set:
    if text is None or pd.isna(text):
        return set()
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9]+", str(text).lower())
    return {word for word in words if word not in STOPWORDS and len(word) > 2}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def detect_collisions(df: pd.DataFrame, threshold: float = 0.25) -> List[Dict[str, Any]]:
    collisions = []

    for (_, row_a), (_, row_b) in itertools.combinations(df.iterrows(), 2):
        audience_score = jaccard(
            tokenize(row_a.get("target_audience", "")),
            tokenize(row_b.get("target_audience", ""))
        )

        message_score = jaccard(
            tokenize(row_a.get("message", "")),
            tokenize(row_b.get("message", ""))
        )

        channel_score = jaccard(
            tokenize(row_a.get("channels", "")),
            tokenize(row_b.get("channels", ""))
        )

        asset_score = jaccard(
            tokenize(row_a.get("assets", "")),
            tokenize(row_b.get("assets", ""))
        )

        overall_score = round(
            (audience_score * 0.35) +
            (message_score * 0.35) +
            (channel_score * 0.15) +
            (asset_score * 0.15),
            2
        )

        if overall_score >= threshold:
            overlap_types = []
            if audience_score >= threshold:
                overlap_types.append("audience")
            if message_score >= threshold:
                overlap_types.append("message")
            if channel_score >= threshold:
                overlap_types.append("channel")
            if asset_score >= threshold:
                overlap_types.append("asset")

            collisions.append({
                "campaign_a": row_a.get("campaign_name", ""),
                "campaign_b": row_b.get("campaign_name", ""),
                "score": overall_score,
                "overlap_types": overlap_types or ["mixed"],
                "audience_score": round(audience_score, 2),
                "message_score": round(message_score, 2),
                "channel_score": round(channel_score, 2),
                "asset_score": round(asset_score, 2),
                "recommendation": build_recommendation(overlap_types),
            })

    return sorted(collisions, key=lambda item: item["score"], reverse=True)


def build_recommendation(overlap_types: List[str]) -> str:
    if "message" in overlap_types and "audience" in overlap_types:
        return "Review whether these campaigns should be differentiated, sequenced, or combined to avoid audience fatigue."
    if "message" in overlap_types:
        return "Clarify message hierarchy and proof points so the campaigns do not sound interchangeable."
    if "audience" in overlap_types:
        return "Confirm audience segmentation and decide whether each campaign owns a distinct audience need."
    if "channel" in overlap_types:
        return "Check timing and channel ownership to reduce internal competition."
    if "asset" in overlap_types:
        return "Look for reusable assets or duplicated production work."
    return "Review for possible coordination risk before launch."


def format_collision_report(collisions: List[Dict[str, Any]]) -> str:
    if not collisions:
        return "## Collision Report\n\nNo major overlaps detected at the selected sensitivity."

    sections = ["## Collision Report"]

    for item in collisions:
        overlap = ", ".join(item["overlap_types"])
        sections.append(
            f"""### {item["campaign_a"]} ↔ {item["campaign_b"]}

**Overall overlap score:** {item["score"]}  
**Overlap type:** {overlap}

- Audience overlap: {item["audience_score"]}
- Message overlap: {item["message_score"]}
- Channel overlap: {item["channel_score"]}
- Asset overlap: {item["asset_score"]}

**Recommendation:** {item["recommendation"]}
"""
        )

    return "\n".join(sections)
