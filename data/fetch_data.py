import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.db import get_connection
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

# Fetching Data from Postgresql:
def fetch_ml_data():
    query = """
        SELECT 
        str.streamer_id,
        str.followers,
        str.niche,
        str.country,
        ROUND(AVG(stm.avg_viewers),2) AS avg_viewers,
        ROUND(AVG(stm.peak_viewers),2) AS avg_peak_viewers,
        ROUND(AVG(stm.chat_rate),2) AS avg_chat_rate,
        ROUND(AVG(stm.like_count),2) AS avg_like_count,
        SUM(stm.duration_minutes) AS total_minutes,
        donation_totals.total_donations
        FROM app.streamers str
        JOIN app.streams stm ON str.streamer_id = stm.streamer_id
        JOIN (
            SELECT streamer_id, SUM(amount) as total_donations
            FROM app.donations
            GROUP BY streamer_id
        ) donation_totals ON str.streamer_id = donation_totals.streamer_id
        GROUP BY 
            str.streamer_id, 
            str.followers, 
            str.niche, 
            donation_totals.total_donations
        ORDER BY str.streamer_id ASC;
    """

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            df = pd.DataFrame(rows)
            df.index = df.index + 1
            return df
    finally:
        conn.close()

df = fetch_ml_data()
print(df.head())