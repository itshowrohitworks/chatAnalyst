from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path
import os

router = APIRouter()

def find_models_dir():
    """Find models directory with multiple fallback paths."""
    # 1) Check env var first
    env = os.getenv("MODEL_DIR")
    if env:
        p = Path(env)
        if p.exists():
            return p
        print(f"⚠️  MODEL_DIR env var set to {env} but doesn't exist")
    
    # 2) Check relative to this file (src/api/routers → src/models)
    current = Path(__file__).resolve()
    relative_up = current.parent.parent.parent / "models"
    if relative_up.exists():
        return relative_up
    
    # 3) Search upwards for any "models" folder
    for parent in current.parents:
        candidate = parent / "models"
        if candidate.exists():
            return candidate
    
    # 4) Render-specific: check /opt/render/project/src/models
    render_path = Path("/opt/render/project/src/models")
    if render_path.exists():
        return render_path
    
    # If nothing found, raise helpful error
    raise FileNotFoundError(
        f"models directory not found!\n"
        f"  Checked: {relative_up}, env var paths, upward search\n"
        f"  On Render, set: MODEL_DIR=/opt/render/project/src/models\n"
        f"  Current file: {current}"
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
