import sqlite3

conn = sqlite3.connect("ehr.db")
cursor = conn.cursor()


cursor.execute("""
               CREATE TABLE IF NOT EXISTS patients(
                   patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   dob TEXT,
                   sex TEXT,
                   phone TEXT,
                   address TEXT,
                   emergency_contact TEXT,
                   condition TEXT,
                   allergies TEXT,
                   photo_path TEXT
                   )
               """)

conn.commit()
conn.close()

print("Patient database created successfully.")




