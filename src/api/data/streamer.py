from pydantic import BaseModel

class Streamer(BaseModel):
    name: str
    niche: str
    followers: int
    country: str
