import sqlite3

DATABASE = 'ehr.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
cursor.execute("""
                CREATE TABLE IF NOT EXISTS pulse_beats(
                beat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                beat_number INTEGER,
                beat_time REAL,
                interval_seconds REAL,
                beat_bpm REAL,
            FOREIGN KEY (session_id) REFERENCES pulse_sessions(session_id)
                )
                """)

conn.commit()
conn.close()
print("pulse_beats table created successfully.")