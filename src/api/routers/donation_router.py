from fastapi import APIRouter, Depends
from api.database import get_db
from api.data.donation import Donation

router = APIRouter()

@router.get("/")
def get_donations(db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM app.donations LIMIT 50;")
    return cur.fetchall()


@router.post("/")
def create_donation(data: Donation, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("""
        INSERT INTO app.donations (streamer_id, stream_id, amount)
        VALUES (%s, %s, %s)
        RETURNING donation_id;
    """, (data.streamer_id, data.stream_id, data.amount))

    db.commit()
    return {"message": "Donation added!", "id": cur.fetchone()[0]}
