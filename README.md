# Chat Analyst – Donation Prediction System

Chat Analyst is an end-to-end machine learning system that predicts the **expected donation amount for a live stream** using engagement metrics such as viewers, chat activity, likes, stream duration, niche, and country.

The project demonstrates a **production-style ML workflow**, covering data engineering, feature engineering, model training, API-based inference, and an interactive frontend.

---

## Overview

Live streamers often want to understand how much donation a particular stream may generate before going live.  
Chat Analyst solves this by learning from **historical streaming and donation data** and estimating the donation potential of a single stream based on its engagement characteristics.

This project focuses on **system design and real-world ML integration**, not just model accuracy.

---

## Problem Type

- **Machine Learning Task**: Regression  
- **Target Variable**: Expected donation amount per stream  
- **Input**: Engagement metrics of a single stream  

---

## Example Prediction

### API Response

```json

{
  "predicted_stream_donation": 288.92
}
```
# System Architecture:

```
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
```
# Tech Stack
```
Backend API: FastAPI



Frontend UI: Streamlit



Database: PostgreSQL



Data Processing: pandas, numpy



Machine Learning: scikit-learn



Model Persistence: joblib



Server: Uvicorn
```
# Project Structure:
```
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
```
# Machine Learning Pipeline:

## 1. Data Engineering:

SQL joins across streamers, streams, and donations

Stream-level aggregation

Clean dataset generation for ML

## 2. Feature Engineering
Numeric data cleaning

One-hot encoding for categorical variables

Correlation-based feature selection



## 3. Model Training

Train-test split

RandomForestRegressor

Evaluation using MAE and R²

Model, encoder, and feature list saved using joblib

# API Endpoint

## POST /predict

### Request body:
```
{

  "avg_viewers": 1500,

  "peak_viewers": 3000,

  "chat_rate": 220,

  "like_count": 900,

  "duration_minutes": 120,

  "niche": "Gaming",

  "country": "India"

}
```
### Response:
```
{

  "predicted_stream_donation": 288.92

}
```
# API documentation:
```
http://127.0.0.1:8000/docs
```

# Running the Project Locally:

## 1. Clone the repository

git clone <repository-url>

cd chatAnalyst

## 2. Create and activate virtual environment
### I used uv virtual environment:
#### a. To install uv use:
```
pip install uv
```
#### b. To create virtual env using uv:
```
uv venv
```
#### c. Activate using:
```
source .venv/bin/activate      # Linux / macOS

.venv\Scripts\activate         # Windows
```
## 3. Install dependencies
```
uv pip install -r requirements.txt
```
## 4. Start FastAPI backend
```
uvicorn api.main:app --reload --app-dir src
```
## 5. Start Streamlit frontend
```
streamlit run src/frontend/streamlit_app.py --server.address localhost
```
## Streamlit UI:
```
http://localhost:8501
```
# Mobile Testing (Same Network)
## Run the fastapi webserver and Streamlit with these commands:
```
uvicorn api.main:app --host 0.0.0.0 --port 8000 --app-dir src
streamlit run src/frontend/streamlit_app.py --server.address 0.0.0.0
```
## Open in mobile browser:
```
http://<PC-IP>:8501
```
