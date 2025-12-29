# Chat Analyst – Donation Prediction System
## Chat Analyst is an end-to-end machine learning system that predicts the expected donation amount for a live stream based on engagement metrics such as viewers, chat activity, likes, duration, niche, and country.

This project demonstrates a production-style ML workflow including data engineering, feature engineering, model training, API-based inference, and an interactive web frontend.

# Project Overview
The goal of Chat Analyst is to help streamers understand the donation potential of a specific stream before it happens. By analyzing historical streaming data, the system identifies patterns between engagement and revenue.

# Problem Type: Regression (predicting a continuous dollar amount).

# Target Variable: predicted_stream_donation

# Model: RandomForestRegressor

# Tech Stack
Backend API: FastAPI (Uvicorn)

Frontend UI: Streamlit

Database: PostgreSQL

Data Processing: pandas, numpy

Machine Learning: scikit-learn

Model Persistence: joblib

# Project Structure

chatAnalyst/
│
├── config/                 # Database connection & configuration
├── data/                   # Data fetching scripts (SQL)
├── pipeline/               # Feature engineering & preprocessing
├── ml/                     # Model training and evaluation logic
├── models/                 # Saved model artifacts (.joblib)
├── src/
│   ├── api/                # FastAPI backend implementation
│   └── frontend/           # Streamlit UI
│       ├── logo/           # Asset files
│       └── streamlit_app.py
├── scripts/                # Utility & automation scripts
├── requirements.txt        # Project dependencies
├── setup.py                # Package setup
└── README.md               # Project documentation

# Machine Learning Pipeline
## 1. Data Engineering
Performs SQL joins across streamers, streams, and donations tables.

Aggregates data at the stream level.

Handles missing values and generates a cleaned dataset.

## 2. Feature Engineering
Numeric data scaling and cleaning.

One-Hot Encoding for categorical variables (Niche, Country).

Correlation-based feature selection to improve model accuracy.

## 3. Training & Evaluation
Uses a RandomForestRegressor for robust non-linear predictions.

Evaluated using Mean Absolute Error (MAE) and R² Score.

The trained model, encoder, and feature list are exported for production use.

# API Documentation
## POST /predict
### Request Body:

JSON

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

JSON

{
  "predicted_stream_donation": 288.92
}

### Note: Predictions are estimates based on historical patterns and do not guarantee future outcomes.

# Running the Project Locally
## 1. Clone the repository
Bash

git clone <repository-url>
cd chatAnalyst

## 2. Set up a Virtual Environment
Bash

python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
## 3. Install Dependencies
Bash

pip install -r requirements.txt

## 4. Start the Backend (FastAPI)
Bash

uvicorn api.main:app --reload --app-dir src
API Docs available at: http://127.0.0.1:8000/docs

## 5. Start the Frontend (Streamlit)
Bash

# Run in a new terminal tab
streamlit run src/frontend/streamlit_app.py
UI available at: http://localhost:8501

# Mobile Testing (Same Network)
To access the application from a mobile device or another PC on the same Wi-Fi network:

Run Backend:

Bash

uvicorn api.main:app --host 0.0.0.0 --port 8000 --app-dir src
Run Frontend:

Bash

streamlit run src/frontend/streamlit_app.py --server.address 0.0.0.0
Access: Open http://<YOUR-PC-IP>:8501 on your mobile browser.
