from fastapi import APIRouter, Depends
from api.database import get_db
from api.data.stream import Stream

router = APIRouter()

@router.get("/")
def get_streams(db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM app.streams LIMIT 50;")
    rows = cur.fetchall()

    return rows


@router.post("/")
def create_stream(data: Stream, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("""
        INSERT INTO app.streams 
        (streamer_id, title, category, duration_minutes,
         avg_viewers, peak_viewers, like_count, comment_count, chat_rate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING stream_id;
    """, (data.streamer_id, data.title, data.category,
          data.duration_minutes, data.avg_viewers, data.peak_viewers,
          data.like_count, data.comment_count, data.chat_rate))

    db.commit()
    return {"message": "Stream created!", "id": cur.fetchone()[0]}
