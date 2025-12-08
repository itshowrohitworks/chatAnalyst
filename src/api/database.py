import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.db import get_connection

def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
