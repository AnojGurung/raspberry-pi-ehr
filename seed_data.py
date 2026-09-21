import sqlite3
from datetime import datetime, timedelta

DATABASE = "ehr.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()


# --------------------------------------------------
# CHECK WHETHER PATIENTS ALREADY EXIST
# --------------------------------------------------

cursor.execute("SELECT COUNT(*) FROM patients")
existing_patients = cursor.fetchone()[0]

if existing_patients > 0:
    print(
        f"There are already {existing_patients} patients in the database."
    )
    print("Patients were NOT added again to avoid duplicates.")
    conn.close()
    raise SystemExit


# --------------------------------------------------
# SYNTHETIC PATIENT DATA
# --------------------------------------------------

patients = [
    ("Maya", "Shrestha", "1988-05-14", "f",
     "9175551001", "Queens NY", "9175552001",
     "Hypertension", "Penicillin"),

    ("Daniel", "Lee", "1976-11-22", "m",
     "9175551002", "Brooklyn NY", "9175552002",
     "Type 2 Diabetes", "None"),

    ("Sofia", "Martinez", "1993-07-08", "f",
     "9175551003", "Bronx NY", "9175552003",
     "Asthma", "Pollen"),

    ("Robert", "Johnson", "1965-02-18", "m",
     "9175551004", "Manhattan NY", "9175552004",
     "Hypertension", "Sulfa"),

    ("Priya", "Patel", "1982-09-03", "f",
     "9175551005", "Queens NY", "9175552005",
     "Type 2 Diabetes", "None"),

    ("James", "Wilson", "1971-06-12", "m",
     "9175551006", "Brooklyn NY", "9175552006",
     "Hypertension", "None"),

    ("Emily", "Brown", "1990-12-21", "f",
     "9175551007", "Queens NY", "9175552007",
     "Asthma", "Dust"),

    ("Michael", "Davis", "1958-04-09", "m",
     "9175551008", "Bronx NY", "9175552008",
     "Type 2 Diabetes", "None"),

    ("Aisha", "Khan", "1985-10-17", "f",
     "9175551009", "Queens NY", "9175552009",
     "Hypertension", "None"),

    ("Carlos", "Rivera", "1979-03-28", "m",
     "9175551010", "Manhattan NY", "9175552010",
     "Type 2 Diabetes", "None"),

    ("Linda", "Garcia", "1969-07-15", "f",
     "9175551011", "Brooklyn NY", "9175552011",
     "Hypertension", "None"),

    ("Kevin", "Nguyen", "1996-01-11", "m",
     "9175551012", "Queens NY", "9175552012",
     "None", "None"),

    ("Fatima", "Ali", "1987-08-25", "f",
     "9175551013", "Bronx NY", "9175552013",
     "Asthma", "Pollen"),

    ("George", "Miller", "1955-11-03", "m",
     "9175551014", "Queens NY", "9175552014",
     "Type 2 Diabetes", "None"),

    ("Rachel", "Thomas", "1992-05-19", "f",
     "9175551015", "Brooklyn NY", "9175552015",
     "None", "None"),

    ("Samuel", "Kim", "1980-02-14", "m",
     "9175551016", "Manhattan NY", "9175552016",
     "Hypertension", "None"),

    ("Nina", "Singh", "1974-09-30", "f",
     "9175551017", "Queens NY", "9175552017",
     "Type 2 Diabetes", "None"),

    ("David", "Anderson", "1962-03-05", "m",
     "9175551018", "Bronx NY", "9175552018",
     "Hypertension", "None"),

    ("Laura", "Moore", "1989-06-07", "f",
     "9175551019", "Brooklyn NY", "9175552019",
     "Asthma", "Dust"),

    ("Joseph", "Taylor", "1977-12-01", "m",
     "9175551020", "Queens NY", "9175552020",
     "Type 2 Diabetes", "None"),

    ("Maria", "Lopez", "1983-04-23", "f",
     "9175551021", "Manhattan NY", "9175552021",
     "Hypertension", "None"),

    ("Andrew", "Clark", "1994-10-10", "m",
     "9175551022", "Queens NY", "9175552022",
     "None", "None"),

    ("Sara", "Ahmed", "1970-01-27", "f",
     "9175551023", "Brooklyn NY", "9175552023",
     "Type 2 Diabetes", "None"),

    ("Brian", "Hall", "1967-08-16", "m",
     "9175551024", "Bronx NY", "9175552024",
     "Hypertension", "None"),

    ("Jessica", "Young", "1991-03-13", "f",
     "9175551025", "Queens NY", "9175552025",
     "Asthma", "Pollen"),

    ("Omar", "Hassan", "1986-11-29", "m",
     "9175551026", "Brooklyn NY", "9175552026",
     "Type 2 Diabetes", "None"),

    ("Karen", "King", "1959-05-18", "f",
     "9175551027", "Manhattan NY", "9175552027",
     "Hypertension", "None"),

    ("Steven", "Wright", "1981-07-02", "m",
     "9175551028", "Queens NY", "9175552028",
     "None", "None"),

    ("Angela", "Scott", "1975-02-09", "f",
     "9175551029", "Bronx NY", "9175552029",
     "Type 2 Diabetes", "None"),

    ("Peter", "Green", "1964-09-21", "m",
     "9175551030", "Brooklyn NY", "9175552030",
     "Hypertension", "None")
]


