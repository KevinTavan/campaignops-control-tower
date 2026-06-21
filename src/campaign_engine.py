from typing import Dict, List, Any
import pandas as pd


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except TypeError:
        pass
    return str(value).strip()


def split_items(value: Any) -> List[str]:
    text = clean_text(value)
    if not text:
        return []
    parts = []
    for chunk in text.replace("|", ",").replace(";", ",").split(","):
        item = chunk.strip().lower()
        if item:
            parts.append(item)
    return parts


def contains_any(text: str, candidates: List[str]) -> bool:
    text_l = text.lower()
    return any(candidate in text_l for candidate in candidates)


def score_presence(value: str, max_points: int, min_length: int = 8) -> int:
    value = clean_text(value)
    if not value:
        return 0
    if len(value) < min_length:
        return max_points // 2
    return max_points


def score_campaign(row: Dict[str, Any]) -> Dict[str, int]:
    objective = clean_text(row.get("objective"))
    audience = clean_text(row.get("target_audience"))
    message = clean_text(row.get("message"))
    channels = split_items(row.get("channels"))
    assets = split_items(row.get("assets"))
    stakeholders = split_items(row.get("stakeholders"))
    launch_date = clean_text(row.get("launch_date"))
    measurement_plan = clean_text(row.get("measurement_plan"))
    notes = clean_text(row.get("notes"))

    scores = {
        "Objective clarity": score_presence(objective, 15),
        "Audience clarity": score_presence(audience, 15),
        "Message clarity": score_presence(message, 20, min_length=20),
        "Channel coverage": min(10, len(channels) * 2),
        "Asset readiness": min(15, len(assets) * 3),
        "Stakeholder clarity": min(10, len(stakeholders) * 2),
        "Measurement clarity": score_presence(measurement_plan, 10, min_length=12),
        "Timeline clarity": 5 if launch_date else 0,
    }

    if "TBD" in objective.upper() or "TBD" in message.upper() or "TBD" in notes.upper():
        scores["Objective clarity"] = max(0, scores["Objective clarity"] - 5)
        scores["Message clarity"] = max(0, scores["Message clarity"] - 5)

    return scores


def find_gaps(row: Dict[str, Any], scores: Dict[str, int]) -> List[str]:
    gaps = []

    if scores["Objective clarity"] < 15:
        gaps.append("Campaign objective needs sharper business outcome or launch goal.")
    if scores["Audience clarity"] < 15:
        gaps.append("Target audience is vague or missing.")
    if scores["Message clarity"] < 20:
        gaps.append("Core message needs more detail, proof, or differentiation.")
    if scores["Channel coverage"] < 6:
        gaps.append("Channel mix may be too narrow for an integrated campaign.")
    if scores["Asset readiness"] < 9:
        gaps.append("Asset checklist appears incomplete.")
    if scores["Stakeholder clarity"] < 6:
        gaps.append("Stakeholder ownership may be unclear.")
    if scores["Measurement clarity"] < 10:
        gaps.append("Measurement plan is missing or underdeveloped.")
    if scores["Timeline clarity"] < 5:
        gaps.append("Launch date or timeline is missing.")

    assets = split_items(row.get("assets"))
    channels = split_items(row.get("channels"))

    if "sales" in channels and not contains_any(",".join(assets), ["sales enablement", "one-pager", "deck"]):
        gaps.append("Sales channel is listed, but sales enablement asset is not clearly included.")

    if "paid media" in channels and not contains_any(",".join(assets), ["landing page", "paid media"]):
        gaps.append("Paid media is listed, but landing page or paid asset is unclear.")

    return gaps or ["No major gaps detected. Human review still recommended."]


def find_strengths(row: Dict[str, Any], scores: Dict[str, int]) -> List[str]:
    strengths = []

    if scores["Objective clarity"] >= 15:
        strengths.append("Campaign objective is clearly stated.")
    if scores["Audience clarity"] >= 15:
        strengths.append("Target audience is defined.")
    if scores["Message clarity"] >= 20:
        strengths.append("Core message is specific enough for review.")
    if scores["Channel coverage"] >= 6:
        strengths.append("Campaign has a multi-channel distribution plan.")
    if scores["Asset readiness"] >= 9:
        strengths.append("Asset plan includes several launch materials.")
    if scores["Stakeholder clarity"] >= 6:
        strengths.append("Stakeholder ownership is reasonably clear.")
    if scores["Measurement clarity"] >= 10:
        strengths.append("Measurement plan is included.")

    return strengths or ["No clear strengths detected yet. The brief needs more campaign detail."]


