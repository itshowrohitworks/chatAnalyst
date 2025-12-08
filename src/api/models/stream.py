from pydantic import BaseModel

class Stream(BaseModel):
    streamer_id: int
    title: str
    category: str
    duration_minutes: int
    avg_viewers: int
    peak_viewers: int
    like_count: int
    comment_count: int
    chat_rate: int
