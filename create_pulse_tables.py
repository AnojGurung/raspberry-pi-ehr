import sqlite3

DATABASE = "ehr.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS pulse_sessions(
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                measurement_time TEXT,
                final_bpm INTEGER,
                beats_detected INTEGER,
                median_interval REAL,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
                """)

cursor.execute ("""
                CREATE TABLE IF NOT EXISTS pulse_samples(
                sample_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                elapsed_time REAL,
                raw_value INTEGER,
                smooth_value REAL,
                FOREIGN KEY (session_id) REFERENCES pulse_sessions(session_id)
                )
                """)

conn.commit()
conn.close()

print("Pulse tables created successfully.")
