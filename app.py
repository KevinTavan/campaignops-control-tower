import pandas as pd
import streamlit as st

from src.campaign_engine import (
    analyze_campaign,
    format_campaign_brief,
    build_handoff_summary,
    readiness_dataframe,
)
from src.collision_radar import detect_collisions, format_collision_report


st.set_page_config(
    page_title="CampaignOps Control Tower",
    page_icon="📡",
    layout="wide"
)

st.title("CampaignOps Control Tower")
st.caption("A workflow prototype for turning messy campaign inputs into launch briefs, readiness scores, and message-overlap alerts.")

with st.sidebar:
    st.header("Settings")
    st.info("This tool supports campaign operations review. It does not replace final marketing, legal, sales, or creative approval.")
    st.markdown("**Best for:** integrated marketing, GTM planning, launch ops, campaign handoff, and message governance.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Campaign Brief Analyzer",
    "Launch Readiness Score",
    "Message Collision Radar",
    "Stakeholder Handoff",
    "About"
])


def load_campaign_data():
    source_choice = st.radio(
        "Choose data source",
        ["Use sample data", "Upload CSV"],
        horizontal=True
    )

    if source_choice == "Upload CSV":
        uploaded = st.file_uploader("Upload a campaign CSV", type=["csv"])
        if uploaded:
            return pd.read_csv(uploaded)
        st.warning("No file uploaded yet. Showing sample data.")
        return pd.read_csv("sample_data/campaigns.csv")

    return pd.read_csv("sample_data/campaigns.csv")


with tab1:
    st.subheader("1. Load campaign inputs")
    df = load_campaign_data()

    required_cols = {
        "campaign_id",
        "campaign_name",
        "objective",
        "target_audience",
        "message",
        "channels",
        "assets",
        "stakeholders",
        "launch_date",
        "status",
        "measurement_plan",
        "notes",
    }

    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        st.error(f"CSV is missing required columns: {', '.join(sorted(missing_cols))}")
        st.stop()

    st.dataframe(df, use_container_width=True)

    st.subheader("2. Select a campaign")
    selected_id = st.selectbox("Campaign ID", df["campaign_id"].astype(str).tolist())
    row = df[df["campaign_id"].astype(str) == selected_id].iloc[0]

    st.text_area("Campaign notes", str(row["notes"]), height=140)

    st.subheader("3. Generate campaign operations brief")
    if st.button("Generate campaign brief", type="primary"):
        analysis = analyze_campaign(row.to_dict())
        st.markdown(format_campaign_brief(analysis))

with tab2:
    st.subheader("Launch readiness score")

    df = pd.read_csv("sample_data/campaigns.csv")
    selected_id = st.selectbox("Campaign ID for scoring", df["campaign_id"].astype(str).tolist(), key="score_campaign_id")
    row = df[df["campaign_id"].astype(str) == selected_id].iloc[0]

    analysis = analyze_campaign(row.to_dict())

    score = analysis["readiness_score"]
    if score >= 80:
        st.success(f"Launch readiness score: {score}/100")
    elif score >= 60:
        st.warning(f"Launch readiness score: {score}/100")
    else:
        st.error(f"Launch readiness score: {score}/100")

    score_df = readiness_dataframe(analysis)
    st.bar_chart(score_df.set_index("Category"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Strengths")
        for item in analysis["strengths"]:
            st.write(f"- {item}")

    with col2:
        st.markdown("### Gaps")
        for item in analysis["gaps"]:
            st.write(f"- {item}")

    st.markdown("### Recommended next steps")
    for step in analysis["next_steps"]:
        st.write(f"- {step}")

with tab3:
    st.subheader("Message Collision Radar")
    st.write("Detects possible audience, message, channel, or asset overlap across campaigns.")

    df = pd.read_csv("sample_data/campaigns.csv")
    st.dataframe(df[["campaign_id", "campaign_name", "target_audience", "message", "channels", "status"]], use_container_width=True)

    threshold = st.slider("Overlap sensitivity", min_value=0.10, max_value=0.80, value=0.25, step=0.05)

    if st.button("Scan for collisions", type="primary"):
        collisions = detect_collisions(df, threshold=threshold)
        st.markdown(format_collision_report(collisions))

with tab4:
    st.subheader("Stakeholder handoff")
    df = pd.read_csv("sample_data/campaigns.csv")
    selected_id = st.selectbox("Campaign ID for handoff", df["campaign_id"].astype(str).tolist(), key="handoff_campaign_id")
    row = df[df["campaign_id"].astype(str) == selected_id].iloc[0]

    analysis = analyze_campaign(row.to_dict())
    st.markdown(build_handoff_summary(analysis))

with tab5:
    st.subheader("About this prototype")
    st.markdown(
        """
        CampaignOps Control Tower is a working prototype for integrated marketing and GTM teams.

        **Core design choice:** Campaign data should be structured before teams make launch decisions.

        **Best-fit use cases:**
        - Campaign planning
        - Integrated marketing operations
        - GTM launch readiness
        - Stakeholder handoff
        - Message overlap review
        - Asset checklist review

        **Not appropriate for:**
        - Final legal approval
        - Final creative approval
        - Budget approval
        - Replacing channel owners
        - Replacing marketing strategy judgment

        **Why this matters:**  
        Many campaign problems are not creative problems. They are coordination problems. This tool helps surface those coordination risks earlier.
        """
    )
