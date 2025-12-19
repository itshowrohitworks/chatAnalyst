import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.db import get_connection

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    result = cur.fetchone()
    print("Connected successfully!")
    print("PostgreSQL version:", result)

    cur.execute("SELECT COUNT(*) FROM app.streams;")
    print("Streams count:", cur.fetchone())
    
    cur.close()
    conn.close()

except Exception as e:
    print("Connection failed:", e)