# Handoff Guide

This guide explains how another person can run and adapt CampaignOps Control Tower.

## Setup

1. Install Python 3.10 or later.
2. Clone the repository.
3. Create a virtual environment.
4. Install requirements.
5. Run `streamlit run app.py`.

## Data format

Use a CSV with these columns:

- campaign_id
- campaign_name
- objective
- target_audience
- message
- channels
- assets
- stakeholders
- launch_date
- status
- measurement_plan
- notes

## Adapting scoring

Scoring logic lives in `src/campaign_engine.py`.

The current score is based on:

- Objective clarity
- Audience clarity
- Message clarity
- Channel coverage
- Asset readiness
- Stakeholder clarity
- Measurement clarity
- Timeline clarity

## Adapting collision detection

Overlap logic lives in `src/collision_radar.py`.

It compares:

- Audience
- Message
- Channel mix
- Asset mix

## Recommended owner

Integrated marketing operations, campaign manager, GTM ops, or PMM operations lead.

## Known limitations

- Overlap detection is keyword-based.
- It does not understand brand nuance or campaign strategy deeply.
- It does not replace creative, legal, sales, or executive review.
- It works best when campaign inputs are reasonably complete.
