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

cursor.execute("""
                CREATE TABLE IF NOT EXISTS vitals(
                vital_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                measurement_date TEXT NOT NULL,
                systolic_bp INTEGER,
                diastolic_bp INTEGER,
                heart_rate INTEGER,
                temperature REAL,
                weight REAL,
                height REAL,
                bmi REAL,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
                )
                """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_data (
        study_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,

        age INTEGER,
        sex TEXT,
        practice_id INTEGER,
        deprivation_score REAL,
        smoking INTEGER,

        measurement_date TEXT,

        bmi REAL,
        systolic_bp INTEGER,
        heart_rate INTEGER,

        treatment INTEGER,
        hospitalized INTEGER,
        hospitalization_date TEXT,

        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        )
        """)

conn.commit()
conn.close()




