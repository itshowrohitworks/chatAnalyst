import random
from datetime import datetime, timedelta

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.db import get_connection

N_STREAMERS = 20
N_STREAMS = 100
N_DONATIONS = 300

STREAMER_NICHES = ["Gaming", "Tech", "Music", "IRL", "Education", "Finance", "Sports"]
COUNTRIES = ["India", "USA", "UK", "Canada", "Japan", "Germany"]
CATEGORIES = ["Gaming", "Podcast", "Tutorial", "Reaction", "QnA", "Review"]


def create_dummy_streamers(cur):
    streamers = []
    for i in range(N_STREAMERS):
        name = f"Streamer_{i+1}"
        niche = random.choice(STREAMER_NICHES)
        followers = random.randint(5000, 500000)
        country = random.choice(COUNTRIES)

        cur.execute("""
            INSERT INTO app.streamers (name, niche, followers, country)
            VALUES (%s, %s, %s, %s)
            RETURNING streamer_id;
        """, (name, niche, followers, country))

        streamer_id = cur.fetchone()[0]
        streamers.append(streamer_id)

    return streamers


def create_dummy_streams(cur, streamer_ids):
    streams = []
    for i in range(N_STREAMS):
        streamer_id = random.choice(streamer_ids)
        title = f"Stream Title {i+1}"
        category = random.choice(CATEGORIES)
        duration = random.randint(30, 240)  # minutes
        start_time = datetime.now() - timedelta(days=random.randint(1, 60))

        avg_viewers = random.randint(100, 5000)
        peak_viewers = avg_viewers + random.randint(50, 2000)
        likes = random.randint(100, 10000)
        comments = random.randint(50, 5000)
        chat_rate = random.randint(20, 500)

        cur.execute("""
            INSERT INTO app.streams 
            (streamer_id, title, category, duration_minutes, start_time,
             avg_viewers, peak_viewers, like_count, comment_count, chat_rate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING stream_id;
        """, (streamer_id, title, category, duration, start_time,
              avg_viewers, peak_viewers, likes, comments, chat_rate))

        stream_id = cur.fetchone()[0]
        streams.append(stream_id)

    return streams


def create_dummy_donations(cur, streamer_ids, stream_ids):
    for _ in range(N_DONATIONS):
        streamer_id = random.choice(streamer_ids)
        stream_id = random.choice(stream_ids)
        amount = round(random.uniform(1, 200), 2)
        donation_time = datetime.now() - timedelta(days=random.randint(1, 60))

        cur.execute("""
            INSERT INTO app.donations (streamer_id, stream_id, amount, donation_time)
            VALUES (%s, %s, %s, %s);
        """, (streamer_id, stream_id, amount, donation_time))


def main():
    conn = get_connection()
    cur = conn.cursor()

    print("Inserting dummy streamers...")
    streamer_ids = create_dummy_streamers(cur)

    print("Inserting dummy streams...")
    stream_ids = create_dummy_streams(cur, streamer_ids)

    print("Inserting dummy donations...")
    create_dummy_donations(cur, streamer_ids, stream_ids)

    conn.commit()
    cur.close()
    conn.close()

    print("Dummy data inserted successfully!")


if __name__ == "__main__":
    main()