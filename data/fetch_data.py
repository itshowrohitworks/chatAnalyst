from config.db import get_connection
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

# Fetching Data from Postgresql:
def fetch_ml_data():
    query = """
        SELECT 
            stm.stream_id,
            str.niche,
            str.country,
            stm.avg_viewers,
            stm.peak_viewers,
            stm.chat_rate,
            stm.like_count,
            stm.duration_minutes,
            -- Calculate total donations specifically for THIS stream
            COALESCE(SUM(don.amount), 0) AS stream_donations
        FROM app.streams stm
        JOIN app.streamers str ON stm.streamer_id = str.streamer_id
        LEFT JOIN app.donations don ON stm.stream_id = don.stream_id
        GROUP BY 
            stm.stream_id, 
            str.niche, 
            str.country, 
            stm.avg_viewers, 
            stm.peak_viewers, 
            stm.chat_rate, 
            stm.like_count, 
            stm.duration_minutes
        ORDER BY stm.stream_id ASC;
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            df = pd.DataFrame(cur.fetchall())
            return df
    finally:
        conn.close()