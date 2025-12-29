from pydantic import BaseModel

class Donation(BaseModel):
    streamer_id: int
    stream_id: int
    amount: float
