from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path
import os

router = APIRouter()

def find_models_dir():
    # 1) allow override via env var
    env = os.getenv("MODEL_DIR")
    if env:
        p = Path(env)
        if p.exists():
            return p
    # 2) search upwards from this file for a "models" directory
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents)[:6]:
        candidate = parent / "models"
        if candidate.exists():
            return candidate
    # Helpful error if not found
    raise FileNotFoundError(
        "models directory not found. Searched from "
        f"{current} upward. Either add a models/ folder to the repo root or "
        "set the MODEL_DIR environment variable to the correct path "
        "(e.g. /opt/render/project/src/models on Render)."
    )

# -------------------------------------------------
# Model paths (routers → api → src)
# -------------------------------------------------
MODEL_DIR = find_models_dir()
MODEL_PATH = MODEL_DIR / "streamer_model.pkl"
ENCODER_PATH = MODEL_DIR / "cat_encoder.pkl"
FEATURES_PATH = MODEL_DIR / "feature_names.pkl"

# -------------------------------------------------
# Lazy-loaded global objects
# -------------------------------------------------
model = None
encoder = None
feature_names = None


def load_model():
    """Load ML artifacts only once (lazy loading)."""
    global model, encoder, feature_names

    if model is None:
        model = joblib.load(MODEL_PATH)
        encoder = joblib.load(ENCODER_PATH)
        feature_names = joblib.load(FEATURES_PATH)


# -------------------------------------------------
# Input Schema
# -------------------------------------------------
class StreamInput(BaseModel):
    avg_viewers: float
    peak_viewers: float
    chat_rate: float
    like_count: float
    duration_minutes: float
    niche: str
    country: str


# -------------------------------------------------
# Prediction Endpoint
# -------------------------------------------------
@router.post("/")
def predict_stream_donation(data: StreamInput):
    load_model()

    # Convert input to DataFrame (Pydantic v2 safe)
    input_df = pd.DataFrame([data.model_dump()])

    # Encode categorical features
    cat_cols = ["niche", "country"]
    encoded = encoder.transform(input_df[cat_cols])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(cat_cols)
    )

    # Combine numeric and encoded features
    numeric_df = input_df.drop(columns=cat_cols)
    final_df = pd.concat([numeric_df, encoded_df], axis=1)

    # Ensure feature alignment
    for col in feature_names:
        if col not in final_df.columns:
            final_df[col] = 0

    final_df = final_df[feature_names]

    # Predict
    prediction = model.predict(final_df)[0]

    return {
        "predicted_stream_donation": round(float(prediction), 2)
    }