def build_next_steps(row: Dict[str, Any], gaps: List[str]) -> List[str]:
    steps = []

    for gap in gaps:
        gap_l = gap.lower()
        if "objective" in gap_l:
            steps.append("Rewrite the objective as a measurable business or audience outcome.")
        elif "audience" in gap_l:
            steps.append("Clarify primary and secondary audiences before finalizing message or channel mix.")
        elif "message" in gap_l:
            steps.append("Add proof points, customer pain, differentiation, and one primary CTA.")
        elif "channel" in gap_l:
            steps.append("Confirm the channel plan with owners for email, web, social, paid, sales, and events.")
        elif "asset" in gap_l:
            steps.append("Create a launch asset checklist with owner, status, and due date.")
        elif "stakeholder" in gap_l:
            steps.append("Assign clear owners for PMM, integrated marketing, creative, web, sales, and analytics.")
        elif "measurement" in gap_l:
            steps.append("Define success metrics such as pipeline, MQLs, CTR, registrations, conversion rate, or influenced revenue.")
        elif "timeline" in gap_l or "launch date" in gap_l:
            steps.append("Confirm launch date, review deadlines, and dependency milestones.")

    if not steps:
        steps.append("Schedule final cross-functional review and confirm launch approval path.")

    steps.append("Create a manager-ready status update with risks, blockers, owners, and next decisions.")
    return list(dict.fromkeys(steps))


def analyze_campaign(row: Dict[str, Any]) -> Dict[str, Any]:
    scores = score_campaign(row)
    readiness_score = sum(scores.values())
    gaps = find_gaps(row, scores)
    strengths = find_strengths(row, scores)
    next_steps = build_next_steps(row, gaps)

    return {
        "campaign_id": clean_text(row.get("campaign_id")),
        "campaign_name": clean_text(row.get("campaign_name")),
        "objective": clean_text(row.get("objective")),
        "target_audience": clean_text(row.get("target_audience")),
        "message": clean_text(row.get("message")),
        "channels": split_items(row.get("channels")),
        "assets": split_items(row.get("assets")),
        "stakeholders": split_items(row.get("stakeholders")),
        "launch_date": clean_text(row.get("launch_date")),
        "status": clean_text(row.get("status")),
        "measurement_plan": clean_text(row.get("measurement_plan")),
        "notes": clean_text(row.get("notes")),
        "scores": scores,
        "readiness_score": readiness_score,
        "strengths": strengths,
        "gaps": gaps,
        "next_steps": next_steps,
    }


def readiness_dataframe(analysis: Dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [{"Category": key, "Points": value} for key, value in analysis["scores"].items()]
    )


def bullets(items: List[str]) -> str:
    return "\n".join([f"- {item}" for item in items])


def build_manager_update(analysis: Dict[str, Any]) -> str:
    risk_level = "low"
    if analysis["readiness_score"] < 60:
        risk_level = "high"
    elif analysis["readiness_score"] < 80:
        risk_level = "moderate"

    main_gap = analysis["gaps"][0] if analysis["gaps"] else "No major gap detected."

    return (
        f"{analysis['campaign_name']} is currently at {analysis['readiness_score']}/100 launch readiness "
        f"with {risk_level} coordination risk. Primary gap: {main_gap} "
        f"Recommended next step: {analysis['next_steps'][0]}"
    )


def format_campaign_brief(analysis: Dict[str, Any]) -> str:
    return f"""## Campaign Operations Brief

### Campaign
**{analysis["campaign_name"]}**  
Campaign ID: `{analysis["campaign_id"]}`  
Status: **{analysis["status"]}**  
Launch date: **{analysis["launch_date"] or "Not specified"}**

### Objective
{analysis["objective"] or "Not specified"}

### Target Audience
{analysis["target_audience"] or "Not specified"}

### Core Message
{analysis["message"] or "Not specified"}

### Channels
{bullets(analysis["channels"] or ["Not specified"])}

### Assets
{bullets(analysis["assets"] or ["Not specified"])}

### Stakeholders
{bullets(analysis["stakeholders"] or ["Not specified"])}

### Measurement Plan
{analysis["measurement_plan"] or "Not specified"}

### Launch Readiness
**{analysis["readiness_score"]}/100**

### Strengths
{bullets(analysis["strengths"])}

### Gaps
{bullets(analysis["gaps"])}

### Suggested Next Steps
{bullets(analysis["next_steps"])}

### Manager-Ready Update
{build_manager_update(analysis)}
"""


def build_handoff_summary(analysis: Dict[str, Any]) -> str:
    return f"""## Stakeholder Handoff Summary

### Campaign
{analysis["campaign_name"]}

### Current Status
{analysis["status"]}

### What this campaign is trying to do
{analysis["objective"] or "Not specified"}

### Who it is for
{analysis["target_audience"] or "Not specified"}

### Message to align around
{analysis["message"] or "Not specified"}

### Owners and stakeholders
{bullets(analysis["stakeholders"] or ["Not specified"])}

### Assets to confirm
{bullets(analysis["assets"] or ["Not specified"])}

### Open gaps
{bullets(analysis["gaps"])}

### Next decisions needed
{bullets(analysis["next_steps"][:4])}

### One-line handoff
{build_manager_update(analysis)}
"""