# --------------------------------------------------
# INSERT PATIENTS
# --------------------------------------------------

cursor.executemany("""
    INSERT INTO patients (
        first_name,
        last_name,
        dob,
        sex,
        phone,
        address,
        emergency_contact,
        condition,
        allergies
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", patients)

conn.commit()

print("30 synthetic patients added successfully.")


# --------------------------------------------------
# GET THE NEW PATIENT IDs
# --------------------------------------------------

cursor.execute("""
    SELECT patient_id,
           first_name,
           last_name,
           condition
    FROM patients
    ORDER BY patient_id
""")

patient_records = cursor.fetchall()


# --------------------------------------------------
# CREATE SYNTHETIC VISITS
# --------------------------------------------------

visits = []

providers = [
    "Dr. Smith",
    "Dr. Patel",
    "Dr. Chen",
    "Dr. Williams"
]

start_date = datetime(2026, 1, 10)

for index, patient in enumerate(patient_records):

    patient_id = patient[0]
    condition = patient[3]

    # Give every patient 3 visits
    for visit_number in range(3):

        visit_date = (
            start_date
            + timedelta(
                days=(visit_number * 90) + (index % 20)
            )
        )

        provider = providers[index % len(providers)]

        if condition == "Hypertension":
            if visit_number == 0:
                reason = "Hypertension evaluation"
            else:
                reason = "Blood pressure follow-up"

        elif condition == "Type 2 Diabetes":
            if visit_number == 0:
                reason = "Diabetes evaluation"
            else:
                reason = "Diabetes follow-up"

        elif condition == "Asthma":
            if visit_number == 0:
                reason = "Asthma evaluation"
            else:
                reason = "Respiratory follow-up"

        else:
            if visit_number == 0:
                reason = "Annual physical"
            else:
                reason = "Routine follow-up"

        notes = "Synthetic visit generated for research analysis."

        visits.append(
            (
                patient_id,
                visit_date.strftime("%Y-%m-%d"),
                provider,
                reason,
                notes
            )
        )


# --------------------------------------------------
# INSERT VISITS
# --------------------------------------------------

cursor.executemany("""
    INSERT INTO visits (
        patient_id,
        visit_date,
        provider,
        reason,
        notes
    )
    VALUES (?, ?, ?, ?, ?)
""", visits)

conn.commit()


# --------------------------------------------------
# FINAL CHECK
# --------------------------------------------------

cursor.execute("SELECT COUNT(*) FROM patients")
patient_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM visits")
visit_count = cursor.fetchone()[0]

conn.close()


print("Synthetic visits added successfully.")

print("\n--- SEED DATA SUMMARY ---")
print("Patients:", patient_count)
print("Visits:", visit_count)