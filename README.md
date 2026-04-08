# Drug Review Analytics — Patient Safety & Product Performance Analysis

## Business Context

In regulated industries (pharmaceutical, medical devices), patient feedback 
represents a critical source of pharmacovigilance signals. 
This project simulates a **GxP-compliant BI tool** designed to help 
Quality/Regulatory and Product teams monitor safety trends and act quickly 
on risk alerts from unstructured patient reviews.

**Problem statement:** How to rapidly identify risk signals and potential 
non-compliance (patient safety, product quality) from a large volume of 
unstructured patient feedback?

## Project Overview

- **Dataset:** 800K+ patient drug reviews (UCI Drug Review Dataset)
- **Role:** Data Analyst / Insights Translator
- **Stack:** Python, pandas, regex, Power BI

## Pipeline

The Python pipeline (`src/pipeline.py`) handles:

1. **Text cleaning** — HTML entity removal, punctuation normalization, 
   lowercasing
2. **Sentiment proxy** — rating-based classification 
   (≥7 Positive, ≤3 Negative, Neutral otherwise)
3. **Security Alert detection** — keyword matching on cleaned reviews 
   (`hospitaliz`, `suicidal`, `overdose`, `fatal`...)
4. **Strategic drug grouping** — rare drugs with alerts flagged as 
   `RARE_ALERT_TO_CHECK` for regulatory prioritization

## Power BI Dashboard

![Dashboard](assets/dashboard_screenshot.png)

Key visuals:
- Safety alert KPI (% reviews flagging risk keywords)
- Average rating trend over time
- Segmentation by condition and drug group
- RARE_ALERT_TO_CHECK drill-through for regulatory review

## Key Design Decisions

- Sampling strategy for dashboard performance (MVP delivery)
- Rating as sentiment proxy — deliberate choice over NLP scoring 
  (more reliable signal, avoids noise from informal text)
- Keyword list built from real pharmacovigilance terminology

## Next Steps

- [ ] Add screenshot of Power BI dashboard
- [ ] Implement VADER/TextBlob sentiment scoring and compare with rating proxy
- [ ] Deploy as interactive Streamlit app
