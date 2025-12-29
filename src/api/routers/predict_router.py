from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib
import os

router = APIRouter()

MODEL_PATH = "models/streamer_model.pkl"
ENCODER_PATH = "models/cat_encoder.pkl"
FEATURES_PATH = "models/feature_names.pkl"

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
feature_names = joblib.load(FEATURES_PATH)


# Input schema 
class StreamInput(BaseModel):
    avg_viewers: float
    peak_viewers: float
    chat_rate: float
    like_count: float
    duration_minutes: float
    niche: str
    country: str


@router.post("/")
def predict_stream_donation(data: StreamInput):
    # Convert input to DataFrame
    input_df = pd.DataFrame([data.dict()])

    # Encode categorical columns
    cat_cols = ["niche", "country"]
    encoded = encoder.transform(input_df[cat_cols])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(cat_cols)
    )

    # Combine numeric + encoded
    numeric_df = input_df.drop(columns=cat_cols)
    final_df = pd.concat([numeric_df, encoded_df], axis=1)

    # Ensure all expected features exist
    for col in feature_names:
        if col not in final_df.columns:
            final_df[col] = 0

    # Reorder columns
    final_df = final_df[feature_names]

    # Predict
    prediction = model.predict(final_df)[0]

    return {
        "predicted_stream_donation": round(float(prediction), 2)
    }
