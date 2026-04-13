# 💼 Job Skill Recommender

> A Streamlit-based job market intelligence tool: enter your skills and target role, get ranked job matches and market insights.

[![Live demo](https://img.shields.io/badge/demo-live-brightgreen)](https://job-skill-recommender.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-orange)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**🔗 Live demo: https://job-skill-recommender.streamlit.app/**

---

## What it does

The app has **8 sections** built into a single Streamlit interface:

- **🎯 Job Matching** — enter your job title, skills, location preference and experience level; TF-IDF cosine similarity ranks matching jobs from a local dataset of ~40K records, with live results from the Muse API (free) and optionally Adzuna / Reed when keys are configured
- **💰 Salary Range** — salary distributions by role, country, seniority level, and work mode, with percentile breakdowns
- **📉 Skills Gap Analysis** — compare your current skills against demand signals in the dataset; highlights missing skills by role and industry
- **💼 Career Trends** — demand trends by job title and technology over time
- **🌍 Global Insights** — market size, salary benchmarks, and growth signals across countries
- **🔌 Live Data Pipeline** — dashboard showing the status of each connected API source
- **🏠 Home** — market highlights and top skills at a glance
- **ℹ️ App Information** — setup guide, API configuration, and data documentation

---

## Dataset

| File | Rows | Description |
|---|---|---|
| `data/processed/ml_features_fast.csv` | ~41,000 | Structured job features (employment type, seniority, salary range, country, skills) |
| `data/processed/job_descriptions_sample.csv` | ~10,000 | Job descriptions for text matching |
| `data/raw/job_postings.csv` | ~1,095 | Raw job postings (UK-focused) |
| `data/raw/salary_data.csv` | ~375 | Salary reference data by role and region |

---

## How the matching works

1. User inputs a target title, a set of skills, preferred location(s), work modality, and experience level.
2. Each job in the dataset is scored against those inputs using **TF-IDF cosine similarity** on the combined text fields, weighted by exact-match bonuses for location and experience level.
3. The top 25 matches are returned with a percentage score and the overlapping skills highlighted.
4. When a live API key is configured (Adzuna, Reed, or The Muse), results are supplemented with real-time listings from those sources.

---

## API integrations

| Provider | Free tier | Status |
|---|---|---|
| [The Muse](https://www.themuse.com/developers/api/v2) | ✅ No key required | Working |
| [Adzuna](https://developer.adzuna.com) | ✅ Free registration | Working with key |
| [Reed](https://www.reed.co.uk/developers) | ✅ Free registration | Working with key |
| [RapidAPI](https://rapidapi.com) | ⚠️ Paid subscription | Optional |
| [Theirstack](https://theirstack.com) | ⚠️ Paid subscription | Optional |

Add your keys to a `.env` file (copy `.env.example` as a starting point). The app falls back gracefully to local data when keys are absent.

---

## Run locally

```bash
# 1. Clone
git clone https://github.com/patriciajaquez/job_skill_recommender.git
cd job_skill_recommender

# 2. Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Add your API keys (optional — app works without them)
cp .env.example .env
# Edit .env with your keys

# 4. Run
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project structure

```
job_skill_recommender/
├── app.py                          # Main Streamlit application (~4,500 lines)
├── scripts/
│   └── api_integration.py          # API connectors (Adzuna, Reed, Muse, RapidAPI, Theirstack)
├── src/
│   ├── apis/                       # API abstraction layer
│   ├── data/                       # Data collectors, processors, validators
│   └── models/                     # Job record model
├── data/
│   ├── raw/                        # Source datasets
│   └── processed/                  # Cleaned and feature-engineered datasets
├── notebooks/
│   └── complete_ai_pipeline.ipynb  # EDA and ML experiments
├── tests/
│   ├── test_app.py
│   └── test_api_connections_app.py
├── Dockerfile
├── requirements.txt
├── .env.example                    # Template — copy to .env, never commit .env
└── .gitignore
```

---

## Stack

Python · Streamlit · pandas · scikit-learn (TF-IDF) · Plotly · NumPy · requests · python-dotenv

---

## What I'd improve next

- ~~Deploy to Streamlit Community Cloud~~ ✅ Live at https://job-skill-recommender.streamlit.app/
- Add **sentence-transformer embeddings** (`all-MiniLM-L6-v2`) for semantic matching — better at catching synonyms like "data wrangling" ↔ "ETL"
- Build a small **evaluation set**: (CV, target-job) pairs to measure Recall@10 objectively
- Add a **GitHub Action** to refresh job data from the Muse API on a weekly schedule
- Modularise `app.py` into page modules for easier testing and extension

---

## Author

**Patricia Jáquez** — Data Analyst  
[LinkedIn](https://linkedin.com/in/patricia-jaquez) · [GitHub](https://github.com/patriciajaquez)

---

*Part of a data analytics portfolio built during the Data Science and AI Specialization at Upgrade Hub.*
