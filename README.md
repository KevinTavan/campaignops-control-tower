# CampaignOps Control Tower

A working Streamlit prototype for integrated marketing teams that turns messy campaign inputs into structured launch briefs, readiness scores, message overlap alerts, asset gaps, and stakeholder handoff summaries.

This project demonstrates applied AI workflow thinking for integrated marketing, GTM operations, campaign planning, and cross-functional handoff. It uses deterministic local logic, so it works without any API key.

## Why this exists

Integrated marketing teams often manage overlapping campaigns across multiple audiences, channels, stakeholders, launch dates, and asset types. Campaign information can live across decks, spreadsheets, meeting notes, chats, and launch briefs. This creates duplicated work, unclear ownership, inconsistent messaging, and launch risk.

CampaignOps Control Tower helps structure that chaos into a clearer operating view.

## What it does

- Loads sample campaign data or a CSV upload
- Generates a structured campaign operations brief
- Scores launch readiness from 0 to 100
- Flags missing campaign inputs
- Reviews audience, message, channel, asset, stakeholder, and measurement clarity
- Detects possible message or audience overlap across campaigns
- Creates a stakeholder handoff summary
- Provides a manager-ready update
- Includes documentation for handoff and workflow use

## What this does not do

This tool does not replace marketing judgment, campaign strategy, creative review, sales alignment, legal review, or final launch approval. It is a workflow support tool that helps teams see gaps earlier.

## Demo

Run locally:

```bash
git clone https://github.com/YOUR-USERNAME/campaignops-control-tower.git
cd campaignops-control-tower
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## CSV format

Your uploaded CSV should include:

```csv
campaign_id,campaign_name,objective,target_audience,message,channels,assets,stakeholders,launch_date,status,measurement_plan,notes
```

See `sample_data/campaigns.csv`.

## Repository structure

```text
.
├── app.py
├── requirements.txt
├── sample_data/
│   └── campaigns.csv
├── src/
│   ├── __init__.py
│   ├── campaign_engine.py
│   └── collision_radar.py
├── docs/
│   ├── problem-statement.md
│   ├── handoff-guide.md
│   └── scoring-methodology.md
└── tests/
    └── test_campaign_engine.py
```

## Why this is useful

This project demonstrates:

- Integrated marketing workflow design
- GTM and launch-readiness thinking
- Structured campaign evaluation
- Message overlap detection
- Stakeholder handoff planning
- Practical operations documentation
- Building usable tools for non-technical teams

## Portfolio positioning

CampaignOps Control Tower shows how messy campaign inputs can become structured, reviewable, and actionable operating briefs. It is built for integrated marketing teams that need stronger coordination across campaigns, assets, channels, stakeholders, and launch timelines.

## Roadmap

- Add export to PDF or Markdown
- Add timeline risk view
- Add campaign dependency mapping
- Add persona-to-proof gap analysis
- Add channel coverage visualization
- Add optional LLM-generated campaign rewrites
- Add GTM Readiness Simulator as a companion app
