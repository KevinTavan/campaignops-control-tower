from src.campaign_engine import analyze_campaign
from src.collision_radar import detect_collisions
import pandas as pd


def test_campaign_readiness_score_exists():
    row = {
        "campaign_id": "C-TEST",
        "campaign_name": "Test Campaign",
        "objective": "Drive awareness for a new workflow product.",
        "target_audience": "Enterprise operations leaders",
        "message": "Workflow automation helps teams reduce manual handoffs and improve speed.",
        "channels": "email, web, sales",
        "assets": "landing page, email, sales enablement",
        "stakeholders": "PMM, Integrated Marketing, Sales",
        "launch_date": "2026-08-01",
        "status": "Planning",
        "measurement_plan": "Track MQLs, conversion rate, and influenced pipeline.",
        "notes": "Strong early campaign brief.",
    }
    analysis = analyze_campaign(row)
    assert analysis["readiness_score"] > 0
    assert "Campaign objective is clearly stated." in analysis["strengths"]


def test_campaign_gaps_detect_missing_measurement():
    row = {
        "campaign_id": "C-TEST",
        "campaign_name": "Test Campaign",
        "objective": "Drive awareness.",
        "target_audience": "Enterprise leaders",
        "message": "A short message.",
        "channels": "email",
        "assets": "email",
        "stakeholders": "PMM",
        "launch_date": "",
        "status": "Draft",
        "measurement_plan": "",
        "notes": "TBD",
    }
    analysis = analyze_campaign(row)
    assert any("Measurement" in gap or "measurement" in gap for gap in analysis["gaps"])


def test_collision_detector_finds_overlap():
    df = pd.DataFrame([
        {
            "campaign_name": "Campaign A",
            "target_audience": "CIOs and enterprise IT leaders",
            "message": "AI workflows improve automation and visibility.",
            "channels": "email, web, sales",
            "assets": "landing page, email",
        },
        {
            "campaign_name": "Campaign B",
            "target_audience": "Enterprise IT leaders and CIOs",
            "message": "AI workflow automation improves visibility and reduces manual work.",
            "channels": "email, web",
            "assets": "landing page, one-pager",
        },
    ])
    collisions = detect_collisions(df, threshold=0.1)
    assert len(collisions) >= 1
