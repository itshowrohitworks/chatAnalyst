from fastapi import FastAPI
from api.routers.streamer_router import router as streamer_router
from api.routers.stream_router import router as stream_router
from api.routers.donation_router import router as donation_router
from api.routers.predict_router import router as predict_router

app = FastAPI(title="Chat Analyst API", version="1.0")

# Routers
app.include_router(streamer_router, prefix="/streamers", tags=["Streamers"])
app.include_router(stream_router, prefix="/streams", tags=["Streams"])
app.include_router(donation_router, prefix="/donations", tags=["Donations"])
app.include_router(predict_router, prefix="/predict", tags=["Predict"])


@app.get("/", tags=["Root"])
def root():
    return {"message": "Chat Analyst API is running."}

# uvicorn api.main:app --reload --app-dir src 