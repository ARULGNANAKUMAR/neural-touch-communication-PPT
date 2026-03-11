import sqlite3
from datetime import datetime

DB_NAME = "robo_ai.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        pulse INTEGER,
        stress TEXT,
        servo1 INTEGER,
        servo2 INTEGER,
        servo3 INTEGER,
        servo4 INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_data(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO sensor_data 
    (temperature, pulse, stress, servo1, servo2, servo3, servo4, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["temperature"],
        data["pulse"],
        data["stress"],
        data["servo1"],
        data["servo2"],
        data["servo3"],
        data["servo4"],
        str(datetime.now())
    ))

    conn.commit()
    conn.close()


def fetch_latest(limit=50):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT temperature, pulse, stress, servo1, servo2, servo3, servo4 
    FROM sensor_data 
    ORDER BY id DESC 
    LIMIT ?
    """, (limit,))

    rows = c.fetchall()
    conn.close()
    return rows
