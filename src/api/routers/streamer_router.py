from fastapi import APIRouter, Depends
from api.database import get_db
from api.models.streamer import Streamer

router = APIRouter()

@router.get("/")
def get_streamers(db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM app.streamers;")
    rows = cur.fetchall()

    return [
        {
            "streamer_id": r[0],
            "name": r[1],
            "niche": r[2],
            "followers": r[3],
            "country": r[4],
            "created_at": r[5]
        }
        for r in rows
    ]


@router.post("/")
def create_streamer(data: Streamer, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("""
        INSERT INTO app.streamers (name, niche, followers, country)
        VALUES (%s, %s, %s, %s)
        RETURNING streamer_id;
    """, (data.name, data.niche, data.followers, data.country))

    db.commit()
    return {"message": "Streamer created!", "id": cur.fetchone()[0]}
