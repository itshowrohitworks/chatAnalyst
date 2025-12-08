from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def predict(data: dict):
    # TEMP dummy response (we replace later with model.pkl)
    return {
        "predicted_donations": 55.7,
        "engagement_score": 82.3
    }
