# Chat Analyst – Donation Prediction System

Chat Analyst is an end-to-end machine learning system that predicts the **expected donation amount for a live stream** based on engagement metrics such as viewers, chat activity, likes, duration, niche, and country.

The project demonstrates a **production-style ML workflow** including data engineering, feature engineering, model training, API-based inference, and an interactive frontend.

---

## Project Overview

The goal of this project is to help streamers understand the **donation potential of a specific stream** before it happens.

The model is trained on **historical streaming and donation data** and, when given engagement metrics for a single stream, returns an estimated donation amount.

This is a **regression problem**, not a classification problem.

---

## What the Model Predicts

Given the engagement metrics of a stream, the system predicts:

- The **expected donation amount** for that stream

Example API response:

```json
{
  "predicted_stream_donation": 288.92
}
The prediction is an estimate based on historical patterns, not a guaranteed future outcome.

# System Architecture:

PostgreSQL
   ↓
Data Fetching & Aggregation (SQL)
   ↓
Feature Engineering Pipeline
   ↓
Model Training (RandomForestRegressor)
   ↓
Saved Model Artifacts
   ↓
FastAPI Inference API
   ↓
Streamlit Frontend

# Tech Stack

Backend API: FastAPI

Frontend UI: Streamlit

Database: PostgreSQL

Data Processing: pandas, numpy

Machine Learning: scikit-learn

Model Persistence: joblib

Server: Uvicorn

# Project Structure:
chatAnalyst/
│
├── config/                 # Database configuration
├── data/                   # Data fetching from PostgreSQL
├── pipeline/               # Feature engineering pipeline
├── ml/                     # Model training logic
├── models/                 # Saved model artifacts
├── src/
│   ├── api/                # FastAPI backend
│   └── frontend/           # Streamlit UI
│       ├── logo/
│       └── streamlit_app.py
├── scripts/                # Utility scripts
├── requirements.txt
├── setup.py
└── README.md

# Machine Learning Pipeline
## Data Engineering

SQL joins across streamers, streams, and donations

Stream-level aggregation

Clean dataset generation for ML

## Feature Engineering

Numeric data cleaning

One-hot encoding for categorical variables

Correlation-based feature selection

## Model Training

Train-test split

RandomForestRegressor

Evaluation using MAE and R²

Model, encoder, and feature list saved using joblib

# API Endpoint
## POST /predict

### Request body:

{
  "avg_viewers": 1500,
  "peak_viewers": 3000,
  "chat_rate": 220,
  "like_count": 900,
  "duration_minutes": 120,
  "niche": "Gaming",
  "country": "India"
}


### Response:

{
  "predicted_stream_donation": 288.92
}

# API documentation:

http://127.0.0.1:8000/docs

# Running the Project Locally

## 1. Clone the repository
git clone <repository-url>
cd chatAnalyst

## 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows

## 3. Install dependencies
pip install -r requirements.txt

## 4. Start FastAPI backend
uvicorn api.main:app --reload --app-dir src


## 5. Start Streamlit frontend
streamlit run src/frontend/streamlit_app.py


## Streamlit UI:

http://localhost:8501

# Mobile Testing (Same Network)

To access the application from another device on the same Wi-Fi network:

uvicorn api.main:app --host 0.0.0.0 --port 8000 --app-dir src
streamlit run src/frontend/streamlit_app.py --server.address 0.0.0.0


## Open in mobile browser:

http://<PC-IP>:8501