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

print("Patient database created successfully.")



cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits(
                visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                visit_date TEXT NOT NULL,
                provider TEXT,
                reason TEXT,
                notes TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
                """)
conn.commit()
conn.close()




